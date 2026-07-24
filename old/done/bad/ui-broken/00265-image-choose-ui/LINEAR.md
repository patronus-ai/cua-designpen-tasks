# DesignPen [image handling]: 'image choose' fails QA — 4/4 runs report broken workflow (00265-image-choose-ui)

Description:
The image picker in the fill paint panel's Image tab is non-functional: clicking the "Choose Image" button produces no file chooser dialog, no in-app picker, and no image ever loads — the preview stays empty and the shape remains without a fill image. Every alternative entry point is equally dead: the "Place image..." menu item and its Shift+K shortcut do nothing, and the "Image/video" shape tool does nothing. There is no other image source in the app (paint panel Libraries tab shows "No paint styles", Assets/Tools panels are empty, File menu has no image import option), so choosing/uploading a picture as a shape's fill is impossible.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Rectangle tool from the bottom toolbar and drag on the canvas to draw a rectangle.
3. Click the fill color swatch in the right-hand Design panel to open the fill paint panel (paint popover with tabs: solid, gradient, pattern, image, video, waves).
4. Switch to the Image tab (panel shows fit-mode dropdown Fill/Fit/Crop/Tile, a "Choose Image" picker area, and adjustment sliders).
5. Click the "Choose Image" button to choose/upload a picture (png/jpg/webp).
6. If nothing happens, also try the "Place image..." menu item, its Shift+K shortcut, and the "Image/video" shape tool.

Actual Result:

- Clicking the "Choose Image" button repeatedly (by coordinates and by element reference, with waits up to 10 seconds) does nothing: no file chooser dialog, no in-app picker, no image loaded; the preview stays empty and the rectangle remains without a fill image.
- "Place image..." menu item and its Shift+K shortcut: nothing happens.
- The "Image/video" shape tool: nothing happens.
- No alternative source exists: paint panel Libraries tab shows "No paint styles"; Assets/Tools panels are empty; File menu has no image import option; no internet access in the environment.

Expected Result:
Clicking the "Choose Image" button (or "Place image..." / the Image/video tool) should open a picker that lets the user choose/upload a png/jpg/webp picture, which then loads as the shape's image fill.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_17dc0b88-c6bc-4ccd-bbc5-e0bf824dc249.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1cb5b66e-10db-44e1-ad6b-d337acf25031.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2914e53a-4cae-4caf-be66-b3e8bd8ca5f0.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c7517e13-a02d-4b66-be61-53eacfcfe09a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e33f1035-4758-483f-a107-2f69e3f70f17.txt`

Agent report (verbatim tail of failing run):

```
I completed the flow as far as the app allowed, but hit a hard blocker at the final step. Here's a summary:

**What worked:**
1. ✅ **Drew a rectangle** — selected the Rectangle tool from the bottom toolbar and dragged on the canvas, creating "Rectangle 1" (300×200 at position 204,200).
2. ✅ **Opened its fill paint panel** — clicked the fill color swatch in the right-hand Design panel; the paint popover opened with fill-type tabs (solid, gradient, pattern, image, video, waves).
3. ✅ **Switched to the Image tab** — the panel correctly switched to image-fill mode, showing the fit-mode dropdown (Fill/Fit/Crop/Tile — which opens fine), a "Choose Image" picker area, and adjustment sliders (Exposure, Contrast, Saturation, etc.). The Fill entry in the sidebar now shows type "Image".

**What failed:**
4. ❌ **The image picker button does nothing.** I clicked the "Choose Image" button repeatedly (by coordinates and by element reference, with waits up to 10 seconds) — no file chooser dialog, no in-app picker, and no image ever loaded; the preview stays empty and the rectangle remains without a fill image. I also tried every alternative path to confirm it wasn't just me:
   - "Place image..." menu item and its Shift+K shortcut → nothing happens
   - The "Image/video" shape tool → nothing happens
   - Paint panel "Libraries" tab → "No paint styles"; Assets/Tools panels → empty; File menu → no image import option
   - No internet access in the environment, so no external image workaround exists

Everything up to the picker works, but clicking the image picker button never opens any chooser or uploads anything, so the picture could not be chosen/uploaded as the shape's fill. The task's final and essential step is blocked by this non-functional image picker.

verdict: not-approve
```
