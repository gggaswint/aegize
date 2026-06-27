#!/usr/bin/env python3
"""Generate the animated terminal demo GIF for Aegize.

This renders every frame directly with Pillow (no external terminal recorder),
so the GIF is fully reproducible:

    pip install pillow
    python scripts/generate_demo_gif.py

Output: assets/demo.gif (~1000px wide, dark terminal theme).

The story, in ~13 seconds: an autonomous agent makes three tool calls —
a web search (allowed), an email send (approval required), and a destructive
shell command (denied) — each governed by Aegize, then the audit log is written.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- canvas / theme ---------------------------------------------------------

WIDTH = 1000
HEIGHT = 500

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
FSIZE = 23
FSIZE_BIG = 30
FSIZE_SMALL = 18

# --- layout -----------------------------------------------------------------

BAR_H = 46
X = 44                       # left margin for body text
HEADER_Y = 72
CMD1_Y, RES1_Y = 138, 174
CMD2_Y, RES2_Y = 230, 266
CMD3_Y, RES3_Y = 322, 358
AUDIT_Y = 424
RESULT_INDENT = 30           # results sit slightly indented under their command

# --- timing (milliseconds) --------------------------------------------------

TYPE_MS = 60                 # per typing tick
CHARS_PER_TICK = 2
AFTER_TYPE_MS = 260          # full command with cursor, before the verdict
RESULT_MS = 950              # verdict shown, hold
HEADER_MS = 900
AUDIT_MS = 1700
END_MS = 3400

regular = ImageFont.truetype(FONT_PATH, FSIZE)
big = ImageFont.truetype(FONT_PATH, FSIZE_BIG)
small = ImageFont.truetype(FONT_PATH, FSIZE_SMALL)


def _measure(font: ImageFont.FreeTypeFont, text: str) -> int:
    return int(font.getlength(text))


# --- status icons (drawn as vectors so no emoji font is required) -----------


def draw_check(d: ImageDraw.ImageDraw, x: int, y: int, color) -> None:
    d.line([(x + 1, y + 8), (x + 6, y + 14)], fill=color, width=3)
    d.line([(x + 6, y + 14), (x + 15, y + 2)], fill=color, width=3)


def draw_clock(d: ImageDraw.ImageDraw, x: int, y: int, color) -> None:
    d.ellipse([x, y, x + 15, y + 15], outline=color, width=2)
    cx, cy = x + 7.5, y + 7.5
    d.line([(cx, cy), (cx, y + 3)], fill=color, width=2)        # minute hand
    d.line([(cx, cy), (x + 11, cy)], fill=color, width=2)       # hour hand


def draw_cross(d: ImageDraw.ImageDraw, x: int, y: int, color) -> None:
    d.line([(x + 2, y + 2), (x + 14, y + 14)], fill=color, width=3)
    d.line([(x + 14, y + 2), (x + 2, y + 14)], fill=color, width=3)


ICONS = {"check": draw_check, "clock": draw_clock, "cross": draw_cross}


# --- frame scaffolding ------------------------------------------------------


def base_frame() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    # title bar
    d.rectangle([0, 0, WIDTH, BAR_H], fill=BAR)
    d.line([(0, BAR_H), (WIDTH, BAR_H)], fill=BORDER, width=1)
    for i, color in enumerate((DOT_RED, DOT_YELLOW, DOT_GREEN)):
        cx = 26 + i * 22
        d.ellipse([cx, BAR_H // 2 - 6, cx + 12, BAR_H // 2 + 6], fill=color)
    title = "aegize — agent session"
    d.text(((WIDTH - _measure(small, title)) // 2, 14), title, font=small, fill=DIM)
    return img


def draw_command(d: ImageDraw.ImageDraw, y: int, text: str, *, cursor: bool) -> None:
    d.text((X, y), ">", font=regular, fill=PROMPT)
    cx = X + _measure(regular, "> ")
    d.text((cx, y), text, font=regular, fill=TEXT)
    if cursor:
        bx = cx + _measure(regular, text) + 2
        d.rectangle([bx, y + 3, bx + 11, y + FSIZE + 1], fill=CURSOR)


def draw_result(d: ImageDraw.ImageDraw, y: int, icon: str, label: str, color) -> None:
    ix = X + RESULT_INDENT
    ICONS[icon](d, ix, y + 3, color)
    d.text((ix + 26, y), label, font=regular, fill=color)


# --- scene model ------------------------------------------------------------
# We accumulate committed lines; each frame redraws all of them plus the
# currently-typing command. Committed results persist on screen, so by the end
# all three verdicts are visible together.

HEADER = "# An AI agent makes three tool calls. Aegize governs each one."

COMMANDS = [
    {
        "cmd_y": CMD1_Y, "res_y": RES1_Y,
        "cmd": 'web_search("Aegize")',
        "icon": "check", "label": "Allowed", "color": GREEN,
    },
    {
        "cmd_y": CMD2_Y, "res_y": RES2_Y,
        "cmd": 'send_email(to="ceo@acme.com", …)',
        "icon": "clock", "label": "Approval required", "color": AMBER,
    },
    {
        "cmd_y": CMD3_Y, "res_y": RES3_Y,
        "cmd": 'execute_shell("rm -rf /")',
        "icon": "cross", "label": "Policy denied", "color": RED,
    },
]


def render(committed_cmds: int, typing: dict | None, show_audit: bool) -> Image.Image:
    """Render a scene frame.

    committed_cmds: how many command blocks are fully shown (cmd + verdict).
    typing: optional {index, chars} for a command being typed (no verdict yet).
    """
    img = base_frame()
    d = ImageDraw.Draw(img)
    d.text((X, HEADER_Y), HEADER, font=regular, fill=DIM)

    for i in range(committed_cmds):
        c = COMMANDS[i]
        draw_command(d, c["cmd_y"], c["cmd"], cursor=False)
        draw_result(d, c["res_y"], c["icon"], c["label"], c["color"])

    if typing is not None:
        c = COMMANDS[typing["index"]]
        draw_command(d, c["cmd_y"], c["cmd"][: typing["chars"]], cursor=True)

    if show_audit:
        d.text(
            (X, AUDIT_Y),
            "Audit log written  ->  audit.jsonl",
            font=regular,
            fill=ACCENT,
        )

    return img


def render_end() -> Image.Image:
    img = base_frame()
    d = ImageDraw.Draw(img)
    line1 = "Every AI action passed through Aegize"
    line2 = "before reaching the outside world."
    y1 = HEIGHT // 2 - 46
    d.text(((WIDTH - _measure(big, line1)) // 2, y1), line1, font=big, fill=TEXT)
    d.text(((WIDTH - _measure(big, line2)) // 2, y1 + 44), line2, font=big, fill=TEXT)
    mark = "aegize"
    d.text(((WIDTH - _measure(small, mark)) // 2, y1 + 110), mark, font=small, fill=ACCENT)
    return img


# --- build the timeline -----------------------------------------------------


def build() -> tuple[list[Image.Image], list[int]]:
    frames: list[Image.Image] = []
    durations: list[int] = []

    def add(img: Image.Image, ms: int) -> None:
        frames.append(img)
        durations.append(ms)

    # header
    add(render(0, None, False), HEADER_MS)

    for i, c in enumerate(COMMANDS):
        # type the command
        n = len(c["cmd"])
        chars = 0
        while chars < n:
            chars = min(n, chars + CHARS_PER_TICK)
            add(render(i, {"index": i, "chars": chars}, False), TYPE_MS)
        # full command, cursor blinking, brief pause
        add(render(i, {"index": i, "chars": n}, False), AFTER_TYPE_MS)
        # verdict (command now committed)
        add(render(i + 1, None, False), RESULT_MS)

    # audit log
    add(render(3, None, True), AUDIT_MS)
    # closing statement
    add(render_end(), END_MS)

    return frames, durations


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "assets" / "demo.gif"
    frames, durations = build()

    total_s = sum(durations) / 1000
    print(f"frames: {len(frames)}  duration: {total_s:.1f}s")

    # Shared palette so colours stay stable across frames (no flicker). The
    # audit frame already contains every colour (all three verdicts persist),
    # and the end frame adds the large white text.
    sample = Image.new("RGB", (WIDTH, HEIGHT * 2), BG)
    sample.paste(render(3, None, True), (0, 0))
    sample.paste(render_end(), (0, HEIGHT))
    master = sample.quantize(colors=128, method=Image.Quantize.MEDIANCUT)

    pal_frames = [f.quantize(palette=master, dither=Image.Dither.NONE) for f in frames]
    pal_frames[0].save(
        out,
        save_all=True,
        append_images=pal_frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    size_mb = out.stat().st_size / 1_000_000
    print(f"wrote {out}  ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
