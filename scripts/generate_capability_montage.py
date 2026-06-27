#!/usr/bin/env python3
"""Generate the capability montage for Aegize's launch video (shot 2-3).

An agent's growing list of real-world actions types out one line at a time,
then a closing line reframes them as consequential. Matches the demo terminal
style exactly (same module), so the two shots cut together cleanly.

    pip install pillow
    python scripts/generate_capability_montage.py                # assets/capability_montage.gif
    python scripts/generate_capability_montage.py --png-sequence --width 1920 --fps 60
"""

from __future__ import annotations

import argparse
from pathlib import Path

from aegize_term import ACCENT, Term, save_gif, save_png_sequence
from PIL import Image

CAPABILITIES = [
    "execute code",
    "send email",
    "query databases",
    "call APIs",
    "move money",
]
CLOSING = "Every one is a real action — with real consequences."

# layout (base 1.0 scale, px)
X = 44
FIRST_Y = 96
ROW_H = 54
CLOSING_GAP = 40

# timing (ms)
TYPE_MS, CHARS_PER_TICK = 55, 2
AFTER_LINE_MS = 240
CLOSING_MS, HOLD_MS = 2400, 1400


def build(scale: float) -> tuple[list[Image.Image], list[int]]:
    t = Term(base_w=1000, base_h=460, scale=scale, title="agent — session")

    def render(committed: int, typing: dict | None, closing: bool) -> Image.Image:
        img, d = t.base()
        for i in range(committed):
            t.command(d, t.px(X), t.px(FIRST_Y + i * ROW_H), CAPABILITIES[i])
        if typing is not None:
            i = typing["index"]
            t.command(d, t.px(X), t.px(FIRST_Y + i * ROW_H),
                      CAPABILITIES[i][: typing["chars"]], cursor=True)
        if closing:
            y = t.px(FIRST_Y + len(CAPABILITIES) * ROW_H + CLOSING_GAP)
            d.text((t.px(X), y), CLOSING, font=t.regular, fill=ACCENT)
        return img

    frames: list[Image.Image] = []
    durations: list[int] = []

    def add(img: Image.Image, ms: int) -> None:
        frames.append(img)
        durations.append(ms)

    add(render(0, None, False), 500)
    for i, line in enumerate(CAPABILITIES):
        n = len(line)
        chars = 0
        while chars < n:
            chars = min(n, chars + CHARS_PER_TICK)
            add(render(i, {"index": i, "chars": chars}, False), TYPE_MS)
        add(render(i + 1, None, False), AFTER_LINE_MS)
    add(render(len(CAPABILITIES), None, True), CLOSING_MS)
    add(render(len(CAPABILITIES), None, True), HOLD_MS)
    return frames, durations


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Render the Aegize capability montage.")
    ap.add_argument("--width", type=int, help="canvas width in px (default 1000)")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--out", type=Path, default=root / "assets" / "capability_montage.gif")
    ap.add_argument("--png-sequence", action="store_true")
    ap.add_argument("--frames-dir", type=Path, default=root / "build" / "montage_frames")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--no-gif", action="store_true")
    args = ap.parse_args()

    scale = args.width / 1000 if args.width else args.scale
    frames, durations = build(scale)
    print(f"scale {scale:.3f}  ->  {frames[0].width}x{frames[0].height}  "
          f"frames {len(frames)}  duration {sum(durations) / 1000:.1f}s")

    if not args.no_gif:
        save_gif(args.out, frames, durations)
        print(f"wrote {args.out}  ({args.out.stat().st_size / 1_000_000:.2f} MB)")

    if args.png_sequence:
        count = save_png_sequence(args.frames_dir, frames, durations, fps=args.fps)
        print(f"wrote {count} PNG frames to {args.frames_dir}/  (assemble at {args.fps} fps)")


if __name__ == "__main__":
    main()
