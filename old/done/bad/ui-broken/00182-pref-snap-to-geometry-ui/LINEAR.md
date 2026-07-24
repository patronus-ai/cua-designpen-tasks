# DesignPen [preferences]: 'pref snap to geometry' fails QA — 5/5 runs report broken workflow (00182-pref-snap-to-geometry-ui)

Description:
Snap-to-geometry engages visually during a drag (pink alignment guides across matching edges, ruler badges showing the snapped coordinates) but the snapped preview is not committed on mouse release. With the drag preview visibly snapped at Y=100 and the pointer only 3px off the aligned spot, releasing the mouse drops the shape at the raw pointer-derived position (Y=103) instead of the displayed snapped position. The snap only "sticks" if the raw pointer position already equals the snapped one at release. The preference itself (Main menu > Preferences > "Snap to geometry", on by default) is fine; the bug is in the snap commit-on-drop logic.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open Main menu > Preferences and confirm "Snap to geometry" is checked (on by default).
3. Draw a rectangle and set it to exactly X=100, Y=100, W=100, H=100 in the Design panel.
4. Draw a second 100x100 square somewhere below it (e.g. at 300, 350).
5. Drag the second square upward until snap guides engage — pink alignment guides across both squares' top edges and ruler badges reading 100/200 — with the pointer a few pixels (e.g. 3px) off the exactly-aligned spot.
6. Release the mouse and check the committed Y in the Design panel.

Actual Result:
- During the drag, snap-to-geometry engages correctly: pink alignment guides appear across both squares' top/center/bottom edges and ruler badges read 100/200.
- On mouse release, the shape is committed at the raw pointer-derived position (Y=103) instead of the displayed snapped position (Y=100) — reproduced twice while the preview was visibly snapped with guides shown.
- The snap only "sticks" if released at the pixel-exact pointer position where the raw position already equals the snapped one; alignment was only achieved via that workaround.

Expected Result:
Releasing the mouse while the snapped preview and guides are showing should commit the shape at the displayed snapped position (both squares' tops level at y=100), not the raw pointer position.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2a17880b-0bff-493b-8335-f682d365808b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_651fc184-c24e-465a-b4dc-2deac964cc09.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_66a8a983-87c8-4f5c-99b0-0bd304c42ffe.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_87fe327a-64e9-4e37-ae0f-20c41e79d00e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f5549266-ffc8-4bb6-8159-a3df8921e693.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Summary of what was done and found:

1. **Snap to geometry preference**: Confirmed enabled — Main menu > Preferences shows a checkmark next to "Snap to geometry" (on by default; left untouched).
2. **First square**: Drew a rectangle and set it to exactly X=100, Y=100, W=100, H=100 (Rectangle 1).
3. **Second square**: Drew Rectangle 2 (100×100) below at (300, 350).
4. **Snap drag**: Dragged Rectangle 2 upward. During the drag, snap-to-geometry engaged correctly — pink alignment guides appeared across both squares' top/center/bottom edges and ruler badges read 100/200. Final committed state: Rectangle 2 at X=300, Y=100 — both squares' tops exactly level at y=100 (verified numerically in the Design panel).

**Problem encountered (reproducible bug)**: the snapped preview is not committed on mouse release. Twice, while the drag preview was visibly snapped at Y=100 (guides shown, ruler badges reading "100"/"200") with the pointer only 3px off the aligned spot, releasing the mouse dropped the shape at Y=103 — the raw pointer-derived position — instead of the displayed snapped position. The snap only "sticks" if you release at the pixel-exact pointer position where the raw position already equals the snapped one. I worked around it by releasing exactly at the aligned pointer coordinate, so the final result is correct (both tops at y=100), but the snap-on-drop behavior is buggy and misleading.

verdict: not-approve
```
