"""Check the loaded NooRules package against its latest stable Git tag."""

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

REPOSITORIES = {
    "noorules": ("noo-dev", "noorules-dev"),
    "noorules-presale": ("noo-presale", "noorules-presale"),
}
VERSION = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"


def parts(version):
    match = re.fullmatch(VERSION, version)
    return tuple(int(component) for component in match.groups()) if match else None


def latest(refs):
    versions = []
    for line in refs.splitlines():
        _, separator, ref = line.partition("\t")
        if separator and ref.startswith("refs/tags/v"):
            version = ref.removeprefix("refs/tags/v")
            if parts(version) is not None:
                versions.append(version)
    return max(versions, key=parts, default=None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", choices=("codex", "claude"), required=True)
    args = parser.parse_args()
    package = Path(__file__).resolve().parents[3]
    manifest = ".codex-plugin" if args.client == "codex" else ".claude-plugin"
    try:
        info = json.loads((package / manifest / "plugin.json").read_text(encoding="utf-8"))
        installed = info["version"]
        repo, marketplace = REPOSITORIES[info["name"]]
        if parts(installed) is None:
            raise ValueError("Неформатная версия")
        settings = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_SSH_COMMAND": "ssh -o BatchMode=yes -o ConnectTimeout=3"}
        query = subprocess.run(
            ["git", "ls-remote", "--refs", "--tags", f"git@github.com:EgorPaleev/{repo}.git", "v*"],
            capture_output=True, text=True, timeout=5, env=settings, check=True,
        )
        available = latest(query.stdout)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError):
        return
    if available and parts(available) > parts(installed):
        print(json.dumps({"installed": installed, "available": available, "marketplace": marketplace,
                          "plugin": info["name"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
