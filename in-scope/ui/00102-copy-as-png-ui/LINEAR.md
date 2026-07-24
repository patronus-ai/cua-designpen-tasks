# DesignPen [clipboard / copy-paste]: 'copy as png' fails QA — 4/5 runs report broken workflow (00102-copy-as-png-ui)

Description:
The context-menu action Copy/Paste as > Copy as PNG fails: clicking the menu item on a selected rectangle shows a red error toast "PNG clipboard export is not available in this browser" and nothing is copied to the clipboard. The failure is specific to the PNG clipboard export path — a control test of "Copy as SVG" on the same rectangle executed with no error. All surrounding UI (drawing, selecting, context-menu navigation, the submenu itself) works; the PNG raster export to clipboard is what's broken in this browser context.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the rectangle tool from the bottom toolbar and drag on the canvas to draw a small rectangle (e.g. 110x80 "Rectangle 1").
3. Ensure the rectangle is selected (selection handles visible, highlighted in Layers panel).
4. Right-click the rectangle to open the context menu.
5. Hover "Copy/Paste as" and click "Copy as PNG" in the submenu (use the menu item, not the ⌘⇧C shortcut — the shortcut label is display-only and not wired).

Actual Result:

- A red error toast appears: "PNG clipboard export is not available in this browser" (shown on each of 3 attempts).
- The rectangle is never copied to the clipboard as a raster image.
- Control test: "Copy as SVG" on the same rectangle executed with no error, so the failure is specific to the PNG clipboard export path.

Expected Result:
Choosing Copy/Paste as > Copy as PNG on a selected shape should place a PNG raster image of that shape onto the clipboard with no error toast.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_90710d42-0bb6-4053-9100-991572e77dd0.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b5db10e1-2e35-42a3-8bba-f741b1911f3d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d8649dc7-7feb-46a0-aac6-12c4e16be6b0.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dac18e30-774a-4273-a9d0-6db3e29b438f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e07e3b60-b3dd-4668-a3cc-c114604a46cf.txt`

Agent report (verbatim tail of failing run):

```
I now have definitive confirmation. The zoomed screenshot clearly shows a red error toast: **"⚠ PNG clipboard export is not available in this browser"** with a copy icon and close button.

## Summary of what I did

1. **Drew a small rectangle** — Selected the rectangle tool from the bottom toolbar and dragged on the canvas to create a 110 × 80 rectangle ("Rectangle 1").
2. **Selected it** — The rectangle was selected, confirmed by the selection handles, the highlighted "Rectangle 1" entry in the Layers panel, and the RECTANGLE properties in the Design panel.
3. **Right-clicked it** — The context menu opened with options including "Copy/Paste as".
4. **Chose Copy/Paste as > Copy as PNG** — The submenu showed "Copy as text / Copy as SVG / Copy as PNG (Ctrl+Shift+C) / Copy as JSX / Copy node ID / Copy XPath", and I clicked **Copy as PNG** via the menu item (not the shortcut), as instructed.

## Result

The "Copy as PNG" action **failed**. Each of the 3 attempts produced a red error toast: **"PNG clipboard export is not available in this browser"** — meaning the rectangle was never copied to the clipboard as a raster image. As a control test, "Copy as SVG" on the same rectangle executed with no error, so the failure is specific to the PNG clipboard export path in this app.

All the UI steps (drawing, selecting, right-click menu navigation) worked fine, but the core goal — getting a PNG raster image onto the clipboard — was blocked by the application's own error stating PNG clipboard export is unavailable.

verdict: not-approve
```
