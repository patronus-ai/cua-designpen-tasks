# DesignPen [text & typography]: 'text underline details' fails QA — 3/5 runs report broken workflow (00315-text-underline-details-ui)

Description:
The underline decoration workflow itself works (Type settings popover → Basics tab → "U" in the Decoration row, then the ">" chevron opens the Underline subview where Dotted can be selected), but at the 1280x720 viewport the right-hand Design panel's Typography section overflows horizontally: the alignment row shows only 3 of its buttons, and the Type settings sliders button plus the vertical-alignment buttons are clipped off-screen past the right edge. There is no visible scrollbar and mouse-wheel horizontal scrolling does nothing, so the sliders button is effectively unreachable by normal mouse interaction. Reaching it via programmatic accessibility-tree scrolling leaves the panel stuck in a horizontally-shifted state (most content hidden) until the layer is deselected and reselected.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. With the Text tool, click on the canvas and type "fine print" to create a text layer.
3. In the Typography section of the right-hand Design panel, look for the Type settings sliders button at the end of the alignment row; try mouse-wheel horizontal scrolling on the row.
4. Scroll the sliders button into view programmatically via the accessibility tree and click it to open the Type settings popover.
5. In the Basics tab, click the "U" button in the Decoration row to set Underline.
6. Click the ">" chevron next to Decoration to open the Underline subview and select the dotted style (middle option).

Actual Result:
- The Typography section overflows horizontally: the alignment row shows only 3 of its buttons, and the Type settings sliders button (plus the vertical-alignment buttons) is clipped off-screen past the right edge; there is no visible scrollbar and mouse-wheel horizontal scrolling on the row does nothing, making the button effectively unreachable by normal mouse interaction.
- Programmatic scrollIntoView via the accessibility tree reaches the button but leaves the panel stuck in a horizontally-shifted state (most panel content hidden) until the layer is deselected and reselected.
- Once reached, the feature works: Underline applies and the dotted style renders in both the preview and the "fine print" text on canvas.

Expected Result:
The Type settings sliders button and the full alignment row should be visible or reachable by normal scrolling at 1280x720, and scrolling within the panel should not leave it stuck in a shifted state.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7beb35be-8f20-423f-8a3f-1811a2267129.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a665fd45-19ab-43bd-883f-29e4dd3e0a17.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c25e91ad-bf24-4def-bb93-87e36ee325a8.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c5eb4aa2-1b1e-440c-ac22-9877d69d1242.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ca4c5e40-de46-4731-ac85-0cedd453f50a.txt`

Agent report (verbatim tail of failing run):

```
All steps of the task were completed successfully:

1. **Created the text layer** — Used the Text tool, clicked on the canvas, and typed "fine print". The layer appears in the Layers panel and on canvas.
2. **Opened the Type settings popover** — Clicked the sliders button (confirmed by its "Type settings" tooltip) at the end of the Typography section's alignment row.
3. **Set decoration to Underline** — In the Basics tab, clicked the "U" button in the Decoration row; the preview and canvas text showed an underline.
4. **Changed underline style to Dotted** — Clicked the ">" chevron next to Decoration to open the Underline subview, then selected the dotted style (middle option). Verified the preview and the "fine print" text on canvas both now render with a dotted underline.

However, I did hit a real UI problem along the way: at the 1280×720 viewport, the right-hand Design panel's Typography section overflows horizontally — the alignment row only shows 3 of its buttons, and the Type settings sliders button (plus the vertical-alignment buttons) is clipped off-screen past the right edge. There is no visible scrollbar, and mouse-wheel horizontal scrolling on the row does nothing, so the sliders button is effectively unreachable by normal mouse interaction. I could only access it by programmatically scrolling the element into view via the accessibility tree, which then left the panel stuck in a horizontally-shifted state (most panel content hidden) until I deselected and reselected the layer to reset it. The type-settings functionality itself worked correctly once the button was reachable, but the clipped/unscrollable panel layout is a genuine usability bug.

verdict: not-approve
```
