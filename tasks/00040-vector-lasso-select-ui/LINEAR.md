# DesignPen [vector editing]: 'vector lasso select' fails QA — 5/5 runs report broken workflow (00040-vector-lasso-select-ui)

Description:
After lasso-selecting vertices in vector edit mode, the natural gesture of grabbing one of the caught anchor points to drag the whole selection does not move the selection together. The lasso's selection rectangle has invisible resize handles on its edges/corners, and since extreme points always lie on that rectangle, grabbing them triggers a resize instead of a translate (dragging the middle valley point moved only it; dragging a peak moved only the two peaks). Additionally, dragging a selected segment silently inserts an extra anchor point (bend behavior) and clears the selection. The group-drag only succeeded via that accidental interior anchor, which was the only caught anchor not coinciding with a resize handle.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool; draw a wavy zigzag line with 5 points, e.g. (480,350), (560,280), (640,350), (720,280), (800,350); commit with Enter and exit to object mode ("Vector 1" layer created).
3. Double-click the line to re-enter vector edit mode (Move/Lasso/Paint/Bend/Cut subtool bar with anchors visible).
4. Press Q to activate the Lasso subtool and drag a freehand loop around the middle points — they select (filled blue with a selection rectangle) while the endpoints stay unselected.
5. Grab one of the caught anchor points and drag downward, expecting the whole selection to move together.

Actual Result:

- Grabbing a caught anchor point "does **not** move the caught points together" — the selection rectangle's invisible resize handles coincide with the extreme points, so "grabbing them triggered a *resize* instead: dragging the middle valley point moved only it, and dragging a peak moved only the two peaks (valley pinned)". Several drags had to be aborted; one left a 3px distortion requiring Ctrl+Z.
- Attempting to drag a selected segment silently "**inserted an extra anchor point** (bend behavior) and cleared the selection"; that extra collinear point remains in the path. Only this accidental interior point made the group-drag work at all.
- Minor: the Code/Inspect SVG panel shows stale data until selection changes, and arrow-key nudging of selected points does nothing.

Expected Result:
With multiple vertices lasso-selected, dragging any caught anchor point should translate the entire selection together; resize handles must not silently hijack drags that start on selected anchor points, and segment drags should not insert anchors or clear the selection as a side effect.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_35abbfbc-c87f-4d9c-8ea7-ad83c48c7abc.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_52e9b37f-fc61-4c85-b223-4e83d74f86f4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_793a9069-e7fd-434c-aabd-3e586e732153.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7f28c510-9207-4ebb-b114-689bd801e7f0.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fc75214a-9987-4f3b-b421-dae40f343b1b.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Final state: the wavy line's middle points have been dragged down together (endpoints pinned at their original height), confirmed both visually and by the SVG path data.

**Summary of what was done:**
1. **Pen tool (P):** Drew a wavy zigzag line with 5 points — (480,350), (560,280), (640,350), (720,280), (800,350) — and committed it with Enter, then exited to object mode (layer "Vector 1" created).
2. **Double-click:** Re-entered vector edit mode (Move/Lasso/Paint/Bend/Cut subtool bar appeared with anchors visible).
3. **Lasso (Q):** Activated the Lasso subtool and dragged a freehand elliptical loop around the middle points — they were caught (filled blue with a selection rectangle), while the endpoints stayed unselected.
4. **Drag down together:** Dragged the caught points downward ~80px in a single drag; the final SVG (`M1 1L81 11 … M161 80 …`) confirms all caught points translated down by exactly 80px together while endpoints stayed put.

**Problems encountered:**
- The natural gesture — grabbing one of the caught anchor points to drag the whole selection — does **not** move the caught points together. The lasso's selection rectangle has invisible resize handles on its edges/corners, and since extreme points always lie on that rectangle, grabbing them triggered a *resize* instead: dragging the middle valley point moved only it, and dragging a peak moved only the two peaks (valley pinned). Several drags had to be aborted, and one left a 3px distortion requiring Ctrl+Z.
- Attempting to drag a selected segment silently **inserted an extra anchor point** (bend behavior) and cleared the selection; that extra collinear point remains in the path (harmless visually, but unintended). Ironically, only this accidental interior point made the group-drag work at all, since it was the only caught anchor not coinciding with a resize handle.
- Minor: the Code/Inspect SVG panel shows stale data until selection changes, and arrow-key nudging of selected points does nothing.

So while the end result matches the task, the "drag the caught points downward together" step only succeeded via a workaround around buggy/unintuitive selection-drag behavior.

verdict: not-approve
```
