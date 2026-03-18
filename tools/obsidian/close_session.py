"""Close a session: update track(s) + write session note + backup to git."""
import argparse
import subprocess
import sys
from pathlib import Path

from .write_track import write_track
from .write_session import write_session_note


def close_session(
    tracks: list,
    state: str = None,
    in_progress: str = None,
    blocked: str = None,
    next_step: str = None,
    observations: list = None,
    title: str = None,
    summary: str = None,
    work_done: list = None,
    decisions: list = None,
    next_steps: list = None,
    open_questions: list = None,
    tags: list = None,
    session_type: str = "development",
    status: str = "complete",
):
    """Update all named tracks then write the session note."""
    observations = observations or []
    work_done = work_done or []
    decisions = decisions or []
    next_steps = next_steps or []

    # Step 1: update every named track
    for track_name in tracks:
        write_track(
            name=track_name,
            state=state,
            in_progress=in_progress,
            blocked=blocked,
            next_step=next_step,
            observations=observations,
        )

    # Step 2: write the session note with wiki-links to all tracks
    write_session_note(
        title=title,
        summary=summary,
        work_done=work_done,
        decisions=decisions,
        next_steps=next_steps,
        open_questions=open_questions,
        tags=tags,
        tracks=tracks,
        session_type=session_type,
        status=status,
    )

    # Step 3: backup to obsidian-brain git repo
    _backup_to_git(title, tracks)


def _backup_to_git(title: str, tracks: list):
    """Commit and push obsidian-brain repo if obsidian/ is a symlink into it."""
    from .write_track import get_project_root

    obsidian_dir = get_project_root() / "obsidian"
    if not obsidian_dir.is_symlink():
        return

    target = obsidian_dir.resolve()   # e.g. ~/obsidian-brain/shawlin
    brain_root = target.parent        # e.g. ~/obsidian-brain

    if not (brain_root / ".git").exists():
        return

    project_name = target.name
    track_list = ", ".join(tracks)
    commit_msg = f"{project_name}: {title}\n\nTracks: {track_list}"

    try:
        subprocess.run(
            ["git", "add", "-A"],
            cwd=brain_root, capture_output=True, check=True,
        )
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=brain_root, capture_output=True,
        )
        if result.returncode == 0:
            return  # nothing staged

        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=brain_root, capture_output=True, check=True,
        )
        subprocess.run(
            ["git", "push"],
            cwd=brain_root, capture_output=True, check=True,
        )
        print(f"✓ Backed up to obsidian-brain")
    except subprocess.CalledProcessError as e:
        # Non-fatal — don't break session close if backup fails
        print(f"⚠ obsidian-brain backup failed: {e.stderr.decode().strip()}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Close a session: update track(s) and write session note in one step."
    )

    # Track args
    parser.add_argument(
        "--track", action="append", default=[], dest="tracks", metavar="NAME",
        help="Track(s) to update (repeatable). e.g. --track rag --track pipeline",
    )
    parser.add_argument("--state", choices=["active", "paused", "blocked", "complete"])
    parser.add_argument("--in-progress", dest="in_progress")
    parser.add_argument("--blocked", dest="blocked")
    parser.add_argument("--next", dest="next_step", metavar="TEXT")
    parser.add_argument(
        "--observation", action="append", default=[], dest="observations", metavar="TEXT",
        help="Observation to append to each track (repeatable). Format: [type] description",
    )

    # Session note args
    parser.add_argument("--title", required=True, help="Session title")
    parser.add_argument("--summary", required=True, help="One-paragraph summary")
    parser.add_argument("--work-done", nargs="+", default=[], metavar="ITEM", dest="work_done")
    parser.add_argument("--decisions", nargs="+", default=[], metavar="ITEM")
    parser.add_argument("--next-steps", nargs="+", default=[], metavar="ITEM", dest="next_steps")
    parser.add_argument("--open-questions", nargs="+", default=[], metavar="ITEM", dest="open_questions")
    parser.add_argument("--tags", nargs="+", default=[])
    parser.add_argument(
        "--session-type", default="development",
        choices=["development", "analysis", "infrastructure", "planning"],
        dest="session_type",
    )
    parser.add_argument("--status", default="complete", choices=["complete", "partial", "blocked"])

    args = parser.parse_args()

    if not args.tracks:
        print("Error: at least one --track is required.", file=sys.stderr)
        sys.exit(1)

    close_session(
        tracks=args.tracks,
        state=args.state,
        in_progress=args.in_progress,
        blocked=args.blocked,
        next_step=args.next_step,
        observations=args.observations,
        title=args.title,
        summary=args.summary,
        work_done=args.work_done,
        decisions=args.decisions,
        next_steps=args.next_steps,
        open_questions=args.open_questions,
        tags=args.tags,
        session_type=args.session_type,
        status=args.status,
    )


if __name__ == "__main__":
    main()
