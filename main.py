#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261126.

Copies the pre-drawn front-page poster (entry.png, in this repository)
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).

Standard library only. No network. Deterministic: both runs of the
program write the same bytes.
"""

import os
import shutil
import sys


def validate_source(src):
    """Check the bundled poster exists and looks like a PNG.

    Returns the file size in bytes. Raises SystemExit with a message
    if the source is missing or is not a PNG.
    """
    if not os.path.isfile(src):
        sys.exit("missing entry image: " + src)
    with open(src, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry image is not a PNG: " + src)
    size = os.path.getsize(src)
    if size > 1048576:
        sys.exit("entry image exceeds 1 MiB: %d bytes" % size)
    return size


def main():
    """Copy entry.png to the output directory as entry.png."""
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    size = validate_source(src)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, size))


if __name__ == "__main__":
    main()
