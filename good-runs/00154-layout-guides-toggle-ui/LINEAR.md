# DesignPen [view & UI toggles]: 'layout guides toggle' fails QA — 5/5 runs report broken workflow (00154-layout-guides-toggle-ui)

Description:
The documented "Layout guides" toggle (Shift+G) is missing from the View menu entirely. The View menu contains only Zoom to 100%, Zoom to fit, Zoom to selection, Zoom In (Ctrl+=), Zoom Out (Ctrl+-), Theme, Language, Toggle UI (Ctrl+\), and Performance profiler, and the item is absent from every other submenu (File, Edit, Object, Text, Arrange, Preferences) as well. The underlying feature itself works — pressing the bare Shift+G shortcut does hide/show layout guide overlays — so this is a missing menu entry, not a broken guide-rendering feature.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Main menu (logo button, top-left) > View and look for a "Layout guides" toggle (Shift+G).
3. Check the other submenus (File, Edit, Object, Text, Arrange, Preferences) for the item.
4. To confirm the underlying feature exists: create a test frame, add a layout guide from the Design panel (a red grid overlay renders), then press Shift+G.

Actual Result:
- There is no "Layout guides" toggle (Shift+G) in the View menu — the menu contains only Zoom to 100%, Zoom to fit, Zoom to selection, Zoom In (Ctrl+=), Zoom Out (Ctrl+-), Theme, Language, Toggle UI (Ctrl+\), Performance profiler. Verified twice (with nothing selected and with a frame carrying a layout guide selected).
- The item is absent from every other submenu (File, Edit, Object, Text, Arrange, Preferences).
- The bare Shift+G keyboard shortcut does work: with a layout guide added to a frame, pressing Shift+G hides the guide overlay.

Expected Result:
The View menu should contain a "Layout guides" menu item with the Shift+G shortcut that toggles canvas-wide layout guide overlay rendering, matching the working keyboard shortcut.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_37182559-3efd-4618-8070-a5c296da839f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_74d80d16-3035-40c9-aa93-9b65cf69693e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a456d69c-587b-46ac-aaa4-8eeccb9710c5.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_be7b4597-6763-4926-9918-d4475ea063b6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d9d25e3f-d616-4d02-9014-3f444acff1f8.txt`

Agent report (verbatim tail of failing run):

```
The canvas is completely clean — no guide lines render over it, and the document is back to its original empty state.

**Summary of what I found and did:**

1. **Checked the View menu** (main menu → View): it contains only *Zoom to 100%, Zoom to fit, Zoom to selection, Zoom In (Ctrl+=), Zoom Out (Ctrl+-), Theme, Language, Toggle UI (Ctrl+\), Performance profiler*. **There is no "Layout guides" toggle (Shift+G) in the View menu** — I verified this twice (with nothing selected and with a frame carrying a layout guide selected), and also searched every other submenu (File, Edit, Object, Text, Arrange, Preferences) — the item is absent everywhere.

2. **Verified the underlying feature state directly**: I created a temporary test frame and added a layout guide from the Design panel — a red grid overlay rendered, showing that guide rendering was initially **enabled** (guides would show). Pressing **Shift+G** successfully hid the guide overlay, confirming the keyboard shortcut works even though its menu entry is missing.

3. **Ensured the requested end state**: guide rendering is now toggled **off** (Shift+G left in the hidden state), and I cleaned up the test frame/guide via undo. The canvas renders no guide lines whatsoever.

**Problem encountered:** While the end state (no layout guide overlays rendering) is achieved, the task's specified control — a "Layout guides" toggle in the View menu with the Shift+G shortcut — does not exist in the app. The View menu is missing that menu item entirely, so the check could only be done via the bare keyboard shortcut and a manual rendering test, not via the documented menu toggle. This is a missing/broken menu feature.

verdict: not-approve
```
