# DesignPen [canvas interactions]: 'canvas eyedropper' fails QA — 5/5 runs report broken workflow (00075-canvas-eyedropper-ui)

Description:
The eyedropper's "Click to sample" is broken: with a shape selected and the eyedropper started via the I shortcut, hovering another shape correctly shows the magnifying loupe with "#FF0000 / Click to sample", but the sampling click is not intercepted by the eyedropper. Instead it passes through to the canvas and re-targets the selection (selecting the hovered shape and deselecting the original), so the sampled color is never applied to the originally selected shape. The failure reproduced with the target locked, with the fill color picker's own eyedropper button, and with separate mousedown/mouseup events; the only working path is a multi-select workaround (select both shapes, then I + click).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw two rectangles side by side (e.g. 150x120 at X=154 and X=354).
3. Select the first rectangle and set its fill to bright red #FF0000 via the right-panel Fill controls (hex input in the color picker).
4. Select the second rectangle.
5. Press I to start the eyedropper and move the cursor over the red rectangle — the magnifying loupe appears showing "#FF0000 / Click to sample".
6. Click to sample.
7. Check the second rectangle's fill and the current selection.

Actual Result:
- Clicking to sample did not apply the color to the selected second rectangle; the click passed through to the canvas and changed the selection (selected the red Rectangle 1 instead), leaving Rectangle 2 gray. Reproduced consistently:
  - Plain click → selection jumped to Rectangle 1, no fill applied.
  - With Rectangle 1 locked → click deselected everything, no fill applied.
  - With the fill color picker open and its eyedropper button active → click closed the picker and deselected, no fill applied.
  - Separate mousedown/mouseup events → same failure.
  - Pressing Enter while the eyedropper was active unexpectedly entered vector-edit mode and converted the rectangle to a VECTOR type (recovered via Ctrl+Z).
- Workaround that succeeded: selecting both rectangles first, then pressing I and clicking on the red — the sampled #FF0000 was applied to the whole selection.

Expected Result:
With a shape selected and the eyedropper active (I), clicking on another shape should sample its color and apply it to the selected shape's fill, without changing the selection.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1f491ba1-2181-48d9-8874-d40ce1bb0438.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_300276c7-9776-420c-9103-fb95a3528e0f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b9d58da1-378e-48a7-a443-2b14beb9e3bf.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e45ccca9-718d-40ee-a29c-09f34f68d07f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_edb5458e-1945-4c81-98bd-55032450a431.txt`

Agent report (verbatim tail of failing run):

```
The task is complete in terms of final state — both rectangles are side by side and the second rectangle now carries the sampled #FF0000 fill. Here's a summary of what happened:

**What worked:**
1. ✅ Drew two 150×120 rectangles side by side (X=154 and X=354).
2. ✅ Set the first rectangle's fill to bright red #FF0000 via the right-panel Fill controls (hex input in the color picker).
3. ✅ Selected the second rectangle and pressed **I** — the eyedropper started, and hovering over the red rectangle correctly showed the magnifying loupe with "#FF0000 / Click to sample".

**What went wrong (bug):**
4. ❌ Clicking to sample did **not** apply the color to the selected second rectangle. The click passed through to the canvas and changed the selection (it selected the red Rectangle 1 instead), leaving Rectangle 2 gray. I reproduced this failure consistently:
   - Plain click → selection jumped to Rectangle 1, no fill applied
   - With Rectangle 1 locked → click deselected everything, no fill applied
   - With the fill color picker open and its eyedropper button active → click closed the picker and deselected, no fill applied
   - Separate mousedown/mouseup events → same failure
   - Pressing Enter while the eyedropper was active unexpectedly entered vector-edit mode and converted the rectangle to a VECTOR type (recovered via Ctrl+Z)
5. ⚠️ Workaround that succeeded: selecting **both** rectangles first, then pressing I and clicking on the red — the sampled #FF0000 was applied to the whole selection, turning the second rectangle red. Both fills were verified as FF0000 afterward.

The eyedropper's "Click to sample" is broken for the prescribed flow: the sampling click isn't intercepted by the eyedropper and instead re-targets the canvas selection, so the sampled color never reaches the originally selected shape. The end state was only achieved via a multi-select workaround.

verdict: not-approve
```
