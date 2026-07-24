# DesignPen [comments]: 'comment mention' fails QA — 5/5 runs report broken workflow (00438-comment-mention-ui)

Description:
The @-mention typeahead in comments cannot be exercised because the comment composer never opens. Activating the Comment tool works (the speech-bubble toolbar icon highlights blue and the right sidebar switches to the Comments panel), and clicking the canvas places a blue draft pin (a "Draft comment" button in the DOM), but no composer/text input ever appears — neither visually nor in the DOM. The accessibility tree (including off-viewport elements) contains no textbox, the bare "Draft comment" pin button has no children, and browser zoom-out to 64% confirmed nothing renders off-screen. Focus probes confirmed no editable element ever receives focus, so typing "@" to trigger the mention typeahead, selecting a person, and submitting are all impossible.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool by clicking the speech-bubble icon in the bottom toolbar.
3. Click the canvas to open the comment composer.
4. Attempt to type "@" to trigger the mention typeahead, select a person from the suggestions, finish the message with "please review", and submit.

Actual Result:

- A blue draft comment pin is placed at the click point (a "Draft comment" button appears in the DOM), but the composer never opens — no comment composer/text input ever appears, visually or in the DOM.
- Screenshots and magnified zooms around the pin show only the pin; the accessibility tree (including off-viewport elements) contains no textbox/composer — only the bare "Draft comment" pin button with no children; zooming the browser out to 64% confirmed nothing was rendered off-screen.
- Clicking, double-clicking, and hovering the pin; keyboard focus + Enter/Space; pressing Enter/letter keys/"@" (shift+2) with a draft pin active; drag-placement; placing pins on empty canvas vs. on a shape; a full page reload; and the Comments sidebar, context menus, main menu, and View menu all fail to open a composer.
- Focus probes confirmed no editable element ever receives focus, so the "@" mention typeahead, person selection, "please review" text, and submission were all impossible.

Expected Result:
Clicking the canvas with the Comment tool active should open a composer; typing "@" in it should show a mention typeahead from which a person can be selected as an inline @-mention, and the completed comment should submit successfully.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5d92bd05-9d67-4534-bfb9-c7ef8f7a70da.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7a064259-8b1b-4625-94b2-75ba4b81864b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_90479b0e-3d18-4009-8cac-0e77b8e62071.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9bbd5b1c-b66b-46f4-b7af-4b98802be30e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f267f7d5-c827-4cb9-b9c5-2aa00f70bfba.txt`

Agent report (verbatim tail of failing run):

```
I've exhaustively tested the comment flow. Here's a summary of what happened:

**What worked:**
1. ✅ **Activated the Comment tool** — clicking the speech-bubble icon in the bottom toolbar highlighted it blue and switched the right sidebar to the Comments panel (showing "Open 0 / Resolved 0 / All 0, No comments").
2. ✅ **Clicked the canvas** — a blue draft comment pin was placed at the click point (a "Draft comment" button appears in the DOM).

**What failed:**
3. ❌ **The composer never opened.** After placing the pin, no comment composer/text input ever appeared — neither visually nor in the DOM. I verified this thoroughly:
   - Screenshots and magnified zooms around the pin show only the pin, no input box.
   - The accessibility tree (including off-viewport elements) contains no textbox/composer — only the bare "Draft comment" pin button with no children.
   - Zooming the browser out to 64% confirmed nothing was rendered off-screen.
   - I tried clicking, double-clicking, and hovering the pin; keyboard focus + Enter/Space; pressing Enter/letter keys/"@" (shift+2) with a draft pin active; drag-placement; placing pins on empty canvas vs. on a shape; a full page reload with a clean retry; and checked the Comments sidebar, context menus, main menu, and View menu for any alternate composer entry point. Nothing opens a composer.
4. ❌ Consequently, typing "@" to trigger the mention typeahead, selecting a person, finishing with "please review", and submitting were all **impossible** — there is no editable field to type into (focus probes confirmed no editable element ever receives focus).

The Comment tool's click-to-compose flow is broken in this build: clicking the canvas creates a draft pin but the comment composer popup never renders, which blocks @-mentions and comment submission entirely.

verdict: not-approve
```
