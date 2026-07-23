# DesignPen [text & typography]: 'type letter case features' fails QA — 3/5 runs report broken workflow (00321-type-letter-case-features-ui)

Description:
Enabling the small caps OpenType feature (Type settings popover → Details tab → Letter case) ultimately works, but the surrounding UI is broken enough that the flow fails: at a 1280x720 viewport the right Design panel overflows the window, so the sliders-icon "Type settings" button is clipped off-screen and unreachable by normal clicks. Interacting with the font family control (at 80% browser zoom) crashed the page to `about:blank` with full document loss. Additionally, clicking the font family row often opens the "Apply variable" popup instead of the font picker depending on click position, and the "Font does not support..." tooltip on the disabled small caps option is clipped and unreadable.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer with the text "Chapter One".
3. In the Typography section of the right Design panel, locate the sliders-icon button (tooltip "Type settings") at the end of the alignment row — note it is clipped off the right edge of the viewport.
4. Open the Type settings popover and switch to the Details tab; the small caps option in the Letter case row is disabled for the default font (Inter) with a clipped "Font does not support..." tooltip.
5. Click the font family row to switch the layer to a font that supports small caps (e.g. Proxima Nova) — clicking parts of the row opens the "Apply variable" popup instead of the font picker.
6. Interact with the font family control (reproduced at 80% browser zoom) — the page can crash to `about:blank`, losing the document.
7. If the app survives, enable the small caps ("Aɢ") option in Type settings → Details → Letter case.

Actual Result:

- While interacting with the font family control, the page crashed to `about:blank` and the document state was lost; the app had to be reloaded and the text layer recreated from scratch.
- At 1280x720 the right Design panel is wider than the available space, so the Type settings sliders button is clipped off-screen and could only be reached via element-based scrolling / zooming tricks.
- Clicking the font family row repeatedly opened the "Apply variable" popup instead of the font picker, depending on the exact click position.
- The "disabled small caps" tooltip ("Font does not support...") was clipped and unreadable.
- Once reached, the feature itself worked: with Proxima Nova selected, the small caps option applied and the canvas rendered "Cʜᴀᴘᴛᴇʀ Oɴᴇ".

Expected Result:
The Type settings button and the rest of the Design panel fit (or scroll accessibly) within a 1280x720 viewport, the font family row reliably opens the font picker, tooltips render fully, and interacting with the font family control never crashes the app or loses the document.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_740d509d-c96f-4acd-b64b-de2221af847f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ab8a196f-5674-4824-9c31-f15d2dff58fa.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ad7f82d0-3d8c-4b3b-8723-1f9e9e28c63e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c7bd5f9f-6969-4548-aa11-d24f76ba9408.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f7e10b6e-a9de-4d17-af86-850819775628.txt`

Agent report (verbatim tail of failing run):

```
The task has been completed successfully. Final state:

1. **Text layer created**: A text layer with the text "Chapter One" exists (visible in the Layers panel and on canvas).
2. **Font check**: The default font (Inter) did **not** support small caps — the small caps option in Type settings → Details → Letter case was grayed out/disabled (with a "Font does not support..." tooltip). I therefore switched the layer's font to **Proxima Nova**, which does support it.
3. **Type settings popover**: Opened via the sliders-icon button (tooltip "Type settings") at the end of the Typography section's alignment row.
4. **Details tab**: Switched to the Details tab and clicked the small caps ("Aɢ") option in the Letter case → Case row. The popover preview and the canvas now render the text as "Cʜᴀᴘᴛᴇʀ Oɴᴇ" in small caps, and the option shows as selected.

However, the run was not smooth — I hit several problems along the way:
- **App crash / data loss**: While interacting with the font family control (at 80% browser zoom), the page crashed to `about:blank` and the document state was lost; I had to reload the app and recreate the text layer from scratch.
- **Clipped UI**: At the 1280×720 viewport, the right Design panel is wider than the available space, so the Type settings sliders button was clipped off-screen and could only be reached via element-based scrolling / zooming tricks.
- **Confusing click targets**: Clicking the font family row repeatedly opened the "Apply variable" popup instead of the font picker, depending on the exact click position, and the "disabled small caps" tooltip was clipped and unreadable.

verdict: not-approve
```
