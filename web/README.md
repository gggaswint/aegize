# aegize.com

The marketing/home site for [Aegize](https://github.com/gggaswint/aegize) —
infrastructure for autonomous AI agents.

Built with **Next.js 15** (App Router) · **React 19** · **TypeScript** ·
**Tailwind CSS v4**. Dark-mode first, responsive, accessible, fully static
(no runtime server), and dependency-light. Animations are CSS-only — no
animation libraries.

## Runtime sandbox

An interactive, **local-only** simulation of the Aegize runtime. A visitor picks
a tool and watches the action flow through the pipeline (Identity → Policy →
Permissions → Approval → Execution → Audit), ending in `Executed`, `Waiting for
human approval`, or `Blocked by policy`, with an audit entry for every attempt.

It is purely a frontend simulation: **no real shell commands, emails, payments,
or API calls are executed, and there is no backend.** All state is local.

- On the homepage as the **"Try the runtime"** section (`#try-the-runtime`).
- As standalone pages at **`/playground`** and **`/sandbox`**.
- Components live in `src/components/sandbox/` (`RuntimeSandbox`, `ToolButton`,
  `PipelineStage`, `AuditLog`, `DecisionBadge`); the data model is in
  `src/lib/sandbox.ts`.

## Develop

```bash
cd web
npm install
npm run dev          # http://localhost:3000
```

## Build

```bash
npm run build        # static export -> ./out
```

The site is a fully static export (`output: "export"`), so `out/` is plain
HTML/CSS/JS and can be served by any static host or CDN.

## Deploy to Cloudflare Pages (via GitHub)

This site lives in the `web/` subdirectory of the repository. In the Cloudflare
dashboard: **Workers & Pages → Create → Pages → Connect to Git**, pick the
`gggaswint/aegize` repo, then set:

| Setting | Value |
| --- | --- |
| Framework preset | **Next.js (Static HTML Export)** |
| Root directory | `web` |
| Build command | `npm run build` |
| Build output directory | `out` |

Add one environment variable so Cloudflare uses a current Node:

| Variable | Value |
| --- | --- |
| `NODE_VERSION` | `22` |

Save and deploy. Every push to `main` will rebuild and publish. To use the
custom domain, add **aegize.com** under the project's **Custom domains** tab.

> No adapter is required — because the site is a static export, Cloudflare just
> serves the `out/` directory.

## Project structure

```
web/
├── src/
│   ├── app/
│   │   ├── layout.tsx      # fonts, metadata, background, skip link
│   │   ├── page.tsx        # section composition
│   │   ├── globals.css     # design tokens, atmosphere, motion
│   │   └── icon.png        # favicon
│   ├── components/         # Hero, RuntimePipeline, Features, ... 
│   └── lib/links.ts        # shared URLs
└── public/                 # demo.gif, logomark.png, og.png
```
