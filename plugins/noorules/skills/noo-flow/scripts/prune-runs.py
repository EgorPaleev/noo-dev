"""Compact closed NooRules runs in the current Git working copy."""

import json
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath


RUN_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,63}")
MAX_AGE = timedelta(days=30)
MAX_SUMMARIES = 20


def git(*args):
    return subprocess.check_output(["git", *args], text=True)


def read_record(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Недоступна запись {path}")
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict) or record.get("schemaVersion") != 1:
        raise ValueError(f"Неизвестный формат {path}")
    return record


def closed_at(summary, now):
    if not isinstance(summary.get("result"), str) or not isinstance(summary.get("checks"), list):
        raise ValueError("Нет итога или списка проверок")
    stamp = datetime.fromisoformat(summary["closedAt"].replace("Z", "+00:00"))
    if stamp.tzinfo is None or stamp > now:
        raise ValueError("Некорректное время завершения")
    return stamp


def run_from_path(path):
    parts = PurePosixPath(path).parts
    if len(parts) > 2 and parts[:2] == (".noorules", "runs"):
        return parts[2]
    return None


def referenced_runs(record):
    references = set()
    for key, value in record.items():
        if isinstance(value, dict):
            references.update(referenced_runs(value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    references.update(referenced_runs(item))
        elif isinstance(value, str):
            if key == "sourceRun":
                references.add(value)
            elif key in {"path", "snapshotPath"}:
                run_id = run_from_path(value)
                if run_id:
                    references.add(run_id)
    return references


def compact(run_dir):
    work_dir = run_dir / "work"
    state_path = run_dir / "run.json"
    if work_dir.is_symlink() or (work_dir.exists() and not work_dir.is_dir()):
        return False
    if state_path.is_symlink():
        return False
    if work_dir.exists():
        shutil.rmtree(work_dir)
    state_path.unlink(missing_ok=True)
    return True


def prune(root, now):
    storage = root / ".noorules" / "runs"
    if storage.parent.is_symlink() or storage.is_symlink() or not storage.is_dir():
        return

    tracked = git("-C", str(root), "ls-files", "-z", "--", ".noorules/runs")
    protected = {run_from_path(path) for path in tracked.split("\0")}
    candidates = []
    for directory in sorted(storage.iterdir()):
        if directory.is_symlink() or not directory.is_dir() or not RUN_ID.fullmatch(directory.name):
            continue
        state_path = directory / "run.json"
        summary_path = directory / "summary.json"
        state = read_record(state_path) if state_path.exists() or state_path.is_symlink() else None
        if state is not None:
            # Сохраняем входы других запусков, даже если у них ещё нет записи о завершении.
            protected.update(referenced_runs(state) - {directory.name})
            steps = state["steps"]
            if not steps or any(step["status"] != "completed" for step in steps):
                continue
        if not summary_path.exists() or summary_path.is_symlink():
            continue
        try:
            summary = read_record(summary_path)
            stamp = closed_at(summary, now)
        except (KeyError, TypeError, AttributeError, ValueError):
            continue
        if summary.get("keepArtifacts", False) is not False:
            protected.add(directory.name)
        candidates.append((stamp, directory))

    eligible = sorted(
        (entry for entry in candidates if entry[1].name not in protected), reverse=True
    )
    for index, (stamp, directory) in enumerate(eligible):
        if not compact(directory):
            continue
        if now - stamp >= MAX_AGE or index >= MAX_SUMMARIES:
            (directory / "summary.json").unlink()
            if not any(directory.iterdir()):
                directory.rmdir()


if __name__ == "__main__":
    try:
        project_root = Path(git("rev-parse", "--show-toplevel").rstrip("\n"))
        prune(project_root, datetime.now(timezone.utc))
    except (KeyError, TypeError, AttributeError, ValueError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Очистка запусков остановлена: {error}")
