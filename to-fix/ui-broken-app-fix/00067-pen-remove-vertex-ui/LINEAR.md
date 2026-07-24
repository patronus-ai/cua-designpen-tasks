# DesignPen [vector editing]: 'pen remove vertex' fails QA — 3/5 runs report broken workflow (00067-pen-remove-vertex-ui)

Description:
With the Pen tool active on a committed path in edit mode, clicking one of the path's existing anchor points is expected to remove that anchor and simplify the path. Instead, the click converts the anchor into a curved/smooth node — bézier control handles are pulled out and the path keeps all of its points, becoming more complex rather than simpler. Three independent QA runs reproduced this on freshly drawn 5-point zigzags, verified with single clicks, double clicks, and pure mouse-down/mouse-up at identical coordinates with zero movement. No alternative removal mechanism exists either: the node's right-click menu only offers object-level actions (no "delete node"/"remove anchor"), pressing Delete/Backspace on a selected node deletes the entire vector, and the path-edit sub-toolbar (Move / Lasso / Paint / Bend / Cut / More) has no node-removal tool. The remove-vertex interaction is either unimplemented or shadowed by the corner/smooth toggle.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool.
3. Click at canvas coordinates (100,300), (160,200), (220,300), (280,200), (340,300) to draw a 5-point zigzag.
4. Press Enter to commit the path ("Vector 1" is created and stays in edit mode with the pen active).
5. Click one of the middle anchor points (e.g. the valley at (220,300)).

Actual Result:

- The clicked anchor is converted into a curved/smooth node — two bézier handles appear and the corner rounds.
- The node count never decreases; the path does not simplify. Reproduced on multiple interior anchors (left peak, center, right peak).
- No fallback works: right-click on a node shows only shape-level actions (Copy/Cut/Duplicate/Delete/Flatten) with no "delete node" option; Delete/Backspace removes the entire vector; the pen dropdown offers only Pen/Pencil; "More" only contains Shape builder / Variable width.

Expected Result:
Clicking an existing anchor point with the Pen tool active in path edit mode should remove that anchor and reconnect the neighbouring segments, simplifying the path (5 points → 4 points).

Estimate: M (3 points) — pen-tool edit-mode click handler dispatches corner/smooth toggle instead of vertex removal; scoped to one interaction in the vector editor

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 3 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ffb5c77c-16d0-4bc4-9630-387feba9ef73.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_40a00491-590d-44db-aacb-b4beaded03db.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8d3cc6af-650c-4cd2-ad17-617646557c98.txt`

Agent report (verbatim tail of failing run):

```
**What did not work (the blocker):**
The required final step — "click one of its middle anchor points so that point is removed and the path simplifies" — cannot be performed in this tool. I tested this exhaustively on freshly drawn, clean paths:

- **Clicking a middle anchor point does NOT remove it.** Instead it toggles the node between corner and smooth (curved) — a bezier-handle curve is created. I reproduced this on three different interior nodes (left peak, center, right peak), including with a guaranteed-pure click (separate mouse-down/mouse-up at identical coordinates, no drag). The node count never decreases; the path does not simplify.
- **No other method removes a single node either:**
  - Selecting a node (even correctly, as a sharp corner, via the Lasso marquee) and pressing **Delete** or **Backspace** deletes the **entire vector**, not the node.
  - **Right-clicking** a node shows only a shape-level context menu (Copy/Cut/Duplicate/Delete/Flatten/etc.) with no "delete node" / "remove anchor" option.
  - The **Pen tool dropdown** offers only "Pen" and "Pencil" — no delete-anchor mode.
  - The path-edit sub-toolbar (Move / Lasso / Paint / Bend / Cut / More) has no node-removal tool, and "More" only contains Shape builder and Variable width.

So the behavior the task relies on (a click on an anchor deleting it and simplifying the path) is not how this tool behaves — clicking curves the node, and the only deletion commands available destroy the whole shape. I left the canvas with a correctly drawn and committed 5-point zigzag in edit mode (pen active), which is exactly the point at which the task breaks down.

The first two parts (draw + commit) went smoothly, but the node-removal-by-click step is broken, so the task could not be completed as described.

verdict: not-approve
```
