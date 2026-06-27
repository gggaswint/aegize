# Aegize — Launch Video Package

A complete, production-ready package for a 55–70 second launch video.
Target runtime: **~62s**. Tone: professional, developer-first, no hype, no
existential AI claims, no fear.

Every visual maps to a committed, regenerable asset (see
[Regenerating the assets](#regenerating-the-assets)).

Brand palette: background `#0d1117`, accent `#58a6ff`, allow `#3fb950`,
approval `#d29922`, deny `#f85149`. Mono font: Menlo / JetBrains Mono.

---

## 1. Script (60 seconds)

`[timecode] VISUAL — AUDIO/VO`

| Time | Visual | Voiceover |
| --- | --- | --- |
| 0:00–0:06 | Black. `AI mostly answered questions.` types in, dims; `That's changing.` appears. | "For years, AI mostly answered questions. That's changing." |
| 0:06–0:19 | Terminal. Five capabilities type in, one per ~0.4s: `execute code` / `send email` / `query databases` / `call APIs` / `move money`. | "Agents now do more than chat. They execute code. They send email. They query databases. They call APIs. They move money." |
| 0:19–0:27 | List holds and desaturates; accent line slides in: `Every one is a real action — with real consequences.` | "Every one of those is a real action, with real consequences." |
| 0:27–0:33 | List clears. Centered, accent: `Not what an agent can say — what it's allowed to do.` | "As agents get more capable, the real question isn't what they can say. It's what they're allowed to do." |
| 0:33–0:39 | Aegize logo fades up, settles to upper third; tagline types: `the runtime layer between agents and tools`. | "That's the layer most teams are missing. Aegize." |
| 0:39–0:45 | Diagram builds: `agent → [ Aegize ] → tools`; chips fade in: `identity · policy · audit`. | "Aegize sits between an agent and the tools it uses. Every action gets an identity, a policy check, and an audit record — before it runs." |
| 0:45–0:57 | Live demo. `web_search("Aegize")` → ✓ Allowed; `send_email(...)` → ⧖ Approval required; `execute_shell("rm -rf /")` → ✗ Policy denied. | "A web search — allowed. Sending email — approval required. A destructive shell command — denied." |
| 0:57–1:00 | Terminal prints `Audit log written → audit.jsonl`. | "And every decision, on the record." |
| 1:00–1:04 | End card: logo + `Infrastructure for autonomous AI agents.` + `aegize.com · github.com/gggaswint/aegize`. | "Aegize. Infrastructure for autonomous AI agents." |

---

## 2. Storyboard

```
FRAME 1 (0:00)            FRAME 2 (0:06)           FRAME 3 (0:19)
Cold-open title          Capability montage       Reframe line appears
"AI mostly answered…"    > execute code           list dims +
"That's changing."       > send email …           "real action / consequences"

FRAME 4 (0:27)           FRAME 5 (0:33)           FRAME 6 (0:39)
Thesis line              Logo reveal + tagline    Positioning diagram
"…what it's ALLOWED      AEGIZE                    agent → [Aegize] → tools
 to do."                 runtime layer…           identity · policy · audit

FRAME 7 (0:45)           FRAME 8 (0:57)           FRAME 9 (1:00)
The demo                 Audit close              End card
three calls,             "Audit log written →     logo + tagline + URLs
three verdicts           audit.jsonl"
```

Transitions: simple cuts and slow fades only. No whips, zooms, or flashes.

---

## 3. Shot list

| # | Time | Type | Source asset | On-screen text | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | 0:00–0:06 | Title card | motion graphic | "AI mostly answered questions." → "That's changing." | Mono, centered, slow fade. |
| 2 | 0:06–0:19 | Screen / motion | `assets/capability_montage.gif` | the five capabilities | Same terminal style as the demo. |
| 3 | 0:19–0:27 | Motion graphic | `assets/capability_montage.gif` (closing frames) | "Every one is a real action…" | Desaturate the list as the line lands. |
| 4 | 0:27–0:33 | Title card | motion graphic | "Not what an agent can say — what it's allowed to do." | "allowed" in accent. Let it breathe. |
| 5 | 0:33–0:39 | Logo animation | `assets/logo.png` | tagline | Scale 110%→100%, no bounce. |
| 6 | 0:39–0:45 | Motion graphic | built in editor | agent → Aegize → tools; identity · policy · audit | Nodes draw left-to-right. |
| 7 | 0:45–0:57 | Screen recording | `assets/demo.gif` or live `python examples/demo_story.py` | three calls + verdicts | The hero shot — prefer the real CLI. |
| 8 | 0:57–1:00 | Screen recording | same | "Audit log written → audit.jsonl" | Hold ~1.5s. |
| 9 | 1:00–1:04 | End card | `assets/end_card.png` | tagline + URLs | Static; reuse as thumbnail. |

---

## 4. Narration

Read calm and even — a senior engineer explaining a tool to a peer, not an
announcer. ~135 words; `[/]` marks a beat.

> For years, AI mostly answered questions. [/]
> That's changing.
>
> Agents now do more than chat. They execute code. They send email. They query
> databases. They call APIs. They move money. [/]
>
> Every one of those is a real action — with real consequences. [/]
>
> As agents get more capable, the real question isn't what they can *say*. It's
> what they're *allowed to do*. [/]
>
> That's the layer most teams are missing. **Aegize.** [/]
>
> Aegize sits between an agent and the tools it uses. Every action gets an
> identity, a policy check, and an audit record — before it runs. [/]
>
> A web search — allowed. Sending email — approval required. A destructive shell
> command — denied. [/]
> And every decision, on the record. [/]
>
> Aegize. Infrastructure for autonomous AI agents.

Delivery: land hard on *allowed / approval required / denied* and sync each to
its on-screen verdict. Slow down and drop pitch on the final line. If you use a
music bed, keep it a neutral low pad at ≈‑24 LUFS under the VO.

---

## 5. Screen recording plan

Shots 7–8 should be a **real terminal recording** — it's the credibility moment
for a developer audience. The exact story is already produced by
`examples/demo_story.py`.

**Terminal**
- App: iTerm2 or Ghostty (no powerline/plugins).
- Colors: background `#0d1117`, foreground `#e6edf3`; match the brand
  green/amber/red.
- Font: JetBrains Mono or Menlo, 18–20pt, line spacing 1.15.
- Window content 1280×720 (record at 2× → 2560×1440). Hide the tab bar; set a
  minimal prompt (`PROMPT='$ '`); session title `aegize — agent session`.

**Capture**
1. Clean prompt. Type (don't paste) `python examples/demo_story.py`, press enter.
2. Let the real output render: three calls, three verdicts, the audit trail.
3. Hold 2s on the final audit summary before cutting.

**Settings**
- Tool: QuickTime screen recording at 60fps, or asciinema + `agg` for a
  re-renderable capture.
- Record 2560×1440, deliver 1920×1080, ≥12 Mbps H.264/H.265. Shoot 3 takes; keep
  the one with the most even typing rhythm.

**Shortcut (no live recording):** drop `assets/demo.gif` onto the timeline for
shots 7–8 — or render a lossless 1080p source (see below).

**Delivery formats**
- 16:9 master (1920×1080). Also export 1:1 (1080×1080) and 9:16 (1080×1920) for
  social — the terminal crops cleanly to square; stack title cards for 9:16.
- Burn-in open captions (developer audiences watch muted); use the narration
  verbatim.

---

## Regenerating the assets

All visuals are rendered from Pillow scripts — no external recorder — so they
reproduce anywhere:

```bash
pip install pillow

# Shot 7-8 — the demo (1000px GIF used in the README)
python scripts/generate_demo_gif.py

# Shot 2-3 — the capability montage
python scripts/generate_capability_montage.py

# Shot 9 — the end card (1920x1080 PNG)
python scripts/generate_end_card.py
```

**Lossless 1080p source for video** (PNG sequence → mp4):

```bash
python scripts/generate_demo_gif.py --png-sequence --no-gif --width 1920 --fps 60
ffmpeg -framerate 60 -i build/demo_frames/frame_%05d.png \
  -c:v libx264 -pix_fmt yuv420p demo_1080p.mp4
```

`--width` sets the resolution (height scales with it); `--png-sequence` expands
the variable-duration frames into a fixed-fps sequence under `build/` (ignored
by git). The same flags work on the capability montage.

| Asset | File | Notes |
| --- | --- | --- |
| Demo animation | `assets/demo.gif` | ~1000px, ~12s, used in the README |
| Capability montage | `assets/capability_montage.gif` | shots 2–3 |
| End card | `assets/end_card.png` | 1920×1080; reuse as thumbnail |
| Logo (full-res) | `assets/logo.png` | shot 5 |
