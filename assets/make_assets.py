#!/usr/bin/env python3
"""
Generate email-signature image assets for Eli Colman's signature.

Outputs (written next to this script, in /assets):
  - run-adp-logo.png        Static "RUN Powered by ADP" mark (final/resting frame)
  - run-adp-logo-slide.gif  Slide-in animated version of the same mark
  - headshot.png            Circular headshot PLACEHOLDER (replace with real photo)

The logo here is a clean TEXT-BASED RECREATION used as a working placeholder so the
signature renders and animates out of the box. To use the official artwork, drop the
real PNG in as `run-adp-logo.png` and re-run this script to rebuild the slide-in GIF.

Usage:
    python3 assets/make_assets.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- Brand colors (approximate ADP palette) -------------------------------
BLUE = (37, 78, 163)     # "run" + "POWERED BY"
RED = (215, 25, 32)      # "ADP"
WHITE = (255, 255, 255)
INK = (51, 51, 51)

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_BOLD_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def rounded_card(size, radius, bg=WHITE):
    """A white rounded-square card on a transparent canvas."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=bg)
    return img


def text_center(draw, cx, y, text, fnt, fill):
    l, t, r, b = draw.textbbox((0, 0), text, font=fnt)
    w = r - l
    draw.text((cx - w / 2 - l, y), text, font=fnt, fill=fill)
    return (b - t)


def build_logo(size=320):
    """Render the 'run / POWERED BY / ADP' mark on a white rounded card."""
    img = rounded_card(size, radius=int(size * 0.22))
    d = ImageDraw.Draw(img)
    cx = size / 2

    f_run = font(FONT_BOLD, int(size * 0.36))
    f_pb = font(FONT_BOLD_ITALIC, int(size * 0.085))
    f_adp = font(FONT_BOLD, int(size * 0.20))

    # "run" — large blue lowercase
    text_center(d, cx, int(size * 0.18), "run", f_run, BLUE)
    # "POWERED BY" — small blue italic, letter-spaced look
    text_center(d, cx, int(size * 0.585), "P O W E R E D  B Y", f_pb, BLUE)
    # "ADP" — red, with registered mark
    text_center(d, cx, int(size * 0.66), "ADP", f_adp, RED)
    # registered mark
    f_reg = font(FONT_BOLD, int(size * 0.06))
    l, t, r, b = d.textbbox((0, 0), "ADP", font=f_adp)
    d.text((cx + (r - l) / 2 + 4, int(size * 0.66)), "®", font=f_reg, fill=RED)

    return img


def build_slide_gif(logo, out, canvas_w=None, frames=22, hold=14):
    """
    Build a slide-in GIF: the logo enters from the left and eases into place,
    fading in as it arrives. The LAST frame is the resting state, so any client
    that freezes on the final frame still shows the complete logo.
    """
    lw, lh = logo.size
    canvas_w = canvas_w or lw
    bg = WHITE  # matches white email background -> no transparency fringing

    def ease_out(t):  # cubic ease-out
        return 1 - (1 - t) ** 3

    # Frame 0 = complete logo (very brief). Clients that freeze on the first
    # frame of a GIF (e.g. classic Outlook) then still show the finished mark.
    rest_full = Image.new("RGBA", (canvas_w, lh), bg + (255,))
    rest_full.alpha_composite(logo, (0, 0))
    images = [rest_full.convert("P", palette=Image.ADAPTIVE, colors=255)]

    for i in range(frames):
        t = ease_out(i / (frames - 1))
        # start fully off to the left (-lw), end at x=0
        x = int((-lw) * (1 - t))
        alpha = int(255 * min(1.0, t * 1.3))

        frame = Image.new("RGBA", (canvas_w, lh), bg + (255,))
        layer = logo.copy()
        # apply fade
        a = layer.split()[3].point(lambda p: int(p * alpha / 255))
        layer.putalpha(a)
        frame.alpha_composite(layer, (x, 0))
        images.append(frame.convert("P", palette=Image.ADAPTIVE, colors=255))

    # hold the final resting frame
    rest = Image.new("RGBA", (canvas_w, lh), bg + (255,))
    rest.alpha_composite(logo, (0, 0))
    rest_p = rest.convert("P", palette=Image.ADAPTIVE, colors=255)
    images.extend([rest_p] * hold)

    durations = [30] + [40] * frames + [60] * hold
    # No `loop` kwarg -> the GIF plays through exactly ONCE and then holds on the
    # final frame (the finished logo). It does not loop forever.
    images[0].save(
        out, save_all=True, append_images=images[1:],
        duration=durations, disposal=1, optimize=True,
    )


def build_headshot_placeholder(out, size=240, initials="EC"):
    """Circular placeholder so the signature renders before the real photo is added."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, size - 1, size - 1], fill=(230, 235, 244, 255))
    f = font(FONT_BOLD, int(size * 0.42))
    l, t, r, b = d.textbbox((0, 0), initials, font=f)
    d.text(((size - (r - l)) / 2 - l, (size - (b - t)) / 2 - t),
           initials, font=f, fill=BLUE)
    # thin ring
    d.ellipse([0, 0, size - 1, size - 1], outline=BLUE, width=max(2, size // 80))
    img.save(out)


def main():
    logo = build_logo(320)
    logo_path = os.path.join(HERE, "run-adp-logo.png")
    # Only generate the placeholder logo if a real one isn't already present.
    if not os.environ.get("KEEP_LOGO") or not os.path.exists(logo_path):
        logo.save(logo_path)
    else:
        logo = Image.open(logo_path).convert("RGBA")

    build_slide_gif(logo, os.path.join(HERE, "run-adp-logo-slide.gif"))
    build_headshot_placeholder(os.path.join(HERE, "headshot.png"))
    print("Wrote:")
    for f in ("run-adp-logo.png", "run-adp-logo-slide.gif", "headshot.png"):
        p = os.path.join(HERE, f)
        print(f"  {f}  ({os.path.getsize(p)} bytes)")


if __name__ == "__main__":
    main()
