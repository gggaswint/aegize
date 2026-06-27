"""Shared terminal-rendering primitives for Aegize's launch-video assets.

Every visual (the demo GIF, the capability montage, the end card) is rendered
with Pillow from these helpers, so they share one look and are fully
reproducible at any resolution. Geometry is expressed at a 1.0 scale (a 1000px
canvas) and multiplied by ``scale`` for higher-resolution output.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- brand palette ----------------------------------------------------------

BG = (13, 17, 23)            # GitHub dark canvas
BAR = (22, 27, 34)           # title bar
BORDER = (33, 38, 45)
DIM = (110, 118, 129)        # comments / secondary text
TEXT = (230, 237, 243)       # primary text
PROMPT = (63, 185, 80)       # green prompt
ACCENT = (88, 166, 255)      # aegize blue
CURSOR = (139, 148, 158)

GREEN = (63, 185, 80)
AMBER = (210, 153, 34)
RED = (248, 81, 73)

DOT_RED = (255, 95, 86)
DOT_YELLOW = (255, 189, 46)
DOT_GREEN = (39, 201, 63)

FONT_PATH = "/System/Library/Fonts/Menlo.ttc"


def font(size: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, round(size))


class Term:
    """A terminal window canvas with scale-aware chrome, text, and status icons."""

    def __init__(
        self,
        base_w: int = 1000,
        base_h: int = 500,
        scale: float = 1.0,
        title: str = "aegize — agent session",
    ) -> None:
        self.scale = scale
        self.W = round(base_w * scale)
        self.H = round(base_h * scale)
        self.title = title
        self.regular = font(23 * scale)
        self.big = font(30 * scale)
        self.small = font(18 * scale)
        self.bar_h = round(46 * scale)
        self.fsize = round(23 * scale)

    def px(self, value: float) -> int:
        return round(value * self.scale)

    def measure(self, fnt: ImageFont.FreeTypeFont, text: str) -> int:
        return int(fnt.getlength(text))

    def base(self) -> tuple[Image.Image, ImageDraw.ImageDraw]:
        img = Image.new("RGB", (self.W, self.H), BG)
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, self.W, self.bar_h], fill=BAR)
        d.line([(0, self.bar_h), (self.W, self.bar_h)], fill=BORDER, width=1)
        r = self.px(6)
        cy = self.bar_h // 2
        for i, color in enumerate((DOT_RED, DOT_YELLOW, DOT_GREEN)):
            cx = self.px(26) + i * self.px(22)
            d.ellipse([cx, cy - r, cx + 2 * r, cy + r], fill=color)
        if self.title:
            tx = (self.W - self.measure(self.small, self.title)) // 2
            d.text((tx, (self.bar_h - self.px(18)) // 2), self.title, font=self.small, fill=DIM)
        return img, d

    # -- status icons (vectors, so no emoji font is required) ----------------

    def icon(self, d: ImageDraw.ImageDraw, name: str, x: int, y: int, color) -> None:
        s = self.scale
        w = max(2, round(3 * s))
        if name == "check":
            d.line([(x + 1 * s, y + 8 * s), (x + 6 * s, y + 14 * s)], fill=color, width=w)
            d.line([(x + 6 * s, y + 14 * s), (x + 15 * s, y + 2 * s)], fill=color, width=w)
        elif name == "clock":
            d.ellipse([x, y, x + 15 * s, y + 15 * s], outline=color, width=max(2, round(2 * s)))
            cx, cy = x + 7.5 * s, y + 7.5 * s
            d.line([(cx, cy), (cx, y + 3 * s)], fill=color, width=max(2, round(2 * s)))
            d.line([(cx, cy), (x + 11 * s, cy)], fill=color, width=max(2, round(2 * s)))
        elif name == "cross":
            d.line([(x + 2 * s, y + 2 * s), (x + 14 * s, y + 14 * s)], fill=color, width=w)
            d.line([(x + 14 * s, y + 2 * s), (x + 2 * s, y + 14 * s)], fill=color, width=w)

    # -- text lines ----------------------------------------------------------

    def command(
        self, d: ImageDraw.ImageDraw, x: int, y: int, text: str, cursor: bool = False
    ) -> None:
        d.text((x, y), ">", font=self.regular, fill=PROMPT)
        cx = x + self.measure(self.regular, "> ")
        d.text((cx, y), text, font=self.regular, fill=TEXT)
        if cursor:
            bx = cx + self.measure(self.regular, text) + self.px(2)
            d.rectangle(
                [bx, y + self.px(3), bx + self.px(11), y + self.fsize + self.px(1)],
                fill=CURSOR,
            )

    def result(self, d: ImageDraw.ImageDraw, x: int, y: int, icon: str, label: str, color) -> None:
        self.icon(d, icon, x, y + self.px(3), color)
        d.text((x + self.px(26), y), label, font=self.regular, fill=color)


# --- output helpers ---------------------------------------------------------


def save_gif(
    path: Path, frames: list[Image.Image], durations: list[int], colors: int = 128
) -> None:
    """Save an animated GIF with a shared palette (no inter-frame flicker)."""
    w, h = frames[0].size
    n = len(frames)
    idxs = sorted({round(i * (n - 1) / 7) for i in range(8)} | {n - 1, n - 2})
    sample = Image.new("RGB", (w, h * len(idxs)), BG)
    for k, ix in enumerate(idxs):
        sample.paste(frames[ix], (0, h * k))
    master = sample.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    pal = [f.quantize(palette=master, dither=Image.Dither.NONE) for f in frames]
    pal[0].save(
        path,
        save_all=True,
        append_images=pal[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )


def save_png_sequence(
    out_dir: Path, frames: list[Image.Image], durations: list[int], fps: int = 60
) -> int:
    """Expand variable-duration frames into a fixed-fps PNG sequence for editing."""
    out_dir = Path(out_dir)
    if out_dir.exists():
        for p in out_dir.glob("frame_*.png"):
            p.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)
    idx = 1
    for f, ms in zip(frames, durations):
        for _ in range(max(1, round(ms / 1000 * fps))):
            f.save(out_dir / f"frame_{idx:05d}.png")
            idx += 1
    return idx - 1
