"""Write the active task list to obsidian/tasks/active.md."""
import argparse
import subprocess
import sys
from datetime import datetime
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


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def write_active_tasks(tasks: list, updated_at: str = None) -> Path:
    """Overwrite obsidian/tasks/active.md with the current task list. Returns written path."""
    root = get_project_root()
    tasks_file = root / "obsidian" / "tasks" / "active.md"
    updated_at = updated_at or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    tasks_file.parent.mkdir(parents=True, exist_ok=True)

    buckets = {"high": [], "medium": [], "low": [], "done": []}
    for t in tasks:
        priority = t.get("priority", "medium").lower()
        if t.get("done", False):
            buckets["done"].append(t)
        elif priority in buckets:
            buckets[priority].append(t)
        else:
            buckets["medium"].append(t)

    def render_task(t):
        area = t.get("area", "")
        tag = f"  `#{area}`" if area else ""
        checkbox = "- [x]" if t.get("done") else "- [ ]"
        return f"{checkbox} {t['text']}{tag}"

    sections = []
    for level in ("high", "medium", "low"):
        heading = f"## {level.capitalize()} Priority"
        items = buckets[level]
        body = "\n".join(render_task(t) for t in items) if items else "_none_"
        sections.append(f"{heading}\n{body}")

    done_items = buckets["done"]
    done_body = "\n".join(render_task(t) for t in done_items) if done_items else "_none_"
    sections.append(f"## Done (this session)\n{done_body}")

    content = f"""---
updated: {updated_at}
---

# Active Tasks

{chr(10).join(chr(10).join([s, ""]) for s in sections)}""".rstrip() + "\n"

    tasks_file.write_text(content, encoding="utf-8")
    print(f"✓ Saved to {tasks_file.relative_to(root)}")
    return tasks_file


def main():
    parser = argparse.ArgumentParser(description="Write active tasks to obsidian/tasks/active.md")
    parser.add_argument(
        "--task", action="append", default=[], metavar="TEXT",
        help="Task text (repeatable)"
    )
    parser.add_argument(
        "--priority", action="append", default=[], metavar="LEVEL",
        choices=["high", "medium", "low"],
        help="Priority for the preceding --task (default: medium)"
    )
    parser.add_argument(
        "--area", action="append", default=[], metavar="TAG",
        help="Area tag for the preceding --task (e.g. rag, agent1)"
    )
    parser.add_argument(
        "--done", action="append", default=[], metavar="TEXT",
        help="Completed task text (repeatable)"
    )
    args = parser.parse_args()

    tasks = []
    for i, text in enumerate(args.task):
        priority = args.priority[i] if i < len(args.priority) else "medium"
        area = args.area[i] if i < len(args.area) else ""
        tasks.append({"text": text, "priority": priority, "area": area, "done": False})

    for text in args.done:
        tasks.append({"text": text, "priority": "low", "area": "", "done": True})

    if not tasks:
        parser.error("Provide at least one --task or --done item")

    write_active_tasks(tasks)


if __name__ == "__main__":
    main()
