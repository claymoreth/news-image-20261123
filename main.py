#!/usr/bin/env python3
"""news-image-20261123 v2 entry point.

Copies the finished newspaper front page (entry.png, 1024x1024, under
the 1 MiB gate; entry.jpg is the fallback if the PNG ever exceeds it)
from the repo directory to MAKEFUN_OUTPUT_DIR/entry.png.

Repo directory resolution: MAKEFUN_BOT_DIR when set, else /bot when it
holds the entry image, else this script's own directory. Output
directory: MAKEFUN_OUTPUT_DIR, default /output.

Standard library only. Deterministic: two runs write identical bytes.
"""
import os
import shutil
import sys

LIMIT = 1048576


def repo_dir():
    env = os.environ.get("MAKEFUN_BOT_DIR")
    if env:
        return env
    if os.path.exists(os.path.join("/bot", "entry.png")) or \
            os.path.exists(os.path.join("/bot", "entry.jpg")):
        return "/bot"
    return os.path.dirname(os.path.abspath(__file__))


def pick_source(directory):
    png = os.path.join(directory, "entry.png")
    if os.path.exists(png) and os.path.getsize(png) <= LIMIT:
        return png
    jpg = os.path.join(directory, "entry.jpg")
    if os.path.exists(jpg):
        return jpg
    return png


def main():
    src = pick_source(repo_dir())
    if not os.path.exists(src):
        print("entry image not found in %s" % repo_dir(), file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied %s -> %s (%d bytes)"
          % (src, dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
