# DesignPen [text & typography]: 'text resize mode' fails QA — 5/5 runs report broken workflow (00236-text-resize-mode-ui)

Description:
The "Auto height" text resizing mode (Design panel > Layout > Resizing) does not recompute the text box height when the box width changes. With Auto height active, typing a new W value in the Dimensions panel or dragging a side resize handle causes the text to visibly rewrap onto more lines, but the bounding box keeps its stale height and the text overflows below the box (Code panel showed the box staying `300×17` while 2 lines rendered, then `200×34` / `251×34` while 3-4 lines rendered outside the box). Height only recomputes when the text content itself is edited — a dummy edit (type a space, then backspace) is needed to force reflow. Additionally, when creating a text layer via the "T" keyboard shortcut, the "t" keypress is inserted as the first character of the new text layer.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer containing a sentence or two (e.g. "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs."). Note: activating the text tool via the "t" shortcut inserts a stray "t" as the first character of the new layer.
3. Select the text layer.
4. In Design panel > Layout > Resizing, set the resizing mode to Auto height (middle button; H field becomes grayed out/auto-computed, W stays editable).
5. Change the text box width — either type a new W value in the Dimensions panel or drag a side resize handle — so the text must rewrap onto more lines.
6. Observe the box height in the panel / Code panel versus the rendered text.

Actual Result:

- Changing the width with Auto height active does not trigger height recalculation: the text rewraps to more lines but overflows below the stale bounding box (verified via Code panel: box stayed `300×17` while 2 lines rendered; `200×34` / `251×34` while 3-4 lines rendered outside the box).
- The height only recomputes when the text content is edited; a dummy edit (type a space, then backspace) was required to force the box to reflow to the correct `300×34`.
- Separate quirk: the "t" text-tool shortcut keypress was inserted as the first character of the new text layer ("tThe quick brown fox…"), requiring select-all and retyping.

Expected Result:
With Auto height resizing active, any width change (typed W value or handle drag) should immediately recompute the box height so the box grows/shrinks to contain the wrapped text — width changes are the primary way wrapping is induced in this mode. The text-tool shortcut keypress should not be inserted into the new text layer.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0410b3e9-37f1-4463-aef3-3fd38b0b17ef.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2ad44d4c-84f6-4ada-b12a-8163ef86db51.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4d8835da-13ee-4ab7-bb63-373d5ec348ac.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_695ee02a-79fc-4453-b9bd-336570ca6b7d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bc339e19-9aa3-4cfb-9f2a-9508a2192023.txt`

Agent report (verbatim tail of failing run):

```
The task deliverable is complete. Final state:

- **Text layer added**: "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs." — visible in the Layers panel and on the canvas.
- **Layer selected** with **Resizing = Auto height** active in Design panel > Layout > Resizing (middle button highlighted; H field grayed out as auto-computed, W editable).
- The box is 300 × 34: fixed width, with the text wrapped onto 2 lines and the height grown to contain them.

**Summary of how it went:**

The core task was accomplished, but I hit two issues along the way:

1. *Minor quirk:* When creating the text layer, the "t" keypress (text-tool shortcut) was itself inserted as the first character of the new text layer ("tThe quick brown fox…"), so I had to select-all and retype the sentence to remove the stray character.

2. *Real bug in the Auto height feature:* With Auto height active, changing the text box width does **not** trigger the automatic height recalculation — neither when typing a new W value in the Dimensions panel nor when dragging a side resize handle. The text visibly rewraps to more lines but overflows below the stale bounding box (verified via the Code panel: box stayed `300×17` while 2 lines rendered, then `200×34` / `251×34` while 3–4 lines rendered outside the box). The height only recomputes when the text content is edited — I had to perform a dummy edit (type a space, then backspace) to force the box to reflow to the correct `300×34`. This contradicts the intended behavior that "the box keeps its width but grows taller as the text wraps," since width changes are the primary way wrapping is induced in this mode.

Because of the stray-character quirk and especially the reproducible auto-height reflow bug that required a workaround:

verdict: not-approve
```
