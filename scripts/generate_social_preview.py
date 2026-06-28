#!/usr/bin/env python3
"""Generate the Aegize social preview image (GitHub / LinkedIn / X).

Simple, dark, no clutter: the logo, the tagline, and the website. 1280x640 —
GitHub's recommended social-preview size, and a clean 2:1 for link cards.

    pip install pillow
    python scripts/generate_social_preview.py            # assets/social-preview.png
"""

from __future__ import annotations

from pathlib import Path

from aegize_term import ACCENT, BG, DIM, TEXT, font
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
W, H = 1280, 640
TAGLINE = "Infrastructure for autonomous AI agents."
URL = "aegize.com"


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cx = W // 2

    # logo (white mark on transparent)
    logo = Image.open(ROOT / "assets" / "logo-dark.png").convert("RGBA")
    lw = 280
    lh = round(logo.height * (lw / logo.width))
    logo = logo.resize((lw, lh), Image.LANCZOS)
    logo_top = 168
    img.paste(logo, ((W - lw) // 2, logo_top), logo)

    # thin accent rule
    rule_w = 84
    rule_y = logo_top + lh + 40
    d.line([(cx - rule_w // 2, rule_y), (cx + rule_w // 2, rule_y)], fill=ACCENT, width=3)

    # tagline
    tag_font = font(40)
    tw = int(tag_font.getlength(TAGLINE))
    d.text((cx - tw // 2, rule_y + 26), TAGLINE, font=tag_font, fill=TEXT)

    # website
    url_font = font(24)
    uw = int(url_font.getlength(URL))
    d.text((cx - uw // 2, rule_y + 92), URL, font=url_font, fill=DIM)

    out = ROOT / "assets" / "social-preview.png"
    img.save(out)
    print(f"wrote {out}  ({W}x{H}, {out.stat().st_size / 1000:.0f} KB)")


if __name__ == "__main__":
    main()
