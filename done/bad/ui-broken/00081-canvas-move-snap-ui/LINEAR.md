# DesignPen [canvas interactions]: 'canvas move snap' fails QA — 5/5 runs report broken workflow (00081-canvas-move-snap-ui)

Description:
Smart-guide snapping on the canvas has a preview/commit mismatch: while dragging a square near another, the red smart guides appear and the drag preview visibly snaps level (ruler highlighted the snapped 300-400 range), but on mouse release the square is committed at the raw pointer position instead of the snapped one — e.g. Y=303 instead of the guide-indicated Y=300, leaving the tops 3px misaligned. The snapped position shown by the guides is not applied on drop, so users who trust the guides get misaligned results; alignment only succeeds if the raw pointer position happens to coincide exactly with the snap target.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Place two 100x100 squares on the canvas.
3. Select the first square and set its Y to exactly 300 by typing into the Y position field in the right panel.
4. Drag the second square around near the first until the red smart guides appear and it snaps level with the first (tops aligned).
5. Release the mouse (do not type the number for the second square).
6. Check the second square's committed Y in the right panel.

Actual Result:
- During the drag the red guides appeared and the preview visibly snapped level (the ruler highlighted 300-400), but on release the square was committed at Y=303 — the snapped position shown by the guides was not applied on drop, leaving the tops 3px misaligned.
- A correct result was only achieved by redoing the drag and releasing at the exact pixel where the raw pointer position coincided with Y=300.

Expected Result:
When the red smart guides show a snapped alignment during a drag, releasing the mouse should commit the shape at the snapped position (tops exactly level), matching the preview.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_36e202d8-78dd-47a8-9231-71fef409edaa.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_46af3de1-1488-4dbb-b550-eda6780380db.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_70404083-1034-450e-a8d0-ded660cede00.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9a5c61ec-85a5-4082-835c-aa3ef5460756.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fd50c421-c2d1-4f11-9328-5d4ca9c31373.txt`

Agent report (verbatim tail of failing run):

```
Both squares are now confirmed in their final state:
- **Rectangle 1**: X=154, Y=300, 100×100 (Y was set to exactly 300 by typing into the Y position field)
- **Rectangle 2**: X=294, Y=300, 100×100 (positioned by dragging with the red smart guides showing top/middle/bottom alignment, no numbers typed)

The tops of both squares are level at Y=300.

**Summary of how it went:** Placing the squares and typing Y=300 for the first one worked fine. However, I hit a real bug with the smart-guide snapping: on my first drag of the second square, the red guides appeared and the preview visibly snapped level (the ruler highlighted 300–400 during the drag), but when I released the mouse the square was committed at Y=303 — the snapped position shown by the guides was not applied on drop, leaving the tops 3px misaligned. I had to redo the drag and release at the exact pixel where the raw pointer position coincided with Y=300 to get a truly level result. The end state is correct, but the snap-on-release behavior is broken (preview/commit mismatch), which would mislead users who trust the guides.

verdict: not-approve
```
