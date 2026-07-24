# DesignPen [image handling]: 'image adjustments' fails QA — 5/5 runs report broken workflow (00264-image-adjustments-ui)

Description:
No picture can be loaded into an image fill in this environment, which blocks the image-adjustments workflow. The "Choose Image" button in the fill paint panel's Image tab, the "Place image… (Shift+K)" menu item, and the "Image/video" toolbar tool all invoke a native OS file-chooser dialog that never appears in the remote/headless browser — clicks are silently swallowed. There is no alternative image source: the fill panel's Libraries tab shows "No paint styles", Assets has 0 components, Tools is empty, Plugins/Widgets/Libraries menus are disabled, there is no URL-entry option, no internet access, and canvas paste ignores external clipboard content (only the app's internal clipboard works). The Image tab itself and the adjustment sliders work: Saturation could be dragged to maximum (100) and persisted, but on an empty image fill.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a rectangle on the canvas.
3. Open the fill paint panel and switch to the Image tab (fill converts to image-type; controls show Fill mode dropdown, "Choose Image", and adjustment sliders: Exposure, Contrast, Saturation, Temperature, Tint, Highlights, Shadows).
4. Click the "Choose Image" button to pick a picture.
5. If nothing happens, try the alternatives: "Place image… (Shift+K)" menu item, the "Image/video" toolbar tool, the fill panel Libraries tab, Assets, and pasting an image into the canvas.
6. Drag the Saturation adjustment slider all the way to maximum.

Actual Result:

- Clicking "Choose Image" (tried ~5 times, including via direct element reference and long waits) has no effect: the native OS file-chooser dialog never appears; clicks are silently swallowed. Same for "Place image… (Shift+K)" and the "Image/video" toolbar tool.
- No alternative image source exists: fill panel Libraries tab shows "No paint styles"; Assets has 0 components; Tools is empty; Plugins/Widgets/Libraries menus are disabled; no URL-entry option; external pictures blocked (confirmed DNS failure); canvas paste ignores external clipboard content (the app only pastes from its internal clipboard).
- The Saturation slider itself works: dragged fully right, value reads 100 (max) and persists after closing/reopening the panel — but on a fill with no actual picture.

Expected Result:
Clicking "Choose Image" (or "Place image…" / the Image/video tool) should open a working image chooser so a picture can be loaded into the fill; the adjustment sliders should then operate on the loaded image. The app needs an image source that works in a browser-only environment.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0ac30fb8-af5e-4cbd-b40f-1653de8e4386.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0e6fcd45-0547-434a-a67a-a667e2e1a1f4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8410eca9-5eb1-4876-82e3-080209553d0b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d9b7a07b-1103-4e08-80c1-a081e77a14fb.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f0b17345-33ec-4d79-9b87-68a0fea1ca8e.txt`

Agent report (verbatim tail of failing run):

```
The saturation setting persisted (slider remains at the far right = 100) after closing and reopening the panel, while all other sliders are still at 0. The final state is: Rectangle 1 selected, fill type = Image (Image tab active in the paint panel), Saturation = 100 (maximum).

**Summary of what I did and found:**

1. **Drew a rectangle** ✓ — Selected the rectangle tool from the bottom toolbar and drew a 260×180 rectangle ("Rectangle 1").
2. **Image fill (Image tab in paint panel)** — Partially ✓: I opened the fill paint panel, switched to the **Image** tab, which converted the fill to an image-type fill and revealed the image controls (Fill mode dropdown, "Choose Image", and adjustment sliders: Exposure, Contrast, Saturation, Temperature, Tint, Highlights, Shadows).
3. **Choosing a picture** ✗ — **Blocked.** The "Choose Image" button (tried ~5 times, incl. via direct element reference and with long waits), the "Place image… (Shift+K)" menu item, and the "Image/video" toolbar tool all invoke a native OS file-chooser dialog, which never appears in this remote/headless browser environment — clicks are silently swallowed. I exhausted alternatives: the fill panel's "Libraries" tab has "No paint styles", Assets has 0 components, Tools is empty, Plugins/Widgets/Libraries menus are disabled, there is no URL-entry option, no internet access for external pictures (confirmed DNS failure), and pasting an image into the canvas doesn't work — the app only pastes from its internal clipboard (I verified the system clipboard held an `<img src=…>` fragment of the app's own favicon, and an SVG-with-image snippet, but canvas paste ignores external clipboard content). So no picture could be loaded into the fill.
4. **Saturation slider to maximum** ✓ — Dragged the Saturation slider in the image fill panel fully to the right; its value reads **100** (max) and it persists after closing/reopening the panel.

The core blocker: in this environment it is impossible to actually pick a picture for the image fill because the image chooser relies on a native OS file dialog that cannot be opened/driven through the browser-only interface, and the app offers no alternative image source (no stock/library images, no URL import, no working clipboard/drag-drop import). Everything else (rectangle, Image fill tab, max Saturation) was completed successfully.

verdict: not-approve
```
