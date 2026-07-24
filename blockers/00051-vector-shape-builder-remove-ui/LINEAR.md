# DesignPen [vector editing]: 'vector shape builder remove' fails QA — 5/5 runs report broken workflow (00051-vector-shape-builder-remove-ui)

Description:
The Shape builder subtool (M) in vector edit mode never commits a fill. Hovering a closed region shows the correct pink/red region highlight and dragging shows a dashed sweep trail with a lavender region preview, but on release no fill is applied — the Fill panel in the right-hand Design panel stays empty for every interaction variant (click, slow-click, double-click, drags in all directions, multi-point scribble sweeps). As a control, the Paint subtool fills the same region instantly with one click, proving the app's region-detection/fill pipeline works — the Shape builder's commit step appears broken or unimplemented. The dependent Alt+drag "strip fill" step was consequently unreachable (and additionally the automation tooling cannot hold Alt during a drag; an attempted alt-drag moved the shape instead).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool.
3. Click corner points to draw a closed shape (e.g. a 4-point rectangle), closing on the first point.
4. Press Enter to commit the shape ("Vector 1" layer created).
5. Double-click the shape to enter vector edit mode (blue hatch overlay and the Move/Lasso/Paint/Bend/Cut/More toolbar appear).
6. Press M to activate the Shape builder subtool (checkmark "Shape builder M" in the toolbar dropdown).
7. Click inside the closed region (which highlights pink/red on hover), or drag a sweep through it, and release.
8. Check the Fill section in the right-hand Design panel.
9. (Intended follow-up, unreachable) Hold Alt and drag a sweep back over the filled area to strip the fill away.

Actual Result:
- The Shape builder never commits a fill: on release (or click, slow-click, double-click, drags inside→inside, inside→out, outside→in, across, and a multi-point scribble sweep), the Fill section remains completely empty (just the "+" button, no fill entries); the Stroke section still shows the single black stroke.
- Hover/drag feedback is correct (pink/red region highlight, dashed sweep trail, lavender region preview), but nothing lands in the scene.
- Control: the Paint subtool fills the same region instantly with one click.
- The Alt+drag strip-fill step could not be performed: there was never a Shape-builder fill to strip, and the input tooling cannot hold Alt during a drag (drag actions accept no modifier, `hold_key` rejects "alt", a bare "alt" key press types literal characters; an attempted alt-drag moved the shape instead, which was undone).

Expected Result:
Clicking or sweep-dragging with the Shape builder (M) inside a highlighted closed region should commit a fill to that region (a fill entry appears in the Fill panel), and a subsequent Alt+drag sweep back over the filled area should strip that fill away.

Estimate: XS (1 point) — likely environment/tooling limitation, verify manually and re-scope

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8e170724-b501-4d9c-aa8c-e5fd4d1b10c8.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8f0c1541-fef0-4d5a-aefc-70aebbf4b6dd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c14fd43b-d05a-4127-bb94-33b2580ad7cd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d7e92048-6e09-49b7-9f33-9caea7d320c4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ddde18aa-1600-43af-86c7-acd8a6be31df.txt`

Agent report (verbatim tail of failing run):

```
Confirmed: the Fill section remains completely empty (just the "+" button, no fill entries) after the final scribble sweep inside the region with the Shape builder active. The Stroke section still shows the single black stroke — the shape is stroke-only, exactly as before the sweep.

This completes my verification. Here's a summary of the full task attempt:

**What worked:**
1. ✅ Pressed **P** and drew a closed shape (4-point rectangle) by clicking corner points and closing on the first point — "Vector 1" layer created.
2. ✅ Committed with **Enter** — shape committed with bounding box.
3. ✅ **Double-clicked** the shape to enter vector edit mode — blue hatch overlay and the vector edit toolbar (Move, Lasso, Paint, Bend, Cut, More) appeared.
4. ✅ Pressed **M** — the Shape builder subtool activated (confirmed via the toolbar dropdown checkmark "Shape builder M" and its highlighted icon).

**What failed:**
- **The Shape builder never commits a fill.** Hovering inside the closed region correctly shows a pink/red region highlight, and dragging shows a dashed sweep trail with a lavender region preview — but on release (or click, slow-click, double-click, drags in every direction: inside→inside, inside→out, outside→in, across, and a multi-point scribble sweep), no fill is ever applied. The Fill panel stays empty every time. As a control, the **Paint** subtool fills the same region instantly with one click, proving the app's region-detection/fill pipeline works — the Shape builder's commit step appears broken or unimplemented.
- **The Alt+drag "strip fill" step could not be performed**: there was never a Shape-builder fill to strip, and additionally the available input tooling cannot hold Alt during a drag (drag actions accept no modifier, `hold_key` rejects "alt", and a bare "alt" key press types literal characters; an attempted alt-drag instead moved the shape, which I undid).

The drawing, committing, edit-mode entry, and subtool activation all behaved correctly, but the core requirement — filling the region with the Shape builder (M) and then Alt+drag-stripping that fill — was impossible to complete: Shape builder clicks/sweeps never commit a fill despite correct highlight feedback (while Paint fills fine), and the Alt-modified drag could not be synthesized.

verdict: not-approve
```
