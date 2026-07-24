# DesignPen [canvas interactions]: 'canvas image crop' fails QA — 4/4 runs report broken workflow (00078-canvas-image-crop-ui)

Description:
The image crop flow is doubly broken. First, no image can actually be placed in this environment: the toolbar "Image/video" tool, "Place image… (Shift+K)", and the fill popover's "Choose Image" button all fail silently (no file chooser appears in the headless browser), and pasting is blocked with the toast "Clipboard access is blocked in this browser context". Second, selecting "Crop" in the fill swatch popover's image scale-mode dropdown never starts a crop session — no crop handles, no overlay, no commit affordance — and dragging an edge handle then shrinks the shape proportionally (aspect-locked) instead of trimming one side, while Enter gives no commit feedback. A control test on a plain rectangle confirmed normal one-sided edge resizing works, so the Crop/image state itself alters resize behavior.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Try to place an image on the canvas (toolbar "Image/video" tool, "Place image… (Shift+K)", or the fill popover's "Choose Image" button); if none works, draw a rectangle (e.g. 300x250) and set its fill type to Image (the layer becomes labeled "Image").
3. Select the shape and open the fill swatch popover in the right panel.
4. Change the image scale mode dropdown to "Crop".
5. Look for crop handles / overlay on the canvas.
6. Drag one of the shape's edge handles (e.g. the left edge) inward to trim one side.
7. Press Enter to commit the crop.

Actual Result:
- Placing an image is blocked: the "Image/video" tool and "Place image… (Shift+K)" show no file chooser; the fill popover's "Choose Image" button fails silently; pasting yields the toast "Clipboard access is blocked in this browser context" (app runs on plain http) and "Copy as PNG" gives "PNG clipboard export is not available in this browser"; no library assets/paint styles, no plugins, AI features require an API key. Best workaround: a rectangle with fill type Image, which contains no bitmap and renders transparent.
- The fill swatch popover and dropdown work: "Crop" was selected and persisted across reopening.
- Selecting "Crop" never engaged a crop session: no crop handles, no overlay, no commit affordance.
- Dragging the shape's left edge handle inward shrank the shape proportionally (300x250 → 245x204 → 212x176) instead of trimming one side; a control test on a plain rectangle confirmed normal one-sided edge resizing works, so the Crop/image state altered resize behavior to aspect-locked scaling.
- Pressing Enter produced no observable commit feedback.

Expected Result:
Selecting "Crop" in the image scale-mode dropdown should start a crop session with visible crop handles; dragging a handle inward should trim only that side of the image, and Enter should commit the crop. Placing an image via the documented entry points should also work.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_41557ab2-41c6-49ba-97c3-f564f39d01b4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_48051b3a-06fc-4c5e-b8e4-4d54ab21149c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_79685bbf-c9b4-4392-9140-20a9b35dc38b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_cd6608d4-3096-484b-b394-5e0e9c2f9829.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d79762f8-0bac-4861-bd24-ed3376e1ed05.txt`

Agent report (verbatim tail of failing run):

```
Final state confirmed: Rectangle 1 (labeled "Image" in the panel, scale mode "Crop") sits at 292,237 with dimensions 212×176 (reduced from the original 300×250 by the handle drags), Enter was pressed, and the stray second browser window has been closed.

## Summary of what happened

**1. Placing an image — blocked by the environment.** Every available path failed:
- Toolbar "Image/video" tool and "Place image… (Shift+K)": no file chooser ever appears in this headless browser context; nothing is placed.
- Fill popover "Choose Image" button: same silent failure.
- Pasting an image: app toast "Clipboard access is blocked in this browser context" (app runs on plain http); "Copy as PNG" gives "PNG clipboard export is not available in this browser".
- No library assets/paint styles, no plugins, AI features require an API key.
- Best achievable workaround: a rectangle whose fill type was set to Image (the app then labels the layer "Image"), but it contains no actual bitmap and renders transparent.

**2. Fill swatch popover & dropdown — worked.** The popover opened from the Fill swatch in the right panel, and the image scale-mode dropdown was successfully changed to "Crop" (value persisted across reopening).

**3. Crop session — never engaged.** Selecting "Crop" produced no crop session: no crop handles, no overlay, no commit affordance. Dragging the shape's left edge handle inward shrank the shape **proportionally** (300×250 → 245×204 → 212×176) rather than trimming one side. A control test on a plain rectangle confirmed normal one-sided edge resizing works in the app, so the Crop/image state altered resize behavior to aspect-locked scaling instead of a one-side crop trim. Pressing Enter produced no observable commit feedback.

The task could not be completed as specified: an actual image cannot be placed in this environment (file chooser and clipboard are both unavailable), and the "Crop" dropdown selection never visibly started a crop session — no crop handles appeared, the handle drag behaved as a proportional resize instead of a one-side trim, and Enter gave no commit feedback (possibly because no real bitmap could ever be loaded into the fill).

verdict: not-approve
```
