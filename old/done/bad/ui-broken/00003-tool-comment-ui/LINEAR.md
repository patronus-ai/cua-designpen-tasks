# DesignPen [toolbelt]: 'tool comment' fails QA — 5/5 runs report broken workflow (00003-tool-comment-ui)

Description:
The comment-creation flow is broken after pin placement: the Comment tool activates (toolbar speech-bubble button or the C shortcut) and clicking the canvas drops a blue draft comment pin (exposed in the DOM as a "Draft comment" button), but the comment composer/text input never renders. The full accessibility tree contains no textbox, textarea, or contenteditable element for comments at any point, so no comment text can ever be typed or submitted; the Comments panel count stays at "Open 0 / No comments". Clicking, double-clicking, hovering, Enter/Space on the focused pin, right-clicking, dragging, and placing the pin over a frame object all fail to open the composer — the draft pin can only be discarded.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool via the toolbar speech-bubble button or by pressing C (the tool highlights blue and a Comments panel opens on the right showing "Open 0 / Resolved 0 / All 0 — No comments").
3. Click near the middle of the canvas to drop a comment pin (a blue draft pin appears).
4. Attempt to type "needs review" — no composer/text input is present.
5. Optionally try clicking/double-clicking/hovering the pin, pressing Enter or Space on the focused pin, right-clicking, dragging, or placing the pin on top of a frame object — the composer still never appears.

Actual Result:

- After placing the pin, no text input/composer box opens anywhere; screenshots and zoomed inspection show no composer UI near the pin or elsewhere.
- The full accessibility tree (including off-viewport elements) contains "**no textbox, textarea, or contenteditable element** for comments at any point".
- Attempting to type returned: "no editable element is focused (active element: BUTTON)".
- The draft pin can only be discarded (Escape / tool switch); no comment is ever created, and the Comments panel count stays at 0.

Expected Result:
After dropping a comment pin, a comment composer with a text input should open next to the pin, allowing the user to type "needs review" and submit; the new comment should appear in the Comments panel (Open count increments to 1).

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3b895e9a-c0f0-4597-a3c6-0a04b647e3f4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3d234386-5457-4976-825e-d92098fc4e90.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_413ae9fe-f63d-410a-a128-6f4a1e705c7d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8c28866b-d874-4b75-9c89-a60c4a3520e5.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bafd5567-dfe7-40bc-8c2a-e19582bbbb7d.txt`

Agent report (verbatim tail of failing run):

```
The undo cleaned up the test frame. The app is back to a clean state, with the Comments panel still showing "Open 0 / No comments".

**Summary of what I did and found:**

1. **Activating the Comment tool worked** — both via the toolbar speech-bubble button and via the `C` shortcut. The tool highlights blue and a Comments panel opens on the right (showing "Open 0 / Resolved 0 / All 0 — No comments").

2. **Dropping a pin worked** — clicking near the middle of the canvas places a blue draft comment pin (exposed in the DOM as a "Draft comment" button).

3. **The comment composer never appears** — this is where the task is blocked. After placing the pin, no text input/composer box opens. I verified exhaustively:
   - Screenshots and zoomed inspection show no composer UI anywhere near the pin or elsewhere.
   - The full accessibility tree (including off-viewport elements) contains **no textbox, textarea, or contenteditable element** for comments at any point.
   - Attempting to type returned: "no editable element is focused (active element: BUTTON)".
   - I tried clicking the pin, double-clicking, hovering, pressing Enter/Space on the focused pin, right-clicking (only a generic canvas context menu appeared), dragging, waiting for async render, and even placing the comment on top of a frame object — the composer never renders in any scenario.
   - The draft pin can only be discarded (Escape / tool switch); no comment is ever created, and the Comments panel count stays at 0.

Because the composer UI never opens, it was impossible to type "needs review" or submit the comment. The comment-creation flow is broken after the pin-placement step. I left the file clean (test frame undone, no stray comments).

The Comment tool activates and drops a pin, but the comment composer/text input never renders, so the comment could not be typed or submitted — this is a blocking bug in the app.

verdict: not-approve
```
