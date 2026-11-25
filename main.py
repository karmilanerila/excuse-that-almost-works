#!/usr/bin/env python3
"""The Excuse That Almost Works.

Writes the one line a gamer texts the boss to skip work during
GTA 6 launch week, to /output/entry.txt.

The angle: a dead access badge. It is the most boring, most checkable
workplace detail there is -- badges really do die after a security
update, facilities really does take days to reissue one, and the
manager can verify it with one phone call. That is exactly why it
almost works: the only suspicious thing about it is the timing, and
the timing is the whole joke. No dead grandmother, no flat tyre, no
sudden fever, no wild story -- just a badge, a security update, and a
Thursday that happens to fall in launch week.
"""

import os
import sys

EXCUSE = (
    "My badge stopped working after the security update "
    "and facilities can't reissue one until Thursday"
)

MAX_WORDS = 20
MIN_CHARS = 1
MAX_CHARS = 140


def normalise(line):
    """Trim surrounding whitespace so the file holds exactly the text.

    A stray space at either end costs a byte in the tie-break (smaller
    text wins ties) and reads like a draft, not a hurried text.
    """
    return line.strip()


def check_line(line):
    """Check the excuse against the competition gate before writing."""
    if not line or line.strip() == "":
        return "line is empty or only whitespace"
    if "\n" in line or "\r" in line:
        return "line must be a single line"
    chars = len(line.encode("utf-8"))
    if chars < MIN_CHARS or chars > MAX_CHARS:
        return "line must be %d to %d characters, got %d" % (
            MIN_CHARS,
            MAX_CHARS,
            chars,
        )
    words = line.split()
    if len(words) > MAX_WORDS:
        return "line must be at most %d words, got %d" % (
            MAX_WORDS,
            len(words),
        )
    return None


def main():
    line = normalise(EXCUSE)
    problem = check_line(line)
    if problem is not None:
        print("invalid excuse: %s" % problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "wb") as handle:
        handle.write(line.encode("utf-8"))
    os.chmod(path, 0o644)

    with open(path, "rb") as handle:
        written = handle.read().decode("utf-8")
    problem = check_line(written)
    if problem is not None or written != line:
        print("verify failed after write: %s" % problem, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
