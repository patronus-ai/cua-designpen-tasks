# DesignPen [text & typography]: 'text list style' fails QA — 3/5 runs report broken workflow (00309-text-list-style-ui)

Description:
The numbered list style feature itself works (Type settings popover → Basics tab → Numbered updates the canvas correctly), but the right-hand Design panel has a layout/overflow bug at the 1280x720 viewport: the panel content is wider than the visible panel area, so the Type settings sliders button and the vertical-alignment buttons at the end of the Alignment row are clipped off-screen/hidden behind the scrollbar. Horizontal mouse-wheel scrolling does not reveal them and hovering the clipped sliver shows no tooltip; the button is only reachable via programmatic scrollIntoView through the accessibility tree, which then leaves the panel awkwardly shifted (labels truncated to "graphy", "rance") until the layer is reselected. A normal mouse user cannot discover or click the Type settings button at this window size.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer with three coffee-making steps on separate lines: "Grind beans", "Boil water", "Pour and brew".
3. With the layer selected, look at the end of the Alignment row in the Typography section of the right-hand Design panel for the Type settings sliders button.
4. Try to reveal the clipped sliders button with horizontal mouse-wheel scrolling over the panel.
5. Scroll the sliders button into view programmatically (e.g. scrollIntoView via the accessibility tree) and click it to open the Type settings popover.
6. In the Basics tab, set the list style to Numbered.

Actual Result:
- The Type settings sliders button (and the vertical-alignment buttons) at the end of the Alignment row are clipped off-screen/hidden behind the scrollbar; horizontal mouse-wheel scrolling over the panel does not reveal them and hovering the clipped sliver shows no tooltip.
- Reaching the button requires programmatic scrollIntoView via the accessibility tree, which leaves the panel horizontally shifted (labels truncated to "graphy", "rance") until the layer is reselected.
- Once reached, the feature works: setting the list style to Numbered updates the canvas text to a numbered list (1. Grind beans, 2. Boil water, 3. Pour and brew) and the Numbered toggle shows as selected.

Expected Result:
At a 1280x720 viewport, the Type settings sliders button and all Alignment-row controls should be visible in the Design panel or reachable by normal scrolling, without clipping or requiring accessibility-tree workarounds.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0b0b7b4e-98f6-4a6a-b801-14779e9c3719.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5a5c8566-db83-4346-bc5f-bea33598d91e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c984906c-3e60-4e3c-9b8c-11d1e5981224.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ef36ae04-7d04-4104-968e-f900d8215bba.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fb332540-a80d-4585-b1d3-c09620461bf6.txt`

Agent report (verbatim tail of failing run):

```
The popover is closed and the task is complete. The canvas shows the text layer with the numbered list:
1. Grind beans
2. Boil water
3. Pour and brew

**Summary of what was done:**
1. ✅ Created a text layer with three coffee-making steps on separate lines ("Grind beans", "Boil water", "Pour and brew")
2. ✅ Opened the Type settings popover via the sliders button in the Typography section (tooltip confirmed "Type settings")
3. ✅ In the Basics tab, set the list style to Numbered — the canvas text updated to a numbered list (1., 2., 3.) and the Numbered toggle shows as selected

**Issue encountered:** While the feature itself worked, the right-hand Design panel has a layout/overflow bug at this viewport size (1280×720): the panel content is wider than the visible panel area, so the Type settings sliders button (and the vertical-alignment buttons) at the end of the Alignment row were clipped off-screen/hidden behind the scrollbar. Horizontal mouse-wheel scrolling over the panel did not reveal them, and hovering the clipped sliver showed no tooltip. I could only reach the sliders button by programmatically scrolling it into view via the accessibility tree (scrollIntoView), which also left the panel awkwardly shifted (labels truncated to "graphy", "rance") until I reset it by reselecting the layer. A normal user would have serious trouble discovering/clicking the Type settings button at this window size.

verdict: not-approve
```
