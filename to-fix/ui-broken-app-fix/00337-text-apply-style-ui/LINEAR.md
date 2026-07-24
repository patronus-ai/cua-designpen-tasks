# DesignPen [text & typography]: 'Create text style' dialog fails QA — 2/5 runs report broken workflow (00337-text-apply-style-ui)

Description:
The "Create new text style" modal (opened from the Styles section "+" → "Text") is taller than the supported 1280x720 viewport, and its primary "Create style" confirmation button is rendered below the fold. The modal is not scrollable: mouse-wheel scrolling over it, `scroll_to` on the button, and a direct click on the off-screen button element all have no effect, so the form cannot be submitted at the standard viewport. Runs only got past this by zooming the browser out to 80% to bring the button on-screen — a workaround a normal user would not know to perform. Style creation and the TextStylesMenu application flow both work once the dialog can be submitted, so the defect is purely the modal's height/overflow at the supported viewport.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press Escape / click empty canvas so nothing is selected.
3. In the properties panel Styles section, click "+" and choose "Text".
4. In the "Create new text style" modal, set Weight = Bold and Size = 32.
5. Attempt to click the "Create style" confirmation button (try wheel-scroll and scroll-to to reach it).

Actual Result:
- The "Create style" button is rendered below the bottom of the 720px viewport.
- The modal provides no scrollbar; wheel-scroll over the modal, `scroll_to` on the button, and a direct element click all fail to submit the form — the dialog stays open.
- The only way to reach and click the button is to zoom the browser out (e.g. to 80%), which is not a legitimate in-app interaction at the supported viewport.

Expected Result:
At the supported 1280x720 viewport, the "Create new text style" modal should fit within the viewport (or be scrollable) so that the "Create style" confirmation button is reachable and the form can be submitted without zooming the browser.

Estimate: S (2 points) — CSS layout/overflow fix on one modal (constrain height, add scroll, or pin footer).

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 2 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a294577a-b47c-4bb3-9619-c15a9fbded38.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b20540a2-fe82-4bf6-af9e-12138059dc82.txt`

Agent report (verbatim tail of failing run):

```
I've completed and verified the full task. Let me summarize what was done and what I observed.

## Summary

What I accomplished:
1. Created a shared text style — Used the Styles section "+" (with nothing selected) → "Text" → set weight to Bold and size to 32 → "Create style". It now appears in the Styles panel as "New text style · 32/Auto" with a bold "Ag" preview (exactly one style, no duplicates).
2. Added a text layer — Used the Text tool to create a layer on the canvas and typed "Section title".
3. Applied the style via the TextStylesMenu — In the Typography section, clicked the grid (4-dot) TextStylesMenu icon and selected "New text style". The text is now rendered bold at 32px, and the Typography panel shows the applied style chip "Ag New text style · 32/38.4".

All three requirements are confirmed working: the style carries the right properties (32px Bold), the layer has the correct text, and the style is correctly bound to the layer.

One problem I hit: When creating the text style via the Styles "+", the "Create new text style" modal was taller than the 1280×720 viewport, and its primary "Create style" confirmation button sat below the fold. The modal is not scrollable — scrolling over it and scroll_to on the button had no effect, and an initial click on the off-screen button did nothing (the dialog stayed open). I only managed to reach and click it by zooming the browser out to 80%. At the default viewport, a user who didn't think to zoom would be unable to submit the form, so this is a genuine (if minor, workaround-able) usability issue rather than a pure feature failure.

Because I encountered this blocker during the flow, I'm flagging it honestly.

verdict: not-approve
```
