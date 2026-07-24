# DesignPen [context menu]: 'right-click Copy → Paste to replace' fails QA — 5/5 runs report broken workflow (00109-paste-to-replace-ui)

Description:
The context-menu "Copy" command does not actually populate the clipboard, so the subsequent "Paste to replace" command fails with a red error banner: "Clipboard has no design content to paste." Agents reproduced the exact flow (right-click a shape > Copy, then select another shape, right-click > Paste to replace) multiple times per run — including with deliberate waits to rule out timing — and it failed consistently. The keyboard shortcut Ctrl+C works correctly: after Ctrl+C, "Paste to replace" swaps the target shape for a copy as expected. One run also observed that using right-click Copy even wipes out content previously copied via Ctrl+C. The clipboard subsystem and the "Paste to replace" feature itself are fine; the defect is isolated to the context-menu "Copy" action, which closes the menu without error but never writes the selection to the clipboard.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a circle (Ellipse tool) on the canvas.
3. Right-click the circle and choose "Copy" (the menu closes with no visible error).
4. Draw a rectangle with the Rectangle tool and select it.
5. Right-click the rectangle and choose "Paste to replace".

Actual Result:

- Step 5 fails with a red error banner: "Clipboard has no design content to paste." The rectangle is not replaced.
- Reproducible on every attempt (agents retried the exact flow 2-3 times per run, including a 1.5-second wait between Copy and Paste to replace).
- Control test: after right-click "Copy", Ctrl+V also pastes nothing (and clears content previously copied via Ctrl+C), confirming the context-menu Copy never populates the clipboard.
- Workaround: copying with keyboard Ctrl+C instead, then "Paste to replace", works and correctly swaps the rectangle for a copy of the circle.

Expected Result:
Right-click > "Copy" should place the selected object on the design clipboard exactly like Ctrl+C does, so that "Paste to replace" (and Ctrl+V) can consume it and swap the selected shape for the copied one.

Estimate: S (2 points) — the context-menu Copy handler is not wired to the same clipboard write path as the Ctrl+C shortcut; fix is scoped to one menu action.

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_06855f12-4645-46d2-8647-f672cca18c4e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_397e841c-ef30-4d1b-902b-887589926dbf.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8c95659b-8ffe-460a-b8dc-8dbea2439c16.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3340aa5b-4466-4ea1-9ee1-8b56038606a2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_361328eb-b83e-43a7-b437-7a0fd659f18f.txt`

Agent report (verbatim tail of failing run):

```
The task's end goal has been achieved — the rectangle was swapped out for a copy of the circle (the canvas now shows two identical circles, and the layers panel shows two "Ellipse 1" entries with no rectangle). However, I hit a real problem along the way.

**What I did:**
1. Drew a circle (150×150 ellipse). ✓
2. Right-clicked it and chose **Copy** (menu closed with no visible error). ✓
3. Drew a rectangle and selected it. ✓
4. Right-clicked the rectangle and chose **Paste to replace** → ❌ failed with the error **"Clipboard has no design content to paste."**

**The problem:** The right-click **Copy** did not actually populate the clipboard. I retried the exact right-click Copy → Paste to replace sequence a second time and got the same "Clipboard has no design content to paste" error. I only managed to complete the swap by using the **Ctrl+C** keyboard shortcut instead of the right-click Copy — after Ctrl+C, "Paste to replace" worked and the rectangle was correctly replaced by a copy of the circle.

**Confirmation:** To rule out a one-off glitch, I ran a controlled test: I recolored a circle red, right-click **Copied** it, drew a fresh rectangle, and chose **Paste to replace** — it failed again with the same "Clipboard has no design content to paste" error (and did not paste a red circle). This definitively confirms the right-click **Copy** command does not feed the "Paste to replace" flow; only the keyboard Ctrl+C does. (I undid the test changes to leave the document in the correct final state.)

So while the rectangle did ultimately get replaced by a copy of the circle, the specific flow the task asked for — **right-click > Copy** followed by **Paste to replace** — is broken and throws an error; I had to use a Ctrl+C workaround to get it to work.

verdict: not-approve
```
