"""Write a session summary note to obsidian/sessions/."""
import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

_project_root = None


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


def _slugify(text: str, max_len: int = 50) -> str:
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug.strip())
    return slug[:max_len].rstrip("-")


def _unique_path(directory: Path, date_str: str, slug: str) -> Path:
    base = directory / f"{date_str}_{slug}.md"
    if not base.exists():
        return base
    n = 2
    while True:
        candidate = directory / f"{date_str}_{slug}_{n}.md"
        if not candidate.exists():
            return candidate
        n += 1


def write_session_note(
    title: str,
    summary: str,
    work_done: list,
    decisions: list,
    next_steps: list,
    open_questions: list = None,
    tags: list = None,
    tracks: list = None,
    date_str: str = None,
    session_type: str = "development",
    status: str = "complete",
) -> Path:
    """Write a session summary note to obsidian/sessions/. Returns the written path."""
    root = get_project_root()
    sessions_dir = root / "obsidian" / "sessions"

    date_str = date_str or date.today().isoformat()
    tags = tags or []
    open_questions = open_questions or []
    tracks = tracks or []

    sessions_dir.mkdir(parents=True, exist_ok=True)
    slug = _slugify(title)
    out_path = _unique_path(sessions_dir, date_str, slug)

    tags_yaml = "[" + ", ".join(tags) + "]" if tags else "[]"

    def bullet_list(items):
        return "\n".join(f"- {item}" for item in items) if items else "- (none)"

    def checkbox_list(items):
        return "\n".join(f"- [ ] {item}" for item in items) if items else "- [ ] (none)"

    questions_section = ""
    if open_questions:
        questions_section = f"\n## Open Questions\n{bullet_list(open_questions)}\n"

    tracks_section = ""
    if tracks:
        track_links = "\n".join(f"- [[{t}]]" for t in tracks)
        tracks_section = f"\n## Tracks\n{track_links}\n"

    content = f"""---
date: {date_str}
title: {title}
tags: {tags_yaml}
session_type: {session_type}
status: {status}
---

# {title} — {date_str}

## Summary
{summary}

## Work Done
{bullet_list(work_done)}

## Decisions Made
{bullet_list(decisions)}

## Next Steps
{checkbox_list(next_steps)}
{questions_section}{tracks_section}"""

    out_path.write_text(content.rstrip() + "\n", encoding="utf-8")
    print(f"✓ Saved to {out_path.relative_to(root)}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Write a session summary note to obsidian/sessions/")
    parser.add_argument("--title", required=True, help="Session title (used in filename and heading)")
    parser.add_argument("--summary", required=True, help="One-paragraph summary of what was accomplished")
    parser.add_argument("--work-done", nargs="+", default=[], metavar="ITEM", dest="work_done")
    parser.add_argument("--decisions", nargs="+", default=[], metavar="ITEM")
    parser.add_argument("--next-steps", nargs="+", default=[], metavar="ITEM", dest="next_steps")
    parser.add_argument("--open-questions", nargs="+", default=[], metavar="ITEM", dest="open_questions")
    parser.add_argument("--tags", nargs="+", default=[])
    parser.add_argument("--tracks", nargs="+", default=[], metavar="TRACK",
                        help="Track names to link (e.g. agent1 rag pipeline)")
    parser.add_argument("--date", default=None, dest="date_str", help="ISO date (default: today)")
    parser.add_argument("--session-type", default="development",
                        choices=["development", "analysis", "infrastructure", "planning"],
                        dest="session_type")
    parser.add_argument("--status", default="complete", choices=["complete", "partial", "blocked"])
    args = parser.parse_args()

    write_session_note(
        title=args.title,
        summary=args.summary,
        work_done=args.work_done,
        decisions=args.decisions,
        next_steps=args.next_steps,
        open_questions=args.open_questions,
        tags=args.tags,
        tracks=args.tracks,
        date_str=args.date_str,
        session_type=args.session_type,
        status=args.status,
    )


if __name__ == "__main__":
    main()
