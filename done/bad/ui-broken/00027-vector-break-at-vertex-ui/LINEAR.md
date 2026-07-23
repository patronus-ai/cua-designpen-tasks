# DesignPen [vector editing]: 'vector break at vertex' fails QA — 4/5 runs report broken workflow (00027-vector-break-at-vertex-ui)

Description:
The core feature under test — Alt+Delete breaking a closed path open at a selected corner vertex in vector edit mode — works, but the surrounding vector-editing infrastructure is broken. Undo (Ctrl+Z) after a committed vector point-move produces an inconsistent state: path data is re-normalized but the shape's position/bounds are not reverted, so geometry renders outside its bounding box, and repeated undo never reverts the move. Additionally, the Code/Inspect panel's generated SVG emits an identical closed path (with `Z`) for both the closed and the visibly broken-open triangle and does not refresh during vector editing, and arrow-key nudging of a selected vector point does nothing.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool; click 3 points (apex, bottom-right, bottom-left), then click the first point to close the triangle; press Enter to commit.
3. Double-click the triangle to enter vector edit mode.
4. Click one corner vertex (e.g. the apex) to select it, then press Alt+Delete to break the outline open at that corner; exit edit mode to commit.
5. Verify the break by dragging one of the now-coincident endpoints apart, then press Ctrl+Z (repeatedly) to undo the verification drag — observe the corrupted undo state.
6. Open the Code/Inspect panel and compare the generated SVG for the closed vs. broken-open triangle.

Actual Result:

- Undo is broken for vector edits: after a verification drag was committed, "Ctrl+Z produced an inconsistent state (path data re-normalized but shape position/bounds not reverted — geometry rendered outside its bounding box), and repeated undo never reverted the point move" — the agent had to delete the triangle and redo the whole flow from scratch.
- The Code/Inspect panel emits an identical closed path (`M101 1L201 201L1 201L101 1Z`, with `Z`) for both the closed and the broken-open triangle — "it even emitted `Z` for a visibly open path" — and it does not refresh during vector editing, so the break is not reflected in the exported SVG.
- Arrow-key nudging of a selected vector point does nothing.
- The Alt+Delete break itself works: after the break the corner has two coincident endpoints and dragging one leaves a visible gap.

Expected Result:
Ctrl+Z after a committed vector edit should cleanly revert the edit (geometry, position, and bounds consistent); the Code/Inspect SVG should reflect the actual path state (an open path must not end in `Z`) and refresh during vector editing; arrow keys should nudge a selected vertex.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_19919050-9839-4eda-863c-4cbe5e34fb64.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_309ba152-df03-4c39-a298-1b59ca504ec2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5e13f9fc-b864-42dd-a48b-5342e626416e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a9fc57f8-3fff-41c5-a66c-c566062ed1f7.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d3754fc5-3de3-43e1-a151-0985668c8e1c.txt`

Agent report (verbatim tail of failing run):

```
Final state verified: Vector 1 (200×200) is committed, geometry intact, with the outline broken open at the top corner.

## Summary

**Task steps — all completed successfully:**
1. **Pen tool (P)** → clicked 3 points (apex, bottom-right, bottom-left), then clicked the first point to close the triangle; the app closed the path and ended drawing. **Committed** with Enter (object mode, 200×200 bounding box).
2. **Double-clicked** the triangle → entered vector edit mode (hatched preview, node handles, Move/Lasso/Paint/Bend/Cut toolbar).
3. **Clicked the apex corner vertex** → it highlighted solid blue (selected).
4. **Pressed Alt+Delete** → the corner was split open, then exited edit mode to commit.

**Verification (including a control experiment on a duplicate):**
- A closed triangle's corner is a single point: clicking it shows one solid node; dragging it moves both attached edges (stays closed).
- After Alt+Delete, the same corner has **two coincident endpoints**: dragging one (tested on the first attempt) separated the ends leaving a visible gap with no closing segment, and on the final artifact, clicking the apex shows an unselected twin node stacked over the selected one — confirming the outline is broken open at that corner while other corners behave normally.

**Problems hit along the way (app bugs, worked around):**
- **Undo is broken for vector edits:** after my verification drag was committed, Ctrl+Z produced an inconsistent state (path data re-normalized but shape position/bounds not reverted — geometry rendered outside its bounding box), and repeated undo never reverted the point move. I had to delete the first triangle and redo the whole flow from scratch.
- **Code/Inspect panel is misleading:** the generated SVG emits an identical closed path (`M101 1L201 201L1 201L101 1Z`, with `Z`) for both the closed and the broken-open triangle — it even emitted `Z` for a visibly open path — and it doesn't refresh during vector editing, so the break isn't reflected/preserved in the exported SVG.
- Minor: arrow-key nudging of a selected vector point does nothing.

The core feature under test (Alt+Delete breaking the outline open at a selected corner) does work, and the final document is in the requested state, but the session was not problem-free due to the undo corruption (which forced a full redo) and the misleading SVG codegen.

verdict: not-approve
```
