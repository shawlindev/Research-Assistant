"""Mirror Claude memory files into obsidian/memory/ with a read-only notice prepended."""
import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

_project_root = None

_MIRROR_NOTICE_PREFIX = "> [!note] Read-only mirror"


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


def derive_memory_source(project_root: Path) -> Path:
    mangled = str(project_root).replace("/", "-")
    return Path.home() / ".claude" / "projects" / mangled / "memory"


def _already_has_notice(text: str) -> bool:
    return text.lstrip().startswith(_MIRROR_NOTICE_PREFIX)


def _prepend_notice(text: str, source_path: Path, synced_at: str) -> str:
    notice = (
        f"{_MIRROR_NOTICE_PREFIX} — source: `{source_path}` "
        f"— synced: {synced_at}\n\n"
    )
    return notice + text


def sync_memory_files(
    source_dir: Path = None,
    dest_dir: Path = None,
    verbose: bool = False,
) -> list:
    """Mirror Claude memory files into obsidian/memory/. Returns list of written paths."""
    root = get_project_root()
    source_dir = Path(source_dir) if source_dir else derive_memory_source(root)
    dest_dir = Path(dest_dir) if dest_dir else root / "obsidian" / "memory"

    if not source_dir.exists():
        print(f"! No memory directory found at {source_dir} — skipping")
        return []

    md_files = sorted(source_dir.glob("*.md"))
    if not md_files:
        print(f"! No .md files in {source_dir} — nothing to sync")
        return []

    dest_dir.mkdir(parents=True, exist_ok=True)
    synced_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    written = []

    for src_file in md_files:
        dest_file = dest_dir / src_file.name
        shutil.copy2(src_file, dest_file)
        original = dest_file.read_text(encoding="utf-8")

        if not _already_has_notice(original):
            dest_file.write_text(
                _prepend_notice(original, src_file, synced_at), encoding="utf-8"
            )
        else:
            lines = original.splitlines(keepends=True)
            lines[0] = (
                f"{_MIRROR_NOTICE_PREFIX} — source: `{src_file}` "
                f"— synced: {synced_at}\n"
            )
            dest_file.write_text("".join(lines), encoding="utf-8")

        written.append(dest_file)
        if verbose:
            print(f"  {src_file.name}")

    print(f"✓ Synced {len(written)} file(s) to {dest_dir.relative_to(root)}")
    return written


def main():
    parser = argparse.ArgumentParser(description="Mirror Claude memory files into obsidian/memory/")
    parser.add_argument("--source", default=None, help="Override source memory directory path")
    parser.add_argument("--dest", default=None, help="Override destination directory path")
    parser.add_argument("--verbose", action="store_true", help="Print each copied file")
    args = parser.parse_args()

    sync_memory_files(
        source_dir=args.source,
        dest_dir=args.dest,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
