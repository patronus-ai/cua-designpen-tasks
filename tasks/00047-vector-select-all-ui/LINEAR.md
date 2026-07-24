# DesignPen [vector editing]: 'vector select all' fails QA — 4/5 runs report broken workflow (00047-vector-select-all-ui)

Description:
Two failures in vector edit mode. First, Cmd+A (Meta+A) does nothing — vertices stay hollow/unselected — while Ctrl+A does select all vertices, so select-all is simply not bound to the Cmd/Meta modifier. Second, arrow-key nudging of selected vertices is non-functional even with a valid selection: pressing Up never moves the vertices or path on canvas, only decrements the Design panel's Y value and ruler labels (a visible UI desync, e.g. panel Y=280 while the shape sits at Y=300), and the phantom value snaps back on exiting edit mode — no movement is ever applied or persisted.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool; click 6 alternating points to draw a zigzag; commit with Enter/Escape ("Vector 1" created).
3. Double-click the path to enter vector edit mode (Move/Lasso/Paint/Bend/Cut toolbar, anchor points visible).
4. Press Cmd+A to select every vertex — observe nothing selects.
5. As a diagnostic, press Ctrl+A instead — all vertices select (solid blue with a selection rectangle).
6. With all vertices selected, press the up arrow key several times.
7. Exit edit mode and check the shape's Y position.

Actual Result:

- "Cmd+A did nothing — all vertices stayed hollow (unselected)." Ctrl+A did select all vertices, "so select-all simply isn't bound to Cmd/Meta+A."
- With vertices selected (via Ctrl+A, and also with a single vertex), pressing Up repeatedly "Never moved the vertices/path on canvas — the rendered shape, anchor dots, and selection rectangle stayed frozen in place."
- It "Only decremented the panel's Y value and ruler highlight labels (e.g., panel showed Y=280 while the shape still sat at Y=300 on canvas — a visible UI desync)". It also wrongly changed the object's Y when a single bottom vertex was "moved" (height should have changed instead).
- "On exiting edit mode, the Y value snapped back to 300 — no movement was ever applied or persisted."

Expected Result:
Cmd+A in vector edit mode should select every vertex (same as Ctrl+A), and arrow keys should nudge the selected vertices on canvas with the change rendered live and persisted after exiting edit mode.

Estimate: XS (1 point) — likely environment/tooling limitation, verify manually and re-scope

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_34d9f531-c2c1-40c0-b77a-30c830a316e9.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3b0b68e3-5ccf-4091-ae8c-de9c4205494f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_468550be-d2ae-4b17-a0a9-01273bf4ce67.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9e9810e7-3dd1-4c17-92aa-e1a22c6f5bde.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c1680076-7e32-469f-8f8c-145ee4b1dc24.txt`

Agent report (verbatim tail of failing run):

```
Confirmed: after exiting edit mode, Y reverted to 300 — the nudges were completely discarded. The shape never moved.

## Summary of what happened

**Step 1 — Draw zigzag with Pen tool (P) and commit: ✅ Worked.**
I pressed P, clicked 6 alternating points to create a zigzag, and committed with Enter/Escape. "Vector 1" was created (X=154, Y=300, 350×100), and the Code panel's SVG confirmed the correct zigzag geometry (`M1 101 L71 1 L141 101 L211 1 L281 101 L351 1`).

**Step 2 — Double-click to enter vector edit mode: ✅ Worked.**
Double-clicking the path opened vector edit mode (Move/Lasso/Paint/Bend/Cut toolbar appeared, anchor points became visible).

**Step 3 — Cmd+A to select every vertex: ❌ Failed.**
Cmd+A did nothing — all vertices stayed hollow (unselected). I verified what selection looks like by clicking a vertex directly (it turns solid blue). As a diagnostic, **Ctrl+A** *did* select all vertices (all turned solid blue with a selection rectangle), so select-all simply isn't bound to Cmd/Meta+A.

**Step 4 — Up arrow to shift all vertices upward: ❌ Failed (broken even with vertices selected).**
With all vertices properly selected (via Ctrl+A), and also with a single vertex selected, pressing Up repeatedly:
- Never moved the vertices/path on canvas — the rendered shape, anchor dots, and selection rectangle stayed frozen in place.
- Only decremented the panel's Y value and ruler highlight labels (e.g., panel showed Y=280 while the shape still sat at Y=300 on canvas — a visible UI desync). It also wrongly changed the object's Y when a single *bottom* vertex was "moved" (height should have changed instead).
- On exiting edit mode, the Y value snapped back to 300 — no movement was ever applied or persisted.

The zigzag was drawn and edit mode entered successfully, but the core goal failed: Cmd+A does not select the vertices in vector edit mode, and arrow-key nudging of selected vertices is non-functional (it only corrupts the displayed position value, doesn't re-render, and reverts on exit). The path remains at its original position.

verdict: not-approve
```
