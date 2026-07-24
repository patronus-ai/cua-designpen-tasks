# DesignPen [file handling]: 'file open' fails QA — 4/4 runs report broken workflow (00388-file-open-ui)

Description:
The "Open…" command in DesignPen's Main menu (Main menu > File > Open…, shortcut Ctrl+O / Cmd+O) is a silent no-op: activating it closes the menu but never presents a file picker, so an existing .fig file can never be opened from disk. No in-page picker dialog appears, no `<input type="file">` is ever added to the DOM, no new window/tab opens, and no error toast is shown. Menu wiring in general is functional — other menu actions (e.g. View > Zoom In, Zoom to 100%) execute correctly — so the failure is specific to the Open… action handler. Side observations from the same run: "Back to files" and the "Actions…/⌘K" palette also appeared inert.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Click the Main menu button (logo, top-left) and hover File — the submenu shows "Open… Ctrl+O".
3. Click the "Open…" menu item (or press Ctrl+O directly, or navigate the menu with arrow keys + Enter).
4. Watch for a file picker: check the screen, the DOM for any file input/dialog/modal, and for new tabs/windows.

Actual Result:
- The menu closes and no file picker ever appears — "no in-page picker dialog, no `<input type="file">` is ever added to the DOM, no new window/tab opens, no error toast or notification is shown, and the app state never changes."
- Repeating the activation via mouse click (coordinates and accessibility ref, 3 times), Ctrl+O (twice), and pure keyboard menu navigation gives the same result.
- Because no picker appears, it is impossible to pick a .fig file, and no existing design can be opened from disk.

Expected Result:
Activating Main menu > File > Open… (or Ctrl+O) should present a file picker that lets the user select a .fig file from disk, and the selected file should load into the editor.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_35be117f-34f7-4582-95c5-d037c6a0bd38.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_53907f6d-f7af-4d00-84a7-97887ed7bf75.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a37f44a7-2c2b-45f2-8588-927b12f3a277.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a5faefd4-d816-4f43-b370-3340051a6bc7.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ef11a99e-563a-4917-b989-20538b17c34a.txt`

Agent report (verbatim tail of failing run):

```
I attempted the requested flow thoroughly. Here's a summary of what I did and found:

**Steps taken:**
1. Loaded the OpenPencil editor at `http://cua_designpen.web` (empty "Untitled" file).
2. Opened the **Main menu** (logo button, top-left) → hovered **File** → the submenu correctly shows **"Open… Ctrl+O"**.
3. Activated **Open…** multiple ways:
   - Mouse click on the menu item (by coordinates and by accessibility ref) — tried 3 times
   - Keyboard shortcut **Ctrl+O** (the environment's equivalent of Cmd+O) — tried twice
   - Pure keyboard menu navigation (arrows + Enter)
4. After each attempt I checked for a picker: took screenshots, read the full accessibility tree (including off-viewport elements), searched for any file input/dialog/modal, checked for new tabs/windows, and waited for delayed rendering.

**Result:** The menu closes and **no file picker ever appears** — no in-page picker dialog, no `<input type="file">` is ever added to the DOM, no new window/tab opens, no error toast or notification is shown, and the app state never changes. As a control test, I verified other menu actions do work (View > Zoom In and Zoom to 100% executed correctly and visibly changed the canvas), so the menu wiring itself is functional — the **Open… action specifically fails to present any picker**. Consequently it was impossible to "pick a .fig file in the picker," and no existing .fig design could be opened from disk. (Side observations: "Back to files" and the "Actions…/⌘K" palette also appeared inert.)

**What went wrong:** Main menu > File > Open… (and Ctrl+O) silently does nothing — the file picker never opens in this environment, blocking the entire task of selecting and opening a .fig file.

verdict: not-approve
```
