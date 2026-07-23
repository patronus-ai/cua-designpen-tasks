# DesignPen [strokes]: 'outline stroke' fails QA — 5/5 runs report broken workflow (00138-outline-stroke-ui)

Description:
The right-click "Outline stroke" command (also Main menu > Object > Outline stroke) executes but produces a wrong result on a rectangle with an 8px inside black stroke over a #D4D4D4 fill. The outlined ring is filled with the rectangle's fill color (#D4D4D4) instead of the stroke color (#000000), the interior fill is discarded (middle becomes transparent), and the inside-positioned stroke is outlined as if it were a center stroke (bounds grow 250x170 → 258x178 and the shape shifts position). The command entry points work; the geometry/paint conversion is what's broken. There is also a minor UI bug: the Stroke weight input in the design panel is clipped/too narrow at this viewport width, hiding its value.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the rectangle tool and drag on the canvas to draw a rectangle (e.g. 250x170 "Rectangle 1").
3. In the right-side design panel, click the Stroke section's + button to add a stroke (black, Position "Inside").
4. Click the stroke weight field and enter 8 (note: the weight input is clipped/too narrow at this viewport width — verify via the Inspect/Code tab, e.g. `border: 8px solid #000`).
5. With the rectangle selected, right-click it and choose "Outline stroke" (also available under Main menu > Object > Outline stroke).
6. Inspect the resulting "Outline stroke" vector's fill, geometry, and bounds.

Actual Result:

- The outlined stroke ring is filled with the rectangle's fill color (#D4D4D4) instead of the stroke's color (#000000) — the black stroke color is lost entirely. Resulting SVG: `<path d="M0 0L258 0L258 178L0 178L0 0ZM8 8L8 170L250 170L250 8L8 8Z" fill="#D4D4D4"/>`.
- The rectangle's interior fill is discarded — the middle is now transparent (before: gray rectangle with an 8px black border; after: a gray ring with an empty middle).
- Although the stroke position was "Inside", the outlined geometry expanded the bounds from 250x170 to 258x178 and shifted position from (254, 250) to (250, 246) — outlined as if it were a center stroke.
- Minor UI issue: the Stroke weight input is clipped/too narrow in the design panel at this viewport width, so its value isn't visible.

Expected Result:
Outline stroke should convert the stroke to a vector ring filled with the stroke's color (#000000), preserve the shape's interior fill as its own geometry, and respect the "Inside" stroke position so the visual appearance and bounds are unchanged.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_31dc7ff8-afe4-4342-99ba-1fc34a526460.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_978ae3cf-cc85-441c-9009-7fc7b9c3c97a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c8aeae3d-61d5-420f-a49b-729814abfa86.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d7925b7f-4243-4fb4-a632-67a160dd5ee2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e47a420b-3c9f-4a52-b3f8-f9249c716aa2.txt`

Agent report (verbatim tail of failing run):

```
I've completed all the steps. Here's a summary of what happened:

**Steps performed:**
1. **Drew a rectangle** — selected the rectangle tool and dragged on canvas to create a 250×170 rectangle ("Rectangle 1").
2. **Added a stroke via the Stroke section's + button** — a black stroke appeared with Position "Inside".
3. **Set weight to 8** — clicked the stroke weight field and entered 8. Verified in the Inspect/Code tab: `border: 8px solid #000`, and the canvas showed the 8px black border.
4. **Right-clicked the rectangle → "Outline stroke"** — the command executed and converted the shape into a vector named "Outline stroke". I also confirmed the command exists under Main menu > Object > Outline stroke (now grayed out there since the resulting vector no longer has a stroke, which is expected).

**Problems observed with the Outline stroke result:**
- The outlined stroke ring was filled with the rectangle's **fill color (#D4D4D4)** instead of the stroke's color (**#000000**) — the black stroke color was lost entirely. Resulting SVG: `<path d="M0 0L258 0L258 178L0 178L0 0ZM8 8L8 170L250 170L250 8L8 8Z" fill="#D4D4D4"/>`.
- The rectangle's interior fill was discarded — the middle is now transparent. So the visual appearance was not preserved (before: gray rectangle with an 8px black border; after: a gray ring with an empty middle).
- Although the stroke position was "Inside", the outlined geometry expanded the bounds from 250×170 to 258×178 and shifted position from (254, 250) to (250, 246) — i.e., it was outlined as if it were a *center* stroke.
- Minor UI issue: the Stroke weight input is clipped/too narrow in the design panel at this viewport width, so its value isn't visible; I had to set it blind and verify via the Inspect tab.

All the requested actions were executable, but the Outline stroke operation produced an incorrect result (wrong fill color on the outlined stroke, lost interior fill, and inside-stroke geometry treated as center), which changes the shape's appearance — a genuine bug in the feature.

verdict: not-approve
```
