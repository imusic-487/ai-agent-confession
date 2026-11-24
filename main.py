#!/usr/bin/env python3
"""Write the Funniest One-Line AI Agent Confession entry to /output/entry.txt.

Reads line.txt next to this file, checks it against the competition gate
(UTF-8 text, 1-200 characters, not only whitespace, a single line), then
writes it byte for byte to /output/entry.txt. Any failure exits non-zero
with a message on stderr, so a bad line can never slip through silently.
"""

import sys
from pathlib import Path

MAX_CHARS = 200
SOURCE_NAME = "line.txt"
OUTPUT_PATH = Path("/output/entry.txt")


def load_source() -> bytes:
    """Read the entry line as raw bytes, or exit 1 if it cannot be read."""
    source = Path(__file__).resolve().parent / SOURCE_NAME
    try:
        return source.read_bytes()
    except OSError as exc:
        print(f"cannot read {SOURCE_NAME}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def gate_error(text: str) -> str | None:
    """Return why text fails the competition gate, or None if it passes."""
    if not text or text.strip() == "":
        return "entry is empty or only whitespace"
    if len(text) > MAX_CHARS:
        return f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    for char in text:
        if ord(char) < 0x20 or ord(char) == 0x7F:
            return f"entry contains a control character (U+{ord(char):04X})"
    return None


def main() -> int:
    raw = load_source()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("entry is not valid UTF-8", file=sys.stderr)
        return 1
    if (problem := gate_error(text)) is not None:
        print(f"entry rejected: {problem}", file=sys.stderr)
        return 1
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(raw)
    written = OUTPUT_PATH.read_bytes()
    if written != raw:
        print("written entry differs from source", file=sys.stderr)
        return 1
    try:
        written_text = written.decode("utf-8")
    except UnicodeDecodeError:
        print("written entry is not valid UTF-8", file=sys.stderr)
        return 1
    if (problem := gate_error(written_text)) is not None:
        print(f"written entry rejected: {problem}", file=sys.stderr)
        return 1
    print(f"wrote {len(written)} bytes / {len(text)} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
