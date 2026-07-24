# DesignPen [comments]: 'comment emoji typeahead' fails QA — 5/5 runs report broken workflow (00436-comment-emoji-typeahead-ui)

Description:
The emoji typeahead in the comment composer cannot be tested because the composer itself never opens. Activating the Comment tool works (toolbar speech-bubble button or "C" shortcut; the right sidebar switches to the Comments panel), and clicking the canvas places a draft pin ("Draft comment" button in the DOM), but no text input, "Add a comment" field, or submit button ever renders — the only textboxes on the entire page are the page-color field and an API-key field. Because the composer never mounts, typing "shipped ", triggering the ":" emoji typeahead, and picking 🎉 from suggestions are all blocked. The "click the canvas to open the composer" core flow is broken.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool via the toolbar speech-bubble button or the "C" keyboard shortcut.
3. Click the canvas to open the comment composer.
4. Attempt to type "shipped " then ":" to trigger the emoji typeahead, type "tada" (or "party"), pick the 🎉 emoji from the suggestions, and submit the comment.

Actual Result:

- Clicking the canvas places a blue draft comment pin (a "Draft comment" button appears in the DOM), but the composer never opens — no text input, no "Add a comment" field, no submit button ever renders (verified via screenshots, accessibility tree including off-viewport elements, and page text extraction immediately after clicking).
- No editable composer element ever mounts in the DOM; the only textboxes on the page are the page-color field and an API-key field.
- Clicking empty canvas, clicking a drawn rectangle, clicking/double-clicking/off-center-clicking the pin, element-level clicks, Enter/Space on the pin, hovering, drag gestures, right-click (only a generic canvas context menu), keyboard Tab-walking, waiting for delayed rendering, and a full page reload with a clean retry all fail.
- Typing "shipped ", triggering the ":" typeahead, picking 🎉, and submitting are all impossible; the Comments panel still shows "Open 0 / No comments."

Expected Result:
Clicking the canvas with the Comment tool active should open a composer text field; typing ":" followed by "tada"/"party" should show emoji typeahead suggestions from which 🎉 can be picked, and the comment should submit successfully.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_268d1f70-236d-4aac-9065-4dec83936f49.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_52aea47c-da7d-4c9f-82f5-6e860293f9f0.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_55abd0dc-b060-4b27-b546-497288d756fe.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_93c5cfa6-a5c8-4d6b-89d6-a68e13800f04.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d8b06339-78c6-4e77-b8e5-9a7fcbe2adbd.txt`

Agent report (verbatim tail of failing run):

```
I was unable to complete the task due to an app bug. Here's a summary of what happened:

**What worked:**
- Activated the Comment tool successfully (both via the toolbar speech-bubble button and the "C" keyboard shortcut) — the tool highlights and the right sidebar switches to the Comments panel.
- Clicking the canvas places a blue draft comment pin (a "Draft comment" button appears in the DOM).

**What failed:**
- The comment composer never opens. After clicking the canvas, only the pin appears — no text input, no "Add a comment" field, no submit button ever renders (verified via screenshots, accessibility tree including off-viewport elements, and page text extraction immediately after clicking).
- I tried exhaustively: clicking empty canvas, clicking on a drawn rectangle, clicking/double-clicking/off-center-clicking the pin itself, element-level clicks, Enter/Space on the pin, hovering, drag gestures, right-click (only showed a generic canvas context menu), keyboard Tab-walking to find a hidden input, waiting for delayed rendering, and a full page reload with a clean retry. In every case, no editable composer element ever mounts in the DOM (the only textboxes on the page are the page-color field and an API-key field).
- Because the composer never opens, I could not type "shipped ", trigger the ":" emoji typeahead, pick 🎉 from suggestions, or submit the comment. The Comments panel still shows "Open 0 / No comments."

The core flow — "click the canvas to open the composer" — is broken: the draft pin is placed but the composer UI never appears, blocking the entire commenting task.

verdict: not-approve
```
