#!/usr/bin/env python3
"""
Turn a raw photo into a signature-ready headshot.

Takes any photo and produces `assets/headshot.png`:
  - center-cropped to a square
  - masked into a circle with TRANSPARENT corners (stays round even in Outlook,
    which ignores CSS border-radius)
  - sized to 240x240 with anti-aliased edges

Usage:
    python3 assets/make_headshot.py path/to/your-photo.jpg
    # or, if you saved it as assets/headshot-raw.jpg, just:
    python3 assets/make_headshot.py
"""

import os
import sys
from PIL import Image, ImageDraw, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "headshot.png")
SIZE = 240          # output size in px (displayed at 96px, so this is ~2.5x retina)
SUPERSAMPLE = 4     # render mask larger then downscale for smooth edges


def find_input():
    if len(sys.argv) > 1:
        return sys.argv[1]
    for name in ("headshot-raw.jpg", "headshot-raw.jpeg", "headshot-raw.png",
                 "headshot-raw.heic", "photo.jpg", "photo.png"):
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            return p
    sys.exit(
        "No input photo found.\n"
        "  Drop your photo in as assets/headshot-raw.jpg, or pass a path:\n"
        "  python3 assets/make_headshot.py /path/to/photo.jpg"
    )


def main():
    src = find_input()
    img = Image.open(src)
    img = ImageOps.exif_transpose(img)          # respect phone rotation
    img = img.convert("RGB")

    # center-crop to a square
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))

    # resize up for supersampled mask, then build circular alpha
    big = SIZE * SUPERSAMPLE
    img = img.resize((big, big), Image.LANCZOS)

    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big, big), fill=255)

    out = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    out = out.resize((SIZE, SIZE), Image.LANCZOS)
    out.save(OUT)
    print(f"Wrote {OUT}  ({os.path.getsize(OUT)} bytes, {SIZE}x{SIZE}, circular)")


if __name__ == "__main__":
    main()
