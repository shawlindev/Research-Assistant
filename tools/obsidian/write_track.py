"""Update a track file's Status section and optionally append Observations."""
import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

_project_root = None

TEMPLATE = """\
---
track: {name}
title: {title}
updated: {today}
---

# {title}

## Status
_Overwritten every session-close. Current snapshot only — no history here._

**State:** active
**Last session:** {today}
**In progress:** (not started)
**Blocked on:** (nothing)
**Next:** (to be defined)

## Context
_Stable background. Rarely changes. Architecture, constraints, key decisions._

(To be filled in.)

## Observations
_Append-only. Typed, dated entries. The long-term memory of this track._

## Dependencies
_[[wiki-links]] to related tracks. Builds the Obsidian graph._

"""


def get_project_root() -> Path:
    global _project_root
    if _project_root is not None:
        return _project_root
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        _project_root = Path(result.stdout.strip())
        return _project_root
    except subprocess.CalledProcessError:
        print("Error: not inside a git repository", file=sys.stderr)
        sys.exit(1)


def _read_track(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _update_frontmatter_date(content: str, today: str) -> str:
    return re.sub(r"(?m)^updated:.*$", f"updated: {today}", content)


def _replace_status(content: str, status_block: str) -> str:
    """Replace everything between '## Status' and '## Context'."""
    pattern = r"(## Status\n).*?(\n## Context)"
    replacement = rf"\g<1>{status_block}\n\g<2>"
    return re.sub(pattern, replacement, content, flags=re.DOTALL)


def _build_status_block(state: str, in_progress: str, blocked: str, next_step: str, today: str) -> str:
    return (
        f"_Overwritten every session-close. Current snapshot only — no history here._\n\n"
        f"**State:** {state}\n"
        f"**Last session:** {today}\n"
        f"**In progress:** {in_progress}\n"
        f"**Blocked on:** {blocked}\n"
        f"**Next:** {next_step}"
    )


def _append_observations(content: str, observations: list) -> str:
    """Append observations to the end of the ## Observations section (before ## Dependencies)."""
    if not observations:
        return content
    today = date.today().isoformat()
    new_entries = []
    for obs in observations:
        if re.match(r"^\[.+?\] \d{4}-\d{2}-\d{2}", obs):
            new_entries.append(f"- {obs}")
        elif re.match(r"^\[.+?\]", obs):
            tag_match = re.match(r"^(\[.+?\])\s*(.*)", obs)
            new_entries.append(f"- {tag_match.group(1)} {today} — {tag_match.group(2)}")
        else:
            new_entries.append(f"- {obs}")
    insert_text = "\n".join(new_entries)

    pattern = r"(\n## Dependencies)"
    return re.sub(pattern, f"\n{insert_text}\n\\g<1>", content, count=1)


def write_track(
    name: str,
    state: str = None,
    in_progress: str = None,
    blocked: str = None,
    next_step: str = None,
    observations: list = None,
    title: str = None,
) -> Path:
    """Update a track file's Status and/or append Observations. Returns the path."""
    root = get_project_root()
    tracks_dir = root / "obsidian" / "tracks"
    tracks_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    track_path = tracks_dir / f"{name}.md"

    if not track_path.exists():
        display_title = title or name.replace("-", " ").replace("_", " ").title()
        content = TEMPLATE.format(name=name, title=display_title, today=today)
        track_path.write_text(content, encoding="utf-8")
        print(f"✓ Created {track_path.relative_to(root)}")

    content = _read_track(track_path)

    if any(x is not None for x in [state, in_progress, blocked, next_step]):
        existing_state = re.search(r"\*\*State:\*\* (.+)", content)
        existing_ip = re.search(r"\*\*In progress:\*\* (.+)", content)
        existing_blocked = re.search(r"\*\*Blocked on:\*\* (.+)", content)
        existing_next = re.search(r"\*\*Next:\*\* (.+)", content)

        status_block = _build_status_block(
            state=state or (existing_state.group(1) if existing_state else "active"),
            in_progress=in_progress or (existing_ip.group(1) if existing_ip else "(not started)"),
            blocked=blocked or (existing_blocked.group(1) if existing_blocked else "(nothing)"),
            next_step=next_step or (existing_next.group(1) if existing_next else "(to be defined)"),
            today=today,
        )
        content = _replace_status(content, status_block)

    if observations:
        content = _append_observations(content, observations)

    content = _update_frontmatter_date(content, today)

    track_path.write_text(content, encoding="utf-8")
    print(f"✓ Updated {track_path.relative_to(root)}")
    return track_path


def main():
    parser = argparse.ArgumentParser(description="Update a track file's Status and/or append Observations")
    parser.add_argument("name", help="Track name (e.g. agent1, rag, pipeline)")
    parser.add_argument("--state", choices=["active", "paused", "blocked", "complete"],
                        help="Track state")
    parser.add_argument("--in-progress", dest="in_progress", help="What's currently being worked on")
    parser.add_argument("--blocked", help="What's blocking progress (default: nothing)")
    parser.add_argument("--next", dest="next_step", help="Next action item")
    parser.add_argument("--observation", action="append", default=[], dest="observations",
                        metavar="TEXT", help="Observation to append (repeatable). Format: [type] description")
    parser.add_argument("--title", help="Display title (only used when creating a new track)")
    args = parser.parse_args()

    write_track(
        name=args.name,
        state=args.state,
        in_progress=args.in_progress,
        blocked=args.blocked,
        next_step=args.next_step,
        observations=args.observations,
        title=args.title,
    )


if __name__ == "__main__":
    main()
