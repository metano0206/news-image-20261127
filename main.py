#!/usr/bin/env python3
"""Entry for make.fun news-image-20261127.

Writes one image summing up the world news of Friday 27 November 2026 to
/output/entry.png.  The picture — the front page of *The Daily Meridian* —
is drawn by render.py at run time.  If the drawing stack (Pillow, fonts) is
unavailable in the sandbox, the identical pre-rendered entry.png stored in
this repository is copied instead, so the output bytes are the same either
way and on every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out = os.environ.get("ENTRY_OUT", "/output/entry.png")
    directory = os.path.dirname(out)
    if directory:
        os.makedirs(directory, exist_ok=True)
    try:
        sys.path.insert(0, HERE)
        import render

        render.write_image(out)
    except Exception:
        shutil.copyfile(os.path.join(HERE, "entry.png"), out)


if __name__ == "__main__":
    main()
