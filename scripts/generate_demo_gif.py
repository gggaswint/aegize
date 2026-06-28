#!/usr/bin/env python3
"""Generate the animated terminal demo for Aegize (shot 7-8 of the launch video).

Renders every frame with Pillow — no external recorder — so it is fully
reproducible at any resolution:

    pip install pillow
    python scripts/generate_demo_gif.py                 # assets/demo.gif (1000px)
    python scripts/generate_demo_gif.py --width 1920    # 1080p-tall GIF
    python scripts/generate_demo_gif.py --png-sequence --width 1920 --fps 60
        # build/demo_frames/frame_00001.png ...  (lossless source for video)

The story (~12s): an autonomous agent makes three tool calls — a web search
(allowed), an email send (approval required), and a destructive shell command
(denied) — each governed by Aegize, then the audit log is written.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from aegize_term import ACCENT, AMBER, DIM, GREEN, RED, TEXT, Term, save_gif, save_png_sequence
from PIL import Image

# --- story ------------------------------------------------------------------

HEADER = "# An AI agent makes three tool calls. Aegize governs each one."

COMMANDS = [
    {"cmd": 'web_search("Aegize runtime")', "icon": "check", "label": "Allowed", "color": GREEN},
    {"cmd": 'send_email(to="ceo@acme.com", …)', "icon": "clock",
     "label": "Approval required", "color": AMBER},
    {"cmd": 'execute_shell("rm -rf /")', "icon": "cross", "label": "Policy denied", "color": RED},
]

# layout (base 1.0 scale, in px)
X, INDENT = 44, 30
HEADER_Y = 72
ROWS = [(138, 174), (230, 266), (322, 358)]   # (command_y, result_y) per call
AUDIT_Y = 424

# timing (milliseconds)
TYPE_MS, CHARS_PER_TICK = 60, 2
AFTER_TYPE_MS, RESULT_MS = 260, 950
HEADER_MS, AUDIT_MS, END_MS = 900, 1700, 3400


def build(scale: float) -> tuple[list[Image.Image], list[int]]:
    t = Term(base_w=1000, base_h=500, scale=scale)

    def render(committed: int, typing: dict | None, audit: bool) -> Image.Image:
        img, d = t.base()
        d.text((t.px(X), t.px(HEADER_Y)), HEADER, font=t.regular, fill=DIM)
        for i in range(committed):
            cy, ry = ROWS[i]
            c = COMMANDS[i]
            t.command(d, t.px(X), t.px(cy), c["cmd"])
            t.result(d, t.px(X) + t.px(INDENT), t.px(ry), c["icon"], c["label"], c["color"])
        if typing is not None:
            i = typing["index"]
            cy, _ = ROWS[i]
            t.command(d, t.px(X), t.px(cy), COMMANDS[i]["cmd"][: typing["chars"]], cursor=True)
        if audit:
            d.text((t.px(X), t.px(AUDIT_Y)), "Audit log written  ->  audit.jsonl",
                   font=t.regular, fill=ACCENT)
        return img

    def render_end() -> Image.Image:
        img, d = t.base()
        line1 = "Every AI action passed through Aegize"
        line2 = "before reaching the outside world."
        y1 = t.H // 2 - t.px(46)
        d.text(((t.W - t.measure(t.big, line1)) // 2, y1), line1, font=t.big, fill=TEXT)
        d.text(((t.W - t.measure(t.big, line2)) // 2, y1 + t.px(44)), line2, font=t.big, fill=TEXT)
        mark = "aegize"
        mx = (t.W - t.measure(t.small, mark)) // 2
        d.text((mx, y1 + t.px(110)), mark, font=t.small, fill=ACCENT)
        return img

    frames: list[Image.Image] = []
    durations: list[int] = []

    def add(img: Image.Image, ms: int) -> None:
        frames.append(img)
        durations.append(ms)

    add(render(0, None, False), HEADER_MS)
    for i, c in enumerate(COMMANDS):
        n = len(c["cmd"])
        chars = 0
        while chars < n:
            chars = min(n, chars + CHARS_PER_TICK)
            add(render(i, {"index": i, "chars": chars}, False), TYPE_MS)
        add(render(i, {"index": i, "chars": n}, False), AFTER_TYPE_MS)
        add(render(i + 1, None, False), RESULT_MS)
    add(render(3, None, True), AUDIT_MS)
    add(render_end(), END_MS)
    return frames, durations


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Render the Aegize demo terminal animation.")
    ap.add_argument("--width", type=int, help="canvas width in px (default 1000)")
    ap.add_argument("--scale", type=float, default=1.0, help="scale factor (ignored with --width)")
    ap.add_argument("--out", type=Path, default=root / "assets" / "demo.gif")
    ap.add_argument("--png-sequence", action="store_true", help="also emit a PNG sequence")
    ap.add_argument("--frames-dir", type=Path, default=root / "build" / "demo_frames")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--no-gif", action="store_true", help="skip the GIF (PNG sequence only)")
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
        print(f"  ffmpeg -framerate {args.fps} -i {args.frames_dir}/frame_%05d.png "
              f"-c:v libx264 -pix_fmt yuv420p demo.mp4")


if __name__ == "__main__":
    main()
