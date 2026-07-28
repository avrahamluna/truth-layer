# Proposed README additions (for review — do NOT auto-merge)

Devy's viz drop. Below are the exact markdown snippets to insert into `README.md`,
with the section each belongs in. Jr + ab review, then integrate on main.

All images are committed under `docs/`. GitHub renders inline SVG in markdown
via `<img>`; the `.png` fallbacks are provided for anywhere SVG doesn't render.

---

## 1. New section after "## Case studies (why this matters)" intro paragraph

Insert this image right below the case-studies intro (before "### 1. Population mixing"):

```markdown
![What the truth layer caught](docs/case-studies.png)
```

> Using the `.png` here (not `.svg`) because GitHub's markdown image renderer is
> most reliable with PNG for detail-dense graphics. SVG is available at
> `docs/case-studies.svg` for the crisp/scalable version.

---

## 2. Replace the single image in "## Architecture" with a small gallery

Current:

```markdown
![Architecture](docs/architecture.png)
```

Proposed (keep architecture, add the two concept diagrams below it):

```markdown
![Architecture](docs/architecture.png)

Three contradictory sources go in; one reconciled, contract-governed layer
comes out, and its data-quality tests run in CI on every push. See
`docs/ARCHITECTURE.md` for the reasoning behind each decision.

**Reconciliation, visualized:**

![Intersection = trusted population](docs/population-intersection.png)

![How records become one population](docs/match-funnel.png)
```

---

## 3. Add an "Interactive demo" line near the top (after the badges/intro)

Once GitHub Pages is enabled (Settings → Pages → Deploy from branch → `main` /
`docs` folder), add:

```markdown
**▶ [Interactive demo](https://avrahamluna.github.io/truth-layer/)** —
animated walkthrough of the case studies, reconciliation, and architecture.
```

> The demo lives at `docs/index.html`, self-contained (no build step, no
> dependencies). Pages serves it directly from the `docs/` folder on `main`.

---

## Files added on branch `feat/visualizations`

| File | What |
|------|------|
| `docs/case-studies.svg` / `.png` | ① Before/after of the 3 case studies |
| `docs/population-intersection.svg` / `.png` | ② Venn: trusted population = overlap |
| `docs/match-funnel.svg` / `.png` | ③ Match-tier reconciliation funnel |
| `docs/index.html` | ④ Interactive self-contained showcase (Pages) |
| `docs/README_PATCH_PROPOSAL.md` | this file |

All figures: dark mode, palette matched to `architecture.svg`
(`#ff6b9d` red, `#4ade80` green, `#22d3ee` cyan, plus `#a855f7`/`#f59e0b` to
distinguish the three sources). All example numbers synthetic and rounded; no PII.
