# DesignPen [comments]: 'comments sidebar' fails QA — 5/5 runs report broken workflow (00442-comments-sidebar-ui)

Description:
In the DesignPen/OpenPencil design app, comment creation is broken: clicking the canvas with the Comment tool drops a blue draft pin ("Draft comment"), but the comment composer (text input + submit button) never appears — no input/textarea ever mounts in the DOM. The Comments tab in the right-hand Properties panel itself works (it auto-opens when the Comment tool activates and shows the list view with "Show resolved" toggle and Open / Resolved / All filters), but because nothing can be typed or submitted, the list permanently shows "No comments" (Open 0). Keystrokes after placing a pin are swallowed as global tool shortcuts (e.g., "s" switched tools and discarded the draft). A secondary layout bug: the Comments panel is clipped at the right edge of the 1280px viewport, visibly cutting off the "All" filter tab.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Activate the Comment tool from the bottom toolbar (it highlights blue); the Comments tab in the right-hand Properties panel auto-opens.
3. Click on the canvas to place a comment pin — a blue "Draft comment" pin appears.
4. Attempt to type "sidebar check" into the comment composer and submit it.
5. Open the Comments tab in the right-hand Properties panel and check the list of comments.

Actual Result:
- The comment composer (text input + submit button) never appears after placing the draft pin; no input/textarea ever mounts in the DOM (verified via repeated accessibility-tree checks, including off-viewport elements).
- Single click, double click, slow click, clicking the pin directly (by coordinates and element ref), hovering, dragging, keyboard activation (Tab to the pin, Enter, Space), and placing pins on empty canvas or inside a frame all fail to open a composer.
- Typing does nothing — keystrokes are swallowed as global tool shortcuts (e.g., "s" switched tools and discarded the draft).
- No comment-related commands exist in the app menus or context menu; a full page reload does not help.
- The comments list permanently shows "No comments" (Open 0).
- Additionally, the right-hand Comments panel is clipped at the right edge of the 1280px viewport — the "All" filter tab is visibly cut off.

Expected Result:
Placing a comment pin should open a composer where the user can type "sidebar check" and submit; the submitted comment should then appear in the Comments tab list in the right-hand Properties panel. Opening/viewing the Comments tab already works; only comment creation is broken, and the panel should not overflow the 1280px viewport.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_31e4e961-38d2-481f-a086-d5a4e2118b47.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_47dc73c5-876c-4f13-a691-6e4827e80dfd.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b2b7c7b1-b002-4b59-b1ef-bc1462843b72.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_da2cba17-5e4c-4499-ae7a-7534cd3ff39b.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e5d833d6-984f-4124-88b9-f2c8061f6841.txt`

Agent report (verbatim tail of failing run):

```
I've completed my investigation. Here's a summary of what happened:

**What worked:**
- Activating the **Comment tool** from the bottom toolbar worked (it highlighted blue).
- The **Comments tab in the right-hand Properties panel** opened as expected — it auto-opened the moment the Comment tool became active, and I also clicked the tab header explicitly. It shows the comments list view with "Show resolved" toggle and Open / Resolved / All filters.

**What failed (blocker):**
- **Placing and submitting the comment "sidebar check" was impossible.** Clicking on the canvas with the Comment tool drops a blue draft pin ("Draft comment"), but the comment composer (text input + submit button) never appears. I verified this thoroughly:
  - No input/textarea ever mounts in the DOM (checked the accessibility tree repeatedly, including off-viewport elements).
  - Tried single click, double click, slow click (down–pause–up), clicking directly on the pin (by coordinates and by element ref), hovering, dragging the pin, keyboard activation (Tab/Shift+Tab to the pin, Enter, Space), and placing pins both on empty canvas and inside a frame.
  - Typing does nothing — keystrokes are swallowed as global tool shortcuts (e.g., "s" switched tools and discarded the draft).
  - No comment-related commands exist in the app menus or context menu, and no composer appears after a full page reload either.
  - As a result, the comments list permanently shows "No comments" (Open 0), so the comment could not be created or submitted.

**Additional bug noticed:** the right-hand Comments panel is clipped at the right edge of the 1280px viewport — the "All" filter tab is visibly cut off, indicating a layout overflow issue.

The second half of the task (opening/viewing the Comments tab) succeeded, but the primary goal — submitting a comment saying "sidebar check" — was blocked by what appears to be a broken comment composer: the draft pin is placed but the text entry UI never opens, making submission impossible.

verdict: not-approve
```
