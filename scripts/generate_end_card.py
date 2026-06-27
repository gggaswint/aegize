#!/usr/bin/env python3
"""Generate the Aegize end card for the launch video (shot 9) and social/thumbnail use.

A full-bleed dark card: the logo, the positioning line, and the URLs. Defaults to
1920x1080; pass --width/--height for other sizes (e.g. 1080x1080 for square).

    pip install pillow
    python scripts/generate_end_card.py                       # assets/end_card.png (1920x1080)
    python scripts/generate_end_card.py --width 1080 --height 1080 --out assets/end_card_square.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

from aegize_term import ACCENT, BG, DIM, TEXT, font
from PIL import Image, ImageDraw, ImageOps

TAGLINE = "Infrastructure for autonomous AI agents."
URLS = "aegize.com  ·  github.com/gggaswint/aegize"


def _prepare_logo(logo_path: Path, raw: bool) -> Image.Image:
    """Load the logo. By default convert a dark-on-light mark into a clean white
    silhouette on transparency, cropped tight, so it reads well on a dark card."""
    src = Image.open(logo_path).convert("RGBA")
    if raw:
        return src
    alpha = ImageOps.invert(src.convert("L"))   # dark mark -> opaque, light bg -> transparent
    mark = Image.new("RGBA", src.size, TEXT + (0,))
    mark.putalpha(alpha)
    bbox = alpha.getbbox()
    return mark.crop(bbox) if bbox else mark


def render(width: int, height: int, logo_path: Path, raw_logo: bool = False) -> Image.Image:
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    u = width / 1920  # scale unit relative to a 1920px-wide design

    cy = height // 2

    # logo, centered above the midline
    logo = _prepare_logo(logo_path, raw_logo)
    logo_w = round(420 * u)
    logo_h = round(logo.height * (logo_w / logo.width))
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    logo_y = cy - logo_h - round(36 * u)
    img.paste(logo, ((width - logo_w) // 2, logo_y), logo)

    # tagline
    tag_font = font(46 * u)
    tw = int(tag_font.getlength(TAGLINE))
    d.text(((width - tw) // 2, cy + round(30 * u)), TAGLINE, font=tag_font, fill=TEXT)

    # urls
    url_font = font(26 * u)
    uw = int(url_font.getlength(URLS))
    d.text(((width - uw) // 2, cy + round(110 * u)), URLS, font=url_font, fill=DIM)

    # thin accent rule under the tagline
    rule_w = round(120 * u)
    d.line(
        [((width - rule_w) // 2, cy + round(18 * u)), ((width + rule_w) // 2, cy + round(18 * u))],
        fill=ACCENT,
        width=max(2, round(3 * u)),
    )
    return img


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Render the Aegize end card.")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--logo", type=Path, default=root / "assets" / "logo.png")
    ap.add_argument("--out", type=Path, default=root / "assets" / "end_card.png")
    ap.add_argument("--raw-logo", action="store_true", help="paste the logo as-is (no silhouette)")
    args = ap.parse_args()

    img = render(args.width, args.height, args.logo, raw_logo=args.raw_logo)
    img.save(args.out)
    kb = args.out.stat().st_size / 1_000
    print(f"wrote {args.out}  ({args.width}x{args.height}, {kb:.0f} KB)")


if __name__ == "__main__":
    main()
