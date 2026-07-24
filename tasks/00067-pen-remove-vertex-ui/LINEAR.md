# DesignPen [vector editing]: 'pen remove vertex' fails QA — 5/5 runs report broken workflow (00067-pen-remove-vertex-ui)

Description:
With the Pen tool active on a committed path in vector edit mode, clicking an existing middle anchor point does not remove that point. Instead the app starts drawing a new segment from the clicked anchor (a rubber-band preview line follows the cursor, Figma-style "extend from node" behavior), so the path never simplifies. This reproduced on multiple anchors and clicks that landed precisely on the nodes (they highlighted on hover). The edit toolbar's "More" menu offers no delete-point alternative (only Shape Builder and Variable Width).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool.
3. Click 5 points to draw a zigzag at canvas coordinates (100,300), (160,200), (220,300), (280,200), (340,300) (use the rulers to map canvas to screen coordinates).
4. Press Enter to commit the path — a "Vector 1" layer is created and the app remains in vector edit mode (Move/Lasso/Paint/Bend/Cut toolbar) with the Pen still active.
5. With the pen active, click one of the middle anchor points (e.g. the bottom anchor at (220,300)); confirm the click lands on the anchor (it highlights on hover).
6. Observe the canvas and the path data (Code panel SVG output).

Actual Result:
- Instead of deleting the clicked point, the app starts drawing a new segment from that anchor — a rubber-band preview line follows the cursor from the clicked node ("extend from node" behavior). Reproduced on the middle bottom anchor at (220,300) twice and the first peak at (160,200) once.
- No point is ever removed and the path never simplifies; after cancelling each unwanted segment with Escape, the SVG output shows the path still has all 5 original points.
- The edit toolbar's "More" menu offers only Shape Builder and Variable Width — no delete-point option.

Expected Result:
With the Pen tool active on the path in edit mode, clicking an existing middle anchor point should remove that point and simplify the path.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_034977db-ef5b-4939-a7dc-87a103b43978.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_89948b01-a020-4847-84b9-86a9faed9405.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a5d3c01f-5c94-4262-86f9-3d85b40c2467.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_afaff85f-0210-4509-9c7a-6a7400de1294.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c3d6b8b5-cd35-4c2d-9f86-794795261a78.txt`

Agent report (verbatim tail of failing run):

```
Here's a summary of what happened:

**What worked:**
1. **Pen tool (P)** — activated successfully via the keyboard shortcut.
2. **Drawing the zigzag** — I clicked the 5 points at canvas coordinates (100,300), (160,200), (220,300), (280,200), (340,300) (using the rulers to map canvas→screen; I corrected a 1px rounding offset by setting X=100 in the panel afterward). The path rendered as the expected "W" zigzag.
3. **Commit** — pressing Enter committed the path: a "Vector 1" layer was created (verified in the Code panel as a 240×100 path: `M1 101 L61 1 … L241 101`, i.e., exactly the 5 requested anchors), and the app remained in vector edit mode (Move/Lasso/Paint/Bend/Cut toolbar) with the Pen still active — exactly the state the task describes.

**What failed:**
4. **Clicking a middle anchor to remove it** — this does not work. With the pen active in edit mode, I clicked the middle bottom anchor at (220,300) twice and the first peak at (160,200) once (all clicks landed precisely on the anchors — they highlighted on hover). In every case, instead of deleting the point, the app **started drawing a new segment from that anchor** (a rubber-band preview line followed the cursor from the clicked node, Figma-style "extend from node" behavior). No point was ever removed and the path never simplified. I pressed Escape after each attempt to cancel the unwanted segment, and verified via the SVG output that the path still has all 5 original points. I also checked the edit toolbar's "More" menu — it only offers Shape Builder and Variable Width, no delete-point option.

So the drawing and committing steps succeeded, but the final required behavior — pen-click on a middle anchor removing the point and simplifying the path — is broken in this app; the pen initiates a new edge from the anchor instead of deleting it.

verdict: not-approve
```
