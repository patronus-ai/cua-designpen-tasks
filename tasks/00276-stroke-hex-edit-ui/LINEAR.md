# DesignPen [strokes]: 'stroke hex edit' fails QA — 4/5 runs report broken workflow (00276-stroke-hex-edit-ui)

Description:
At the default layout in a 1280x720 viewport, the right Design panel renders extremely narrow (~135px), which completely collapses/hides the hex inputs in both the Fill and Stroke rows (the opacity value "100" is also visually truncated to "10"). Clicking where the stroke hex input should be — even targeting the element directly via the accessibility tree — focuses the Opacity field instead, because the hex input has effectively zero width. The hex-edit interaction only becomes possible after manually dragging the panel's left edge to widen it, which reveals the input. This is a layout/responsiveness bug; the hex commit itself works once the input is visible.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a 200x200 square on the canvas using the rectangle tool.
3. In the right Design panel, click the "+" in the Stroke section to add a border (initially black, Inside, weight 1).
4. Attempt to click the hex input in the stroke row and type 0000FF.
5. If the input is invisible/unclickable, drag the Design panel's left edge to widen the panel, then click the now-revealed hex input, type 0000FF, and commit.

Actual Result:

- At the default layout, the right Design panel renders ~135px wide, completely collapsing/hiding the hex inputs in both the Fill and Stroke rows; the opacity value "100" is visually truncated to "10".
- Clicking where the hex input should be (even targeting the element via the accessibility tree) focuses the Opacity field instead, since the hex input has effectively zero width.
- Only after manually widening the panel via its draggable left edge could 0000FF be typed into the stroke hex input; the value then committed (stroke swatch blue, square renders with a #0000FF border).

Expected Result:
The hex input in the stroke row should be visible and clickable at the default panel width in a 1280x720 viewport, allowing the user to type 0000FF directly without resizing the panel.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 completed runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_30e0655b-2ef4-4719-9f37-fdd4509e81eb.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3d11afd6-7cc1-401e-916f-9b93265c673f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_998944b3-cbf6-4778-9833-b8b7cef51fd1.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e62adaa7-e694-4cc5-9df0-889577ca3d7b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fdf9a24c-b188-429d-8023-62e3dd6ea8e9.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Final state confirmed:

1. **Drew a square** — Created a 200×200 rectangle on the canvas using the rectangle tool.
2. **Added a border via the Stroke section "+"** — Clicking the "+" added a stroke (initially black, Inside, weight 1).
3. **Typed 0000FF into the hex input in the stroke row** — The value committed successfully: the stroke swatch turned blue and the square now renders with a blue #0000FF border on the canvas.

However, there was a notable UI problem along the way: at the default layout in the 1280×720 viewport, the right Design panel rendered extremely narrow (~135px), which completely collapsed/hid the hex inputs in both the Fill and Stroke rows (the opacity value "100" was also visually truncated to "10"). Clicking where the hex input should be (even targeting the element directly via the accessibility tree) focused the Opacity field instead, since the hex input had effectively zero width. I could only complete the requested interaction after discovering that the panel's left edge is draggable and manually widening the panel, which revealed the hex input and allowed typing 0000FF directly into it.

So while the end goal was achieved, the hex input in the stroke row was inaccessible in the default layout — a layout/responsiveness bug that required a workaround.

verdict: not-approve
```
