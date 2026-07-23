# DesignPen [text & typography]: 'text truncate' fails QA — 3/5 runs report broken workflow (00314-text-truncate-ui)

Description:
The truncation feature itself works (Type settings popover → Basics tab → "Truncate text" with the "A…" ellipsis option truncates the canvas text correctly), but the right-hand Design panel overflows horizontally at the 1280x720 viewport: the Type settings sliders button and part of the alignment buttons are clipped completely off-screen in the panel's default state, with only a half-cut button visible at the panel edge. There is no horizontal scrollbar and mouse-wheel scrolling (left/right) on the panel does not reveal the clipped controls; the sliders button is only reachable by scrolling it into view via the accessibility tree. The required control being visually clipped and unreachable through normal scrolling is a genuine UI layout bug at this viewport.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer with the sentence "This sentence is far too long to fit inside a small text box".
3. Switch the layer's resizing to fixed size and shrink its box to 150 x 17 so the sentence overflows the box.
4. Look at the end of the Typography section's alignment row in the right-hand Design panel for the Type settings sliders button; try mouse-wheel scrolling left/right on the panel to reveal it.
5. Scroll the sliders button into view via the accessibility tree and click it to open the Type settings popover.
6. In the Basics tab, enable "Truncate text" with the "A…" (ellipsis) option.

Actual Result:
- In the panel's default state, the Type settings (sliders) button and part of the alignment buttons are clipped completely off-screen (a half-cut button visible at the panel edge); there is no horizontal scrollbar and mouse-wheel scrolling on the panel does not reveal them.
- The sliders button is only reachable by scrolling it into view via the accessibility tree.
- Once reached, truncation works: the segment highlights in the popover and the canvas text renders as "This sentence is far t…" (layer 150 x 17).

Expected Result:
The Type settings button and alignment controls should be fully visible or reachable via normal scrolling in the Design panel at a 1280x720 viewport, without accessibility-tree workarounds.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_22f94ac5-7530-4fec-a7ab-010c97f473cd.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_527648b7-737c-4cd7-bc22-ee483a6a641c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9ecb3f9c-0b75-461a-bbeb-2bf8b6130ddc.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b662af74-a09a-4f5a-bae5-8170f41658ee.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fa7b122d-2959-401f-8170-d566f593fe32.txt`

Agent report (verbatim tail of failing run):

```
The popover closed, and a tooltip confirms the sliders button is indeed "Type settings". The canvas shows the final result: the text layer (150 × 17) now displays "This sentence is far t…" — truncated with an ellipsis.

**Summary of what was done:**
1. ✅ Created a text layer with the sentence "This sentence is far too long to fit inside a small text box"
2. ✅ Switched the layer's resizing to fixed size and shrunk its box to 150 × 17, so the sentence no longer fit (it overflowed the box)
3. ✅ Opened the Type settings popover via the sliders button at the end of the Typography section's alignment row (tooltip: "Type settings")
4. ✅ In the Basics tab, enabled "Truncate text" with the "A…" (ellipsis) option — verified both in the popover (segment highlighted) and on canvas (text now renders as "This sentence is far t…")

**Problem encountered:** The right-hand Design panel overflows horizontally at the 1280×720 viewport — the Type settings (sliders) button and part of the alignment buttons were clipped completely off-screen in the panel's default state (a half-cut button was visible at the panel edge). Mouse-wheel scrolling (left/right) on the panel did not reveal them and there was no horizontal scrollbar; I could only reach the sliders button by scrolling it into view via the accessibility tree. While the truncation feature itself worked perfectly once the button was reached, the required control being visually clipped and not reachable through normal scrolling is a genuine UI layout bug at this viewport.

verdict: not-approve
```
