# DesignPen [vector editing]: 'vector interior select all' fails QA — 4/4 runs report broken workflow (00038-vector-interior-select-all-ui)

Description:
In vector edit mode, clicking inside a closed shape's fill correctly selects all vertices, but then dragging from inside the fill to move the whole outline is a no-op — the app treats the pointer movement as hover (even showing segment-hover indicators mid-drag) and nothing moves. Two related bugs compound it: arrow-key nudging of the selection updates the panel/ruler readout but the change is phantom and reverts on exiting edit mode, and the selection bbox's resize handles sit exactly on the shape's vertices, so grabbing a vertex actually grabs a handle and stretches/distorts the shape. The only working path is dragging each vertex individually with nothing pre-selected.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool; click three points to draw a triangle, close it by clicking the first anchor, and commit with Enter ("Vector 1" layer created).
3. Double-click the shape to enter vector edit mode (hatched fill, anchors, Move/Lasso/Paint/Bend/Cut toolbar).
4. Click once inside the shape's fill area — all three vertices select (anchors turn solid blue).
5. Drag from inside the fill to move the whole outline a bit to the right — nothing moves.
6. Optionally press arrow keys instead, then exit edit mode — the nudged position reverts.

Actual Result:

- Dragging from inside the fill with all vertices selected is a "**no-op**: the app treated the pointer movement as hover (even showing segment-hover indicators mid-drag) and nothing moved", across many attempts (slow/fast, small/large steps, composite drag, press-wait-drag).
- Arrow-key nudging moved the selection in the panel/ruler readout, but the change was "**phantom — it reverted to X=154 upon exiting edit mode**" (both via canvas click and the explicit ✕/done button).
- With all vertices selected, the selection bbox "**resize handles sit exactly on the triangle's vertices**", so grabbing a vertex grabs a handle and stretches/distorts the shape.
- There is no live drag preview; drags only apply at mouse-release.
- Workaround that works: with nothing selected, per-vertex drags apply correctly, so each vertex can be moved individually.

Expected Result:
With all vertices selected via a fill click, dragging from inside the fill should move the entire outline as one gesture (with a live preview), and arrow-key nudges of the selection should persist after exiting edit mode; resize handles must not shadow the vertices themselves.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0da7ef23-780a-4fad-85e7-e2f3e92329b3.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3864df97-cc55-41f8-a05c-f8b4cc303214.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_52b2be45-8657-48de-b151-2314ecd027ad.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_aab5cc26-d7b7-4ba7-a3fd-c97a866b9952.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fd2fd339-5332-4ee6-91c3-079c267355c9.txt`

Agent report (verbatim tail of failing run):

```
Committed successfully. Final state verified: **X=194, Y=300, 200×150** — the triangle's outline moved exactly 40px to the right with its shape and size intact (originally X=154).

## Summary of what was done

1. **✓ Drew a closed triangle with the Pen tool (P)** — three clicks, closed it by clicking the first anchor, committed with Enter ("Vector 1" layer created, 200×150).
2. **✓ Double-clicked the shape** to enter vector edit mode (hatched fill, anchors, and the Move/Lasso/Paint/Bend/Cut toolbar appeared).
3. **✓ Clicked once inside the fill area** — this correctly selected all three vertices at once (all anchors turned solid blue).
4. **✗ Dragging the whole outline right did not work as prescribed** — I had to use a workaround:
   - Dragging from inside the fill with all vertices selected was a **no-op**: the app treated the pointer movement as hover (even showing segment-hover indicators mid-drag) and nothing moved, across many attempts (slow/fast, small/large steps, composite drag, press-wait-drag).
   - Arrow-key nudging moved the selection in the panel/ruler readout, but the change was **phantom — it reverted to X=154 upon exiting edit mode** (both via canvas click and the explicit ✕/done button).
   - With all vertices selected, the selection bbox **resize handles sit exactly on the triangle's vertices**, so grabbing a vertex actually grabbed a handle and stretched/distorted the shape (these accidental edits had to be undone).
   - There is also **no live drag preview**; drags only apply at mouse-release.
   - Working fallback: in fresh edit mode with nothing selected, true per-vertex drags do work — I dragged each of the three vertices +40px right individually, clicked the fill to re-select all vertices, and exited to commit. Final geometry matches the intent (whole outline shifted right, size unchanged).

The end result is correct, but the core prescribed interaction — select all vertices via a fill click, then drag the whole outline in one gesture — is broken in this app (drag does nothing), and I hit two additional bugs along the way (keyboard nudge changes discarded on exit, and resize handles overlapping vertices causing unintended stretches).

verdict: not-approve
```
