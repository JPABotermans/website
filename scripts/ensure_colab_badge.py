#!/usr/bin/env python3
"""Ensure a post notebook carries an up-to-date 'Open in Colab' badge.

The badge points at this notebook's own path in the GitHub repo, derived from
the git remote and current branch. Idempotent: it updates an existing badge cell
(identified by the HTML marker) or inserts one right after the front-matter cell.

Usage: python3 scripts/ensure_colab_badge.py posts/<slug>/index.ipynb [more.ipynb ...]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "<!-- colab-badge -->"
FALLBACK_SLUG = "JPABotermans/website"
FALLBACK_BRANCH = "main"


def _git(args, fallback):
    try:
        return subprocess.check_output(["git", *args], text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return fallback


def repo_slug():
    url = _git(["config", "--get", "remote.origin.url"], "")
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    return m.group(1) if m else FALLBACK_SLUG


def default_branch():
    ref = _git(["symbolic-ref", "--quiet", "refs/remotes/origin/HEAD"], "")
    return ref.rsplit("/", 1)[-1] if ref else FALLBACK_BRANCH


def badge_source(rel_path):
    url = (
        f"https://colab.research.google.com/github/"
        f"{repo_slug()}/blob/{default_branch()}/{rel_path}"
    )
    return [
        f"{MARKER}\n",
        f"[![Open In Colab](https://colab.research.google.com/assets/"
        f"colab-badge.svg)]({url})",
    ]


def ensure_badge(path):
    p = Path(path)
    nb = json.loads(p.read_text())
    cells = nb.get("cells", [])
    src = badge_source(p.as_posix())

    idx = next(
        (
            i
            for i, c in enumerate(cells)
            if c.get("cell_type") == "markdown"
            and any(MARKER in line for line in c.get("source", []))
        ),
        None,
    )
    if idx is None:
        # Keep the raw YAML front-matter cell first, if present.
        insert_at = 1 if cells and cells[0].get("cell_type") == "raw" else 0
        cells.insert(insert_at, {"cell_type": "markdown", "metadata": {}, "source": src})
    else:
        cells[idx]["source"] = src

    nb["cells"] = cells
    p.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        ensure_badge(arg)
