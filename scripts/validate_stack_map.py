#!/usr/bin/env python3
"""Validate data/stack_map.json against content/supplements/ and content/stacks/.

Exit 0 on success, 1 on any failure. Stdlib only.
"""

import argparse
import json
import sys
from pathlib import Path


SECTION_INDEX = "_index.md"
ROOT_MARKERS = ("hugo.toml", "config.toml")


def find_root(start: Path) -> Path:
    """Walk up from `start` looking for a Hugo config file."""
    cur = start.resolve()
    candidates = [cur] + list(cur.parents)
    for parent in candidates:
        for marker in ROOT_MARKERS:
            if (parent / marker).exists():
                return parent
    raise SystemExit(
        f"could not locate {' or '.join(ROOT_MARKERS)} walking up from {start}"
    )


def list_slugs(directory: Path) -> set:
    """Return slugs (filename stem) of .md files in `directory`, excluding _index."""
    if not directory.is_dir():
        raise SystemExit(f"missing directory: {directory}")
    out = set()
    for p in directory.iterdir():
        if p.is_file() and p.suffix == ".md" and p.name != SECTION_INDEX:
            out.add(p.stem)
    return out


def validate(root: Path) -> int:
    map_path = root / "data" / "stack_map.json"
    supp_dir = root / "content" / "supplements"
    stack_dir = root / "content" / "stacks"

    problems = []

    if not map_path.exists():
        print(f"FAIL: missing map file: {map_path}", file=sys.stderr)
        return 1

    try:
        raw = map_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"FAIL: {map_path} is not valid JSON: {e}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print(
            f"FAIL: {map_path} must contain a JSON object at top level "
            f"(got {type(data).__name__})",
            file=sys.stderr,
        )
        return 1

    supplements = list_slugs(supp_dir)
    stacks = list_slugs(stack_dir)

    for key, value in data.items():
        if key not in supplements:
            problems.append(
                f"key '{key}' has no matching supplement file "
                f"({supp_dir / (key + '.md')})"
            )
        if not isinstance(value, list):
            problems.append(
                f"key '{key}' value must be a list, got {type(value).__name__}"
            )
            continue
        if not value:
            problems.append(f"key '{key}' has an empty stack list")
            continue
        for entry in value:
            if not isinstance(entry, str):
                problems.append(
                    f"key '{key}' has non-string stack entry: {entry!r}"
                )
                continue
            if entry not in stacks:
                problems.append(
                    f"key '{key}' references missing stack '{entry}' "
                    f"(no {stack_dir / (entry + '.md')})"
                )

    mapped = set(data.keys())
    missing_coverage = sorted(supplements - mapped)
    for slug in missing_coverage:
        problems.append(
            f"coverage gap: supplement '{slug}' has no entry in stack_map.json "
            f"({supp_dir / (slug + '.md')})"
        )

    keys = list(data.keys())
    sorted_keys = sorted(keys)
    if keys != sorted_keys:
        for i, (actual, expected) in enumerate(zip(keys, sorted_keys)):
            if actual != expected:
                problems.append(
                    f"keys not sorted alphabetically; "
                    f"first deviation at index {i}: '{actual}' should be '{expected}'"
                )
                break

    if problems:
        print(f"FAIL: {len(problems)} problem(s) in {map_path}:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    total_refs = sum(len(v) for v in data.values())
    unique_stacks = {e for v in data.values() for e in v}
    print(f"OK: {map_path}")
    print(f"  supplements covered:    {len(data)} / {len(supplements)}")
    print(f"  total stack references: {total_refs}")
    print(f"  unique stacks used:     {len(unique_stacks)} / {len(stacks)}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Project root (default: walk up from this script for hugo.toml/config.toml).",
    )
    args = parser.parse_args()

    root = (
        args.root.resolve()
        if args.root is not None
        else find_root(Path(__file__).resolve().parent)
    )
    return validate(root)


if __name__ == "__main__":
    raise SystemExit(main())
