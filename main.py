#!/usr/bin/env python3
"""Robot Band — make.fun entry program (program/v1).

Writes one funny name for a band made of robots, plus a few words on its
hit song, to /output/entry.txt (or $OUTPUT_DIR/entry.txt).

The entry was chosen at build time from 11 candidates scored against the
judge's published brief, in its stated order (see CANDIDATES.md):
  1. funny robot band name + a few words on its hit song
  2. laugh on the first read, a real joke not pun-shaped noise
  3. hit-song line adds a second laugh and fits the band's name
  4. sounds like a band that could exist, a name you'd repeat to a friend
  5. few words, no filler, no explaining of the joke

The program is deterministic and stdlib-only. It validates the house gate
inside itself (UTF-8 text, 1-200 characters, not only whitespace, one line)
and fails loudly instead of writing a bad file. It never removes the output
directory itself: it only replaces entry.txt inside it.
"""

import os
import sys

ENTRY = (
    "The ATMs \u2014 hit single \u201cInsufficient Funds\u201d went platinum, "
    "then charged the fans $3.50 just to listen."
)


def main() -> int:
    text = ENTRY

    # Gate, checked inside the program: 1-200 Unicode code points,
    # one line, not only whitespace, valid UTF-8.
    if not (1 <= len(text) <= 200):
        print(f"gate failed: entry is {len(text)} chars, must be 1-200",
              file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("gate failed: entry must be a single line", file=sys.stderr)
        return 1
    if not text.strip():
        print("gate failed: entry is only whitespace", file=sys.stderr)
        return 1
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"gate failed: entry is not UTF-8: {exc}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    # Replace only entry.txt inside the output directory; never remove
    # the directory itself (the grader user cannot remove a root-owned
    # mount, and removing it would crash the run). Write to a temp file
    # in the same directory and atomically replace, then read the file
    # back and confirm the bytes are exactly the entry.
    path = os.path.join(out_dir, "entry.txt")
    tmp_path = os.path.join(out_dir, ".entry.txt.tmp")
    with open(tmp_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    os.replace(tmp_path, path)
    with open(path, encoding="utf-8", newline="") as fh:
        if fh.read() != text:
            print("gate failed: written file does not match entry",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
