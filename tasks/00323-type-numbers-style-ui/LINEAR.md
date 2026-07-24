# DesignPen [text & typography]: 'type numbers style' fails QA — 3/5 runs report broken workflow (00323-type-numbers-style-ui)

Description:
Setting tabular (monospaced) figures via the Type settings popover (Details tab → Numbers → Style) works once reached, but the entry point is effectively unreachable at a 1280x720 viewport: the right-hand Design panel's content overflows past the window's right edge, clipping the sliders-icon "Type settings" button (and the vertical alignment buttons) off-screen. Mouse-wheel horizontal scrolling over the panel does not reveal the button; the agent could only reach it via the accessibility tree and a programmatic scrollIntoView. This is a UI layout/responsiveness bug — a regular user cannot find or click the button at this resolution.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer with the digits "1234567890" using the Text tool.
3. Look at the Typography section in the right Design panel: the sliders button (tooltip "Type settings") at the end of the Alignment row is clipped off the right edge (only a tiny sliver of one button visible).
4. Try to scroll the panel horizontally with the mouse wheel — the button is not revealed.
5. (Workaround) Scroll the button into view programmatically (scrollIntoView via the accessibility tree), click it to open the Type settings popover.
6. Switch to the Details tab and click the second "17" button in the Numbers → Style row (tooltip: "Monospace uppercase/lining").

Actual Result:

- At 1280x720 the "Type settings" sliders button and vertical alignment buttons render off-screen, clipped past the window's right edge; horizontal mouse-wheel scrolling over the panel does not reveal them.
- The button could only be clicked after locating it in the accessibility tree and calling scrollIntoView programmatically — not achievable by a regular user.
- Once reached, the tabular figures setting itself worked correctly: the text layer's width grew from 85×17 to 91×17 px and the setting persisted when the popover was reopened.

Expected Result:
The Type settings button (and all Typography section controls) are visible and clickable within a 1280x720 viewport, either by fitting the panel content or providing working scrolling.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0eca181f-9230-4c8b-a2f3-907a06c911b6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_27b0f00f-47ec-4367-b513-454855bfb44a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5916d10c-2eb9-4350-989f-23e2b6d37d5b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dcb92857-29b6-4be7-83e1-dde062020bc3.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f3fa8e0d-3a70-4bd1-8005-265ccccaec5e.txt`

Agent report (verbatim tail of failing run):

```
All steps completed successfully. Summary of what was done:

1. **Created a text layer** with the digits "1234567890" using the Text tool on the canvas.
2. **Opened the Type settings popover** via the sliders button (tooltip confirmed: "Type settings") located at the end of the Alignment row in the Typography section.
3. **Switched to the Details tab** in the popover.
4. **Set the number style to tabular (monospaced) figures** by clicking the second "17" button in the Numbers → Style row (tooltip: "Monospace uppercase/lining"). The change applied correctly — the text layer's width grew from 85×17 to 91×17 px (tabular digits are evenly spaced), and the setting persisted when the popover was reopened.

However, there was a notable problem along the way: at this viewport (1280×720), the right-hand Design panel's content overflows past the window's right edge. The sliders ("Type settings") button — along with the vertical alignment buttons — was clipped/rendered off-screen and not visible in the default view (only a tiny sliver of one button was visible). Mouse-wheel horizontal scrolling over the panel did not reveal it; I had to locate the button via the accessibility tree and scroll it into view programmatically (scrollIntoView) before I could click it. A regular user would likely be unable to find or click this button at this resolution, so this is a real UI layout/responsiveness bug, even though the underlying functionality (Type settings → Details → tabular figures) works correctly once reached.

verdict: not-approve
```
