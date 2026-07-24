# DesignPen [text & typography]: 'text font bind variable' fails QA — 4/5 runs report broken workflow (00302-text-font-bind-variable-ui)

Description:
Binding a text layer's font family to a STRING variable works end-to-end, but the "Apply variable" affordance on the font family row in the Typography section is invisible: unlike the Opacity row (which shows a visible variable icon), the button never appears visually — not even on hover over the row, its right edge, or the dropdown (tested on two separate text layers). The button exists in the DOM and works when activated directly, so a mouse user has no visible affordance to click. Additionally, immediately after applying the variable the canvas text disappeared and stayed invisible for 5+ seconds, only re-rendering after entering and exiting text edit mode (likely a missing repaint after the Roboto font loaded).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Local variables dialog from the left panel's Variables tab.
3. Create a collection via the folder+ button in the dialog.
4. Add a Text (STRING) variable named "body-font" with value "Roboto".
5. Create a text layer with the text "Hello World".
6. In the Typography section, hover over the font family row (and its right edge / dropdown) looking for the "Apply variable" affordance.
7. Activate the DOM-present "Apply variable" button on the font family row directly and select "body-font" in the picker.
8. Observe the canvas immediately after applying the variable.

Actual Result:
- The "Apply variable" button on the font family row never appears visually, even on hover (reproduced on two separate text layers); it exists in the DOM and works only when activated directly.
- Immediately after applying the variable, the "Hello World" text vanished from the canvas and stayed invisible for 5+ seconds; it only re-rendered after entering and exiting text edit mode.
- The binding itself works: the font family row shows the "body-font" variable chip (with detach icon), the text renders in Roboto, and the binding persists.

Expected Result:
The variable affordance on the font family row should be visible (at least on hover, like the Opacity row) so it can be discovered and clicked with the mouse, and the canvas text should repaint immediately after the bound font is applied, without requiring text edit mode to force a re-render.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 completed runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_06d90a8c-3edb-4d89-be7e-705472973e64.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3c37705e-af7d-409c-8cfb-7452caa453fe.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_630208cb-b2ba-4837-af5e-b8354259c9da.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bd64f59f-2424-457c-ad12-9f653c4fab6e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bec77b1f-e405-460a-aa95-068db302c422.txt`

Agent report (verbatim tail of failing run):

```
Final state is confirmed: the font family row in Typography shows the "body-font" variable chip (with detach icon), and "Hello World" renders in Roboto on the canvas.

**Summary of what I did:**
1. ✅ Opened the Local variables dialog from the left panel's Variables tab
2. ✅ Created a collection ("New collection") via the folder+ button in the dialog
3. ✅ Added a Text (STRING) variable named "body-font" with value "Roboto" (Mode 1)
4. ✅ Created a text layer with the text "Hello World"
5. ✅ Bound the font family to the "body-font" variable via the "Apply variable" affordance on the font family row — the picker listed "body-font", and applying it replaced the font dropdown with a variable chip; the text now renders in Roboto and the binding persists

**Problems encountered:**
- **Invisible variable affordance on the font family row:** Unlike the Opacity row (which shows a visible variable icon), the font family row's "Apply variable" button never appeared visually — not even when hovering over the row, its right edge, or the dropdown (tested on two separate text layers). The button exists in the DOM and works when activated directly, but a mouse user would have no visible affordance to click. This is a discoverability/rendering bug in the exact feature under test.
- **Canvas text disappeared after binding:** Immediately after applying the variable, the "Hello World" text vanished from the canvas and stayed invisible for 5+ seconds of waiting; it only re-rendered after I entered and exited text edit mode (likely a missing repaint after the Roboto font loaded).

The end-to-end flow was achievable and the final state is correct, but the hidden affordance and the transient canvas rendering glitch are real bugs.

verdict: not-approve
```
