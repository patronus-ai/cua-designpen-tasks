# DesignPen [strokes]: 'stroke weight edit' fails QA — 4/5 runs report broken workflow (00287-stroke-weight-edit-ui)

Description:
The stroke weight input in the right-hand Design panel renders with a collapsed, near-zero width — it appears only as a thin sliver next to the Weight label, so a typed value is not visible in the field. The panel content is also truncated/overflowing horizontally: labels like "Stroke"/"Position" get clipped and numeric fields such as W/H/opacity are cut off. The edit itself works functionally (typing 8 and pressing Enter applies `border: 8px solid #000`, confirmed via the Code tab), but the field had to be located via the accessibility tree and the value verified in the Code tab because the panel rendering is broken.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Ellipse tool from the shape dropdown and drag on the canvas to draw an ellipse.
3. Click the "+" in the Stroke section of the Design panel to add a border (black stroke).
4. Locate the stroke weight field next to the Weight label (it may only be findable via its "Stroke weight" tooltip or the accessibility tree due to its collapsed width).
5. Click the field, select the existing value, type 8, and press Enter.
6. Inspect the field in the panel and the ellipse's border (e.g. via the Code tab).

Actual Result:

- The stroke weight input renders with a collapsed, near-zero width — only a thin sliver next to the Weight label — so the typed value "8" is not visible in the field itself.
- The right-hand panel content is truncated/overflowing horizontally: labels like "Stroke"/"Position" are clipped, and numeric fields such as W/H/opacity are cut off.
- The value does apply correctly: the border visibly thickens and the Code tab confirms `border: 8px solid #000`, but the field had to be located via the accessibility tree and verified through the Code tab instead of the panel.

Expected Result:
The stroke weight field should render at a usable width in the Design panel, visibly showing its current value, with no horizontal truncation of the surrounding stroke section controls.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 completed runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_459486dd-cccb-476e-a9c6-27118e6c4eeb.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_467a43da-30ac-4402-b5c0-e6465e39f760.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6723c057-b24c-4894-99b0-78383be10492.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a9b3c336-4c73-4e2e-ad37-f80a30e7ded5.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b74b1f80-6091-46e3-8e56-f15dfc80451f.txt`

Agent report (verbatim tail of failing run):

```
All task steps were completed:

1. **Drew an ellipse** — Selected the Ellipse tool from the shape dropdown and dragged on the canvas, creating "Ellipse 1" (200×150).
2. **Added a border** — Clicked the "+" in the Stroke section, which added a black stroke to the ellipse.
3. **Typed 8 into the stroke weight field** — Clicked the stroke weight field (confirmed by its "Stroke weight" tooltip), selected the existing value, typed `8`, and pressed Enter. The ellipse's border visibly thickened, and the Code tab confirms the result: `border: 8px solid #000`.

However, I did hit a UI problem along the way: the stroke weight input in the Design panel renders with a collapsed, near-zero width (it appears only as a thin sliver next to the Weight label), so the typed value "8" is not visible in the field itself. The right-hand panel content is also truncated/overflowing horizontally (labels like "Stroke"/"Position" get clipped, and numeric fields such as W/H/opacity are cut off). I had to locate the field via the accessibility tree and verify the final value through the Code tab instead of reading it in the panel. The functionality worked (the value applied correctly as 8px), but the broken rendering of the stroke weight field is a genuine UI bug.

verdict: not-approve
```
