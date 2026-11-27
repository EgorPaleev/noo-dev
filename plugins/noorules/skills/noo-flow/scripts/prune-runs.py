"""Remove temporary files for closed NooRules runs."""

import json
import re
import shutil
import subprocess
from pathlib import Path, PurePosixPath


RUN_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,63}")


def git(*args):
    return subprocess.check_output(["git", *args], text=True)


def read_record(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Недоступна запись {path}")
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict) or record.get("schemaVersion") != 1:
        raise ValueError(f"Неизвестный формат {path}")
    return record


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


def closed_run(state, summary):
    if state is not None:
        steps = state["steps"]
        if not steps or any(step["status"] != "completed" for step in steps):
            return False
    if summary is not None and summary.get("keepArtifacts", False) is not False:
        return False
    if state is not None and "closed" in state:
        return state["closed"] is True
    return (
        summary is not None
        and isinstance(summary.get("closedAt"), str)
        and isinstance(summary.get("result"), str)
        and isinstance(summary.get("checks"), list)
    )


def prune(root):
    storage = root / ".noorules" / "runs"
    if storage.parent.is_symlink() or storage.is_symlink() or not storage.is_dir():
        return

    tracked = git("-C", str(root), "ls-files", "-z", "--", ".noorules/runs")
    protected = {run_from_path(path) for path in tracked.split("\0")}
    candidates = {}
    dependencies = {}
    for directory in storage.iterdir():
        if directory.is_symlink() or not directory.is_dir() or not RUN_ID.fullmatch(directory.name):
            continue
        run_id = directory.name
        state_path = directory / "run.json"
        summary_path = directory / "summary.json"
        work_dir = directory / "work"
        state = read_record(state_path) if state_path.exists() or state_path.is_symlink() else None
        summary = read_record(summary_path) if summary_path.exists() and not summary_path.is_symlink() else None
        if state is not None:
            dependencies[run_id] = referenced_runs(state)
        if (
            not work_dir.is_symlink()
            and not summary_path.is_symlink()
            and (not work_dir.exists() or work_dir.is_dir())
            and closed_run(state, summary)
        ):
            candidates[run_id] = directory
        else:
            protected.add(run_id)

    pending = list(protected)
    while pending:
        needed = dependencies.get(pending.pop(), set()) - protected
        protected.update(needed)
        pending.extend(needed)

    for run_id in candidates.keys() - protected:
        directory = candidates[run_id]
        work_dir = directory / "work"
        if work_dir.exists():
            shutil.rmtree(work_dir)
        (directory / "run.json").unlink(missing_ok=True)
        (directory / "summary.json").unlink(missing_ok=True)
        if not any(directory.iterdir()):
            directory.rmdir()


if __name__ == "__main__":
    try:
        project_root = Path(git("rev-parse", "--show-toplevel").rstrip("\n"))
        prune(project_root)
    except (KeyError, TypeError, AttributeError, ValueError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Очистка запусков остановлена: {error}")
