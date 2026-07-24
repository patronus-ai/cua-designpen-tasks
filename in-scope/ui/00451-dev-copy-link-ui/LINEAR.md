# DesignPen [clipboard / copy-paste]: 'dev copy link' fails QA — 4/5 runs report broken workflow (00451-dev-copy-link-ui)

Description:
In the DesignPen/OpenPencil design app's Dev Mode, the "Copy link" control (chain-link icon in the code panel header) does not actually copy a shareable deep link to the clipboard, and no toast or confirmation is shown. The setup steps all work (draw a frame, toggle Dev Mode via the `</>` button, select the frame — the code panel header shows the frame with its controls). The agent verified the environment's clipboard works via native ctrl+c/ctrl+v, seeded the clipboard with marker text "Frame 1", clicked "Copy link" repeatedly with the frame selected, and pasting still produced the stale marker instead of a URL. Other copy controls in the Inspect panel (e.g., "Copy width: 300") also silently fail, suggesting the app's clipboard writes fail globally — likely `navigator.clipboard` being unavailable on this insecure `http://` origin with no fallback — without any user-facing error.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Frame tool from the toolbar and drag on the canvas to draw a frame ("Frame 1").
3. Switch to Dev Mode via the `</>` toggle on the right side of the bottom toolbar.
4. Select the frame on the canvas; the code panel header shows the frame with its controls.
5. Click the copy-link control — the chain-link icon in the code panel header (tooltip "Copy link").
6. Paste into a free-text input to inspect the clipboard contents.

Actual Result:
- The copy-link control does not copy anything: after seeding the clipboard with marker text "Frame 1", clicking "Copy link" (with the frame selected, multiple attempts), pasting still produced the stale marker "Frame 1" instead of a shareable URL.
- The app shows no toast/confirmation — its notifications region stays empty.
- Other copy controls in the Inspect panel (e.g., "Copy width: 300") also silently fail to write to the clipboard, indicating a global clipboard-write failure with no user-facing error.
- The environment's clipboard machinery itself works (native ctrl+c/ctrl+v of text in the layer-rename input round-trips correctly).

Expected Result:
Clicking the copy-link control in the Dev Mode code panel header should place a shareable deep link to the current selection on the clipboard and give the user confirmation, or surface an error if the copy fails. Clipboard writes should work (or have a fallback) on the insecure HTTP origin.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 runs failed (agent verdict: not-approve; 1 approved)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_24e3890c-81d4-44b0-92f5-736e53e3f617.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6ef3eab2-65fa-437b-b1e7-db2994eded7b.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8811b67a-515a-4ba4-81a9-8fc117eb9b54.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_970a4d67-221b-4d09-b25a-b3e69728de1d.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_df002902-1c80-4b2e-8151-f9159a06ff56.txt`

Agent report (verbatim tail of failing run):

```
All steps of the task were performed, and my cleanup left the document in a good state. Here's a summary of what happened:

**Completed actions:**
1. **Drew a frame** — used the Frame tool from the toolbar and dragged on the canvas, creating "Frame 1" (300 × 250).
2. **Switched to Dev Mode** — clicked the `</>` toggle on the right side of the bottom toolbar; the UI switched to Dev Mode (dark toolbar, "Ready for development" panel, Inspect/Code panel).
3. **Selected the frame** — clicked it on the canvas; the code panel header showed the frame with its controls.
4. **Clicked the copy-link control** — the chain-link icon in the code panel header (tooltip confirmed as "Copy link"); clicked it several times with the frame selected.

**Problem found:** The copy-link control does not actually copy anything. I verified this rigorously:
- Clipboard machinery itself works in this environment: selecting text in the layer-rename input and pressing ctrl+c → ctrl+v correctly round-trips the text ("Frame 1").
- I seeded the clipboard with that marker text, clicked the "Copy link" control again (frame selected), and pasted into a free-text input — the paste still produced the stale marker "Frame 1" instead of a shareable URL. Repeated tests gave the same result.
- The app shows no toast/confirmation (its notifications region stays empty), and other copy controls in the Inspect panel (e.g., "Copy width: 300") also silently fail to write to the clipboard — suggesting the app's clipboard writes fail globally (likely `navigator.clipboard` being unavailable on this insecure `http://` origin with no fallback), failing without any user-facing error.

So while the requested UI interaction was carried out exactly as specified, the control's actual effect — copying a shareable deep link to the selection — never happened.

verdict: not-approve
```
