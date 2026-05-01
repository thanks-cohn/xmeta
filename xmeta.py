#!/usr/bin/env python3
"""
xmeta — Metadata sidecars for files and folders

A local-first CLI for attaching meaning to files and directories using plain JSON sidecars.

Supported commands:
  xmeta tag <path> tag1,tag2
  xmeta note <path> "note text"
  xmeta summary <path> "summary text"
  xmeta custom <path> <field_name> "value"
  xmeta custom-many <path> <field_name> "value", "value", "value"
  xmeta rts <path> "rts structure"
  xmeta rts-many <path> "rts structure", "rts structure"
  xmeta show <path>
  xmeta sidecar <path>
  xmeta init <path>

Sidecar rules:
  file.png      -> file.png.xmeta.json
  directory/    -> directory/.xmeta.json

No database. No cloud. No hidden state.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


SIDECAR_SUFFIX = ".xmeta.json"
DIRECTORY_SIDECAR = ".xmeta.json"


DEFAULT_SCHEMA: Dict[str, Any] = {
    "tags": [],
    "notes": [],
    "summaries": [],
    "custom": {},
    "rts": [],
}


class XMetaError(Exception):
    """User-facing xmeta error."""


def sidecar_path(target: Path) -> Path:
    """Return the correct sidecar path for a file or directory."""
    target = target.expanduser()

    if target.exists() and target.is_dir():
        return target / DIRECTORY_SIDECAR

    if str(target).endswith("/"):
        return target / DIRECTORY_SIDECAR

    return target.with_name(target.name + SIDECAR_SUFFIX)


def empty_metadata() -> Dict[str, Any]:
    """Return a fresh metadata document."""
    return json.loads(json.dumps(DEFAULT_SCHEMA))


def load_metadata(target: Path) -> Dict[str, Any]:
    """Load metadata from sidecar, creating an empty in-memory document if needed."""
    spath = sidecar_path(target)

    if not spath.exists():
        return empty_metadata()

    try:
        with spath.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise XMetaError(f"Invalid JSON in sidecar: {spath}\n{exc}") from exc

    if not isinstance(data, dict):
        raise XMetaError(f"Sidecar must contain a JSON object: {spath}")

    return normalize_metadata(data)


def normalize_metadata(data: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure all expected top-level fields exist with safe types."""
    normalized = empty_metadata()
    normalized.update(data)

    if not isinstance(normalized.get("tags"), list):
        normalized["tags"] = []
    if not isinstance(normalized.get("notes"), list):
        normalized["notes"] = []
    if not isinstance(normalized.get("summaries"), list):
        normalized["summaries"] = []
    if not isinstance(normalized.get("custom"), dict):
        normalized["custom"] = {}
    if not isinstance(normalized.get("rts"), list):
        normalized["rts"] = []

    return normalized


def save_metadata(target: Path, data: Dict[str, Any]) -> Path:
    """Write metadata to the sidecar file."""
    spath = sidecar_path(target)
    spath.parent.mkdir(parents=True, exist_ok=True)

    with spath.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return spath


def split_values(raw: str) -> List[str]:
    """
    Split comma-separated CLI values while respecting quotes.

    Examples:
      portrait,reference -> ["portrait", "reference"]
      "red, gold", "black" -> ["red, gold", "black"]
    """
    if raw is None:
        return []

    reader = csv.reader([raw], skipinitialspace=True)
    values = next(reader, [])
    return [value.strip() for value in values if value.strip()]


def add_unique(items: List[str], values: List[str]) -> None:
    """Append values to a list without duplicating existing entries."""
    seen = set(items)
    for value in values:
        if value not in seen:
            items.append(value)
            seen.add(value)


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.path)
    data = load_metadata(target)
    spath = save_metadata(target, data)
    print(f"initialized: {spath}")
    return 0


def cmd_tag(args: argparse.Namespace) -> int:
    target = Path(args.path)
    data = load_metadata(target)
    add_unique(data["tags"], split_values(args.tags))
    spath = save_metadata(target, data)
    print(f"updated tags: {spath}")
    return 0


