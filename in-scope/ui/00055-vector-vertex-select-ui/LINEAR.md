# DesignPen [vector editing]: 'vector vertex select' fails QA — 5/5 runs report broken workflow (00055-vector-vertex-select-ui)

Description:
Arrow-key nudging of a single selected vertex in vector edit mode is broken. After entering vector edit mode (double-click a committed Pen path) and clicking exactly one vertex (it turns solid blue while the others stay hollow), pressing arrow keys does not move the selected point. Instead the keys wrongly target the whole object's Position X/Y in the Design panel, that shift is never rendered on the canvas, and it is discarded when exiting edit mode (Escape or Enter) — so the nudge has zero lasting effect. The SVG path data in the Code panel stays unchanged throughout.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P to activate the Pen tool.
3. Click 4 points on the canvas to create a path, then press Enter to commit it ("Vector 1" created).
4. Double-click the committed path to enter vector edit mode (Move/Lasso/Paint/Bend/Cut toolbar appears; all 4 vertices visible as hollow circles).
5. Click exactly one vertex so it turns solid blue while the other three remain hollow.
6. Press an arrow key a few times (e.g. Right x5 or Down x5).
7. Observe the vertex position on canvas, the SVG path data in the Code panel, and the Position X/Y fields in the Design panel.
8. Exit edit mode with Escape or Enter and observe the object's position.

Actual Result:
- The selected vertex does not move: verified at 16x zoom that its on-canvas position was pixel-identical before/after the key presses.
- The SVG path data in the Code panel stayed unchanged (`M1 71L111 1M111 1L231 81M231 81L151 201`).
- Instead of nudging the point, the app shifted the whole object's Position X/Y in the Design panel and ruler highlights (254→259, 180→185, 254→257) — a wrong target for the nudge — and even that shift was never rendered on the canvas.
- On exiting edit mode (Escape or Enter), the position reverted to the original (254, 180), so the nudge had zero lasting effect.

Expected Result:
With a single vertex selected in vector edit mode, arrow keys should nudge only that vertex, the movement should render on the canvas and update the path data, and it should persist after exiting edit mode.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_138d69f7-3379-4d05-b0b6-e45232a6eb61.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_afb597ca-919e-4909-9c10-7920337aa88e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bce82dd4-590f-4b60-844a-4c60735606e7.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d4e47e88-5e67-44f9-afd7-845b22333808.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_eded9d60-be79-4148-8e8f-9e532dd19a2d.txt`

Agent report (verbatim tail of failing run):

```
Exiting with Enter also reverted the position to X:254, Y:180 — the nudge never persisted in any form.

**Summary of what I did and found:**

1. ✅ **Pen tool & path creation**: Pressed `P`, clicked 4 points on the canvas to create a path, and committed it with Enter — "Vector 1" was created successfully.
2. ✅ **Enter vector edit mode**: Double-clicked the committed path; the vector edit toolbar (Move/Lasso/Paint/Bend/Cut) appeared and all 4 vertices became visible as hollow circles.
3. ✅ **Single vertex selection**: Clicked exactly one vertex — it turned solid blue while the other three remained hollow, confirming exactly one point was selected. (This worked reliably for the top, bottom, and right vertices across three attempts.)
4. ❌ **Arrow-key nudge**: Pressed arrow keys multiple times (Right ×5, Down ×5 in a second attempt, Right ×3 in a third attempt). In every case the selected vertex **did not move**:
   - Verified at 16× zoom that the selected vertex's on-canvas position was pixel-identical before/after the key presses.
   - The SVG path data in the Code panel stayed unchanged (`M1 71L111 1M111 1L231 81M231 81L151 201`).
   - Instead of nudging the point, the app shifted the **whole object's Position X/Y** in the Design panel and ruler highlights (254→259, 180→185, 254→257) — a wrong target for the nudge — and even that shift was never rendered on the canvas.
   - On exiting edit mode (whether via Escape or Enter), the position reverted to the original (254, 180), so the nudge had zero lasting effect.

The drawing, committing, entering vector edit mode, and single-vertex selection all worked, but the core requested behavior — nudging a single selected point with arrow keys — is broken in this app: arrow keys incorrectly target the whole shape's position, the change isn't rendered, and it's discarded on exit, leaving the point (and shape) unmoved.

verdict: not-approve
```
