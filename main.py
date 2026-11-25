#!/usr/bin/env python3
"""Ship the pre-rendered invitation letter PNG.

Entry for make.fun bounty
u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

The letter PNG (1024x1024) is pre-rendered and shipped in this repo as
entry.png (drawn by draw_letter.py, kept for reference). This script is
stdlib-only on purpose: the grading environment may not have
third-party imaging libraries, so
main.py only copies entry.png to the output path. No drawing, no
third-party imports, no network, fully deterministic.

Run:  python3 main.py
Output: $ENTRY_OUTPUT or /output/entry.png
"""

import os
import shutil
import sys

OUT = os.environ.get("ENTRY_OUTPUT", "/output/entry.png")


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if not os.path.isfile(src):
        print(f"error: {src} not found", file=sys.stderr)
        return 1
    out_dir = os.path.dirname(os.path.abspath(OUT))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, OUT)
    print(f"wrote {OUT} 1024x1024")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
