# DesignPen [vector editing]: 'vector cut divide' fails QA — 5/5 runs report broken workflow (00030-vector-cut-divide-ui)

Description:
The Cut subtool (X) in vector edit mode fails silently when the cut line passes exactly through the shape's corner anchor points. Dragging a cut from one corner of a closed square to the opposite corner renders the magenta cut line, but on release nothing happens — no split, no new layers, no error — and the path stays a closed square. The tool works when the line crosses segment interiors (a horizontal mid-cut splits instantly, and the diagonal succeeds when offset ~2px from the corner anchors), so the intersection logic ignores vertex intersections. This is an edge-case bug in the cut/intersection engine with no user feedback.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool; click 4 corners (e.g. 500,250 → 700,250 → 700,450 → 500,450), click the start point to close the path, and commit (Escape) — a single closed 200×200 vector.
3. Double-click the square to enter vector edit mode (Move/Lasso/Paint/Bend/Cut subtool toolbar appears).
4. Press X to activate the Cut subtool.
5. Drag a cut line exactly from the top-left corner to the bottom-right corner (through the corner anchor points) and release.
6. Optionally retry with the line extended beyond both corners while still passing exactly through them — same silent failure.

Actual Result:

- The magenta cut line renders during the drag, but on release "**nothing happened** — no split, no new layers, no error; the SVG path stayed a closed square."
- Retrying with the cut line extended beyond both corners (still passing exactly through them) also failed silently.
- Diagnostics show the tool itself works: a horizontal cut through the middle split the shape into two layers instantly, and the diagonal cut succeeded when offset ~2px from the exact corner anchor points.

Expected Result:
A cut line dragged corner-to-opposite-corner through a closed square should split it into two triangular vectors along the diagonal, the same as a cut crossing segment interiors; vertex intersections must be handled by the cut logic (or at minimum the user should get feedback instead of a silent no-op).

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_160dec0f-624a-4178-b5f0-37363d5c9616.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4f993828-c7f5-450b-a25f-a28097f67f01.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_62893e78-e6ca-45af-a7dd-6a71d398e602.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7ea71c90-81ca-4497-891e-7ec57d0746ef.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bfe6cafd-20ea-4509-9e86-d14449f714ff.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Final state: the square outline is cut along its corner-to-corner diagonal into two triangular vectors (two "Vector 1" layers with triangle icons).

**Summary of what I did and found:**

1. **Pen tool square** ✅ — Pressed P, clicked 4 corners (500,250 → 700,250 → 700,450 → 500,450), clicked the start point to close the path, and committed with Escape. Result: a single closed 200×200 vector (`M1 1L201 1L201 201L1 201L1 1Z`).

2. **Vector edit mode** ✅ — Double-clicked the square; the hatched edit overlay and the subtool toolbar (Move/Lasso/Paint/Bend/Cut) appeared.

3. **Cut subtool (X)** ✅ — Pressing X highlighted "Cut" in the toolbar.

4. **Corner-to-corner cut** ⚠️ — Dragging the cut line exactly from the top-left corner to the bottom-right corner rendered the magenta cut line correctly, but on release **nothing happened** — no split, no new layers, no error; the SVG path stayed a closed square. Retrying with the line extended beyond both corners (still passing exactly through them) also failed silently. Diagnostics confirmed the tool itself works: a horizontal cut through the middle split the shape into two layers instantly (I undid it). The diagonal cut only succeeded when offset ~2px from the exact corner anchor points — that cut split the square into two triangles along the diagonal, which is the final state I kept.

**Problem encountered:** The Cut subtool fails silently when the cut line passes exactly through the shape's corner anchor points — the literal corner-to-opposite-corner drag (the exact scenario requested) is a no-op with no user feedback. It only works if the cut line is offset slightly so it crosses segment interiors near the corners. This is an edge-case bug in the cut/intersection logic (vertex intersections are ignored).

verdict: not-approve
```