def cmd_note(args: argparse.Namespace) -> int:
    target = Path(args.path)
    data = load_metadata(target)
    note = args.note.strip()
    if note:
        data["notes"].append(note)
    spath = save_metadata(target, data)
    print(f"added note: {spath}")
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    target = Path(args.path)
    data = load_metadata(target)
    summary = args.summary.strip()
    if summary:
        data["summaries"].append(summary)
    spath = save_metadata(target, data)
    print(f"added summary: {spath}")
    return 0


def cmd_custom(args: argparse.Namespace) -> int:
    target = Path(args.path)
    data = load_metadata(target)
    data["custom"][args.field_name] = args.value
    spath = save_metadata(target, data)
    print(f"set custom field: {spath}")
    return 0


def cmd_custom_many(args: argparse.Namespace) -> int:
    target = Path(args.path)
    data = load_metadata(target)
    data["custom"][args.field_name] = split_values(args.values)
    spath = save_metadata(target, data)
    print(f"set custom list field: {spath}")
    return 0


def validate_rts(raw: str) -> None:
    """
    Lightweight RTS validation.

    This MVP preserves RTS as text. It does not fully parse/render the tree yet.
    It only catches obviously empty structures and unbalanced quotes.
    """
    if not raw or not raw.strip():
        raise XMetaError("RTS structure cannot be empty.")

    quote_count = raw.count('"')
    if quote_count % 2 != 0:
        raise XMetaError("RTS structure has unbalanced quotes.")


def cmd_rts(args: argparse.Namespace) -> int:
    target = Path(args.path)
    validate_rts(args.structure)
    data = load_metadata(target)
    add_unique(data["rts"], [args.structure.strip()])
    spath = save_metadata(target, data)
    print(f"added rts: {spath}")
    return 0


def cmd_rts_many(args: argparse.Namespace) -> int:
    target = Path(args.path)
    structures = split_values(args.structures)
    for structure in structures:
        validate_rts(structure)

    data = load_metadata(target)
    add_unique(data["rts"], structures)
    spath = save_metadata(target, data)
    print(f"added rts structures: {spath}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    target = Path(args.path)
    data = load_metadata(target)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


def cmd_sidecar(args: argparse.Namespace) -> int:
    target = Path(args.path)
    print(sidecar_path(target))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="xmeta",
        description="Attach meaning to files and folders using plain JSON sidecars.",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create or normalize a sidecar")
    p.add_argument("path")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("tag", help="add comma-separated tags")
    p.add_argument("path")
    p.add_argument("tags", help="example: portrait,reference")
    p.set_defaults(func=cmd_tag)

    p = sub.add_parser("note", help="add a note")
    p.add_argument("path")
    p.add_argument("note")
    p.set_defaults(func=cmd_note)

    p = sub.add_parser("summary", help="add a summary")
    p.add_argument("path")
    p.add_argument("summary")
    p.set_defaults(func=cmd_summary)

    p = sub.add_parser("custom", help="set a single custom field")
    p.add_argument("path")
    p.add_argument("field_name")
    p.add_argument("value")
    p.set_defaults(func=cmd_custom)

    p = sub.add_parser("custom-many", help="set a multi-value custom field")
    p.add_argument("path")
    p.add_argument("field_name")
    p.add_argument("values", help='example: "red, gold", black')
    p.set_defaults(func=cmd_custom_many)

    p = sub.add_parser("rts", help="add one RTS structure")
    p.add_argument("path")
    p.add_argument("structure")
    p.set_defaults(func=cmd_rts)

    p = sub.add_parser("rts-many", help="add multiple RTS structures")
    p.add_argument("path")
    p.add_argument("structures")
    p.set_defaults(func=cmd_rts_many)

    p = sub.add_parser("show", help="print metadata JSON")
    p.add_argument("path")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("sidecar", help="print sidecar path")
    p.add_argument("path")
    p.set_defaults(func=cmd_sidecar)

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return args.func(args)
    except XMetaError as exc:
        print(f"xmeta error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
