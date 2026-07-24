# DesignPen [image handling]: 'image tile scale' fails QA — 3/3 runs report broken workflow (00268-image-tile-scale-ui)

Description:
The Tile scale-mode controls in the image fill panel work (scale mode can be set to Tile and 50 can be typed into the tile scale percent field), but no actual picture can be loaded into the image fill, leaving the workflow unfulfillable. "Choose Image", "Place image… (Shift+K)", and the Image/video tool all trigger a native file chooser that never appears in the browser context (the hidden file input is not reachable programmatically either). Clipboard paste is blocked with red toasts "Clipboard access is blocked in this browser context" and "PNG clipboard export is not available in this browser", there is no internet access, and the app ships no sample images (Assets 0 components, Libraries "No paint styles", no plugins, AI panel needs an API key, Code panel read-only).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a rectangle on the canvas.
3. Open the fill popup and set the fill type to Image.
4. Attempt to load any picture: click "Choose Image", try "Place image… (Shift+K)", or the Image/video tool; also try pasting an image from the clipboard.
5. Set the scale mode dropdown to Tile.
6. Type 50 into the tile scale percent field and commit it.

Actual Result:

- "Choose Image", "Place image… (Shift+K)", and the Image/video tool all trigger a native file chooser that never appears (clicked repeatedly, waited 5+ seconds — no dialog, no effect); the hidden file input is not reachable programmatically.
- Pasting shows red toasts: "Clipboard access is blocked in this browser context" on paste and "PNG clipboard export is not available in this browser" on Copy-as-PNG.
- No internet access (external domains fail DNS) and no sample images anywhere in the app (Assets 0 components, fill Libraries tab "No paint styles", no plugins, AI panel requires an API key, Code panel read-only).
- The rectangle ends with an image-type fill configured with Tile mode at 50% tile scale (field shows "50 %"), but the fill contains no actual picture.

Expected Result:
The user should be able to load a picture into the image fill (via a working image chooser or another image source), set the scale mode to Tile, and type 50 into the tile scale percent field so each tile renders at half the image's original size.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 3 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_30acb54a-c2b0-4f6d-a70f-b8e86fbb1aa4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_86672c89-13b8-4b46-b98d-c38f081bfb8a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ab27c783-ef7e-4c01-8385-d03f54827f9e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b3ab87d4-3a96-491a-9fac-a49c84943b50.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bafb0b7f-9d5e-425e-bf7f-8b7c2f19735a.txt`

Agent report (verbatim tail of failing run):

```
Final state is confirmed. Here's a summary of what happened:

**Completed:**
- Drew a rectangle (300×250 at X=204, Y=200) on the canvas
- Set its fill type to **Image** in the fill popup
- Set the scale mode dropdown to **Tile**
- Typed **50** into the tile scale percent field and committed it (field shows "50 %")

**Blocked — could not load an actual picture into the image fill:**
Every possible path to supply a picture failed in this environment:
1. **"Choose Image"**, **"Place image… (Shift+K)"**, and the **Image/video tool** all trigger a native file chooser that never appears in this browser context (clicked repeatedly, waited up to 5+ seconds — no dialog, no effect; the hidden file input isn't reachable programmatically either).
2. **Clipboard is blocked**: the app shows red toasts "Clipboard access is blocked in this browser context" on paste and "PNG clipboard export is not available in this browser" on Copy-as-PNG, so pasting an image was impossible.
3. **No internet access** (external domains fail DNS), so no picture could be fetched from the web.
4. The app contains **no sample images anywhere**: Assets has 0 components, fill Libraries tab shows "No paint styles", no plugins installed, AI panel requires an API key, and the Code panel is read-only.

So the rectangle ends with an image-type fill configured with Tile mode at 50% tile scale, but the fill contains no actual picture — the core "with any picture" requirement was impossible to satisfy because the file chooser is suppressed and all alternative image sources are blocked in this sandbox.

verdict: not-approve
```
