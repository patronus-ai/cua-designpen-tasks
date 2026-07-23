# DesignPen [view & UI toggles]: 'toggle ui' fails QA — 4/5 runs report broken workflow (00160-toggle-ui-ui)

Description:
Main menu > View > "Toggle UI" (Ctrl+\, the app's name for Show/Hide UI) hides only the side panels, never all editor chrome. In the UI-hidden state the left sidebar (Pages/Layers + File/Assets/Tools/Variables rail) and right Design panel disappear, but the bottom tool palette (select, frame, shape, pen, text, comment, etc.) remains fully visible and interactive — it even reappears on mouse movement while UI is supposedly hidden — and two floating chrome bars persist: a top-left pill (main-menu button, "Untitled" title, sidebar toggle) and a top-right pill (avatar, 100% zoom, Share/Present). The promised "only the canvas remains visible" outcome is never achieved.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Main menu (logo button, top-left) > View > "Toggle UI" (listed with the Ctrl+\ shortcut).
3. Observe which editor chrome remains visible; move the mouse over the canvas.
4. Press Ctrl+\ to toggle the state back and forth and observe the same behavior via the shortcut.

Actual Result:
- The menu item and Ctrl+\ shortcut both toggle a "UI hidden" state: the left sidebar (Pages/Layers + File/Assets/Tools/Variables rail) and the right Design panel are hidden.
- The bottom toolbar is NOT hidden — the tool palette (select, frame, shape, pen, text, comment, etc.) remains fully visible and interactive, and it reappears on mouse movement while the UI is supposedly hidden; pressing Ctrl+\ with the toolbar showing hides the side panels but leaves the toolbar on screen.
- Two floating chrome bars also persist: a top-left pill (main-menu button, "Untitled" title, sidebar toggle) and a top-right pill (avatar, 100% zoom, Share/Present buttons).

Expected Result:
Invoking View > Toggle UI (Ctrl+\) should hide all editor chrome — panels, toolbars, and floating menu/title/share bars — leaving only the canvas visible.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_02e7029f-231b-4d3c-9c21-67b022e5b4ea.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3e71a1a3-777b-471c-99eb-690af5dbf45d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_68e9b369-f672-4c71-b0ee-0ee13a99a1a4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bcec1573-5227-440e-a240-d04cd757b74f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c13d8368-285f-4cd8-88cb-49ad1abf63e6.txt`

Agent report (verbatim tail of failing run):

```
I've completed the task as specified and thoroughly verified the behavior. Here's a summary of what I did and found:

**Actions taken:**
1. Opened the Main menu (logo button, top-left) → **View** → clicked **"Toggle UI"** (this app's name for Show/Hide UI, listed with the `Ctrl+\` shortcut, the platform equivalent of `Cmd+\`).
2. Verified the keyboard shortcut `Ctrl+\` toggles the same state back and forth, and left the editor in the **UI-hidden state** as requested.

**Results:**
- ✅ The menu item exists and works as a toggle; the shortcut works too.
- ✅ The left sidebar (Pages/Layers + File/Assets/Tools/Variables rail) and the right Design panel are hidden.
- ❌ **The bottom toolbar is NOT hidden.** The tool palette (select, frame, shape, pen, text, comment, etc.) remains fully visible and interactive in hidden-UI mode — it even reappears on mouse movement while the UI is supposedly hidden, and pressing `Ctrl+\` with the toolbar showing hides the side panels but leaves the toolbar on screen.
- ❌ Two floating chrome bars also persist: a top-left pill (main-menu button, "Untitled" title, sidebar toggle) and a top-right pill (avatar, 100% zoom, Share/Present buttons).

So while I invoked the feature exactly as instructed and the app is now in its "UI hidden" state, the promised outcome — "only the canvas remains visible" — is never achieved: the toolbar (explicitly named in the requirement) and floating bars stay visible. This is a bug in the Show/Hide UI implementation rather than something I could work around via the specified command.

The task did not go smoothly: View > Toggle UI (Ctrl+\) hides the side panels but fails to hide the bottom toolbar and floating title/share bars, so editor chrome remains visible instead of only the canvas.

verdict: not-approve
```
