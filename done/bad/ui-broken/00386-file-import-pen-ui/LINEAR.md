# DesignPen [vector editing]: 'file import pen' fails QA — 5/5 runs report broken workflow (00386-file-import-pen-ui)

Description:
Main menu > File > Open… fails silently: clicking the menu item just closes the menu and no file picker ever appears — neither an in-app modal nor any `<input type="file">` element exists in the DOM/accessibility tree at any point, so a .pen file can never be selected or imported. The Ctrl+O shortcut and keyboard activation of the menu item fail the same way, with no error message, no new tab/window, and no delayed dialog. The "Back to files" menu item was also non-functional during testing. The menu structure itself renders correctly (File submenu shows New, Open… (Ctrl+O), Save, Save as…, etc.).

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Main menu via the OpenPencil logo button in the top-left corner.
3. Open the File submenu.
4. Click "Open… (Ctrl+O)".
5. Also try the Ctrl+O keyboard shortcut and keyboard activation of the menu item (arrow keys + Enter), waiting a few seconds after each attempt.

Actual Result:

- Clicking "Open…" simply closes the menu; no file picker ever appears.
- All variants failed: direct-coordinate clicks (multiple times), accessibility-tree reference activation, Ctrl+O, keyboard navigation + Enter, and waiting up to 3 seconds for a delayed dialog.
- No dialog, modal, or `<input type="file">` element exists in the DOM/accessibility tree at any point; no new tabs/windows open; no error messages appear.
- Nothing is imported — the document remains "Untitled" with an empty Page 1 and no layers.
- The "Back to files" menu item was also non-functional during testing.

Expected Result:
Invoking Main menu > File > Open… (or Ctrl+O) should present a file picker allowing the user to select a .pen design file from disk and import it into the app.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1c652533-5f5a-402c-b789-405b83334201.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_37bd0524-f4f7-4b19-8d5d-d0b7c0e6fed1.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dc2663e4-9426-4309-a586-609b3e19803d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ed5b39c7-3a33-419e-a354-9ce238bbd181.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fb2d4fed-f492-4399-b8e1-736c39f86b98.txt`

Agent report (verbatim tail of failing run):

```
I've completed my testing of the .pen file import flow. Here's a summary of what happened:

**Steps performed:**
1. ✅ Opened the Main menu via the OpenPencil logo button in the top-left corner — the menu opened correctly with entries (Back to files, Actions…, File, Edit, View, Object, Text, Arrange, …).
2. ✅ Opened the **File** submenu — it correctly displayed: New (Ctrl+N), **Open… (Ctrl+O)**, Save, Save as…, Export selection…, Export frames to PDF…, Auto-save to local file, Close tab.
3. ❌ Clicked **Open…** — the menu simply closed and **no file picker ever appeared**.

**Troubleshooting attempts (all failed to produce a file picker):**
- Clicked "Open…" by direct coordinates (multiple times) and via its accessibility-tree reference
- Used the Ctrl+O keyboard shortcut
- Activated the menu item via keyboard navigation (arrow keys + Enter)
- Waited up to 3 seconds after each attempt for a delayed dialog
- Inspected the DOM/accessibility tree for any dialog, modal, or `<input type="file">` element — none exists at any point
- Checked for newly opened tabs/windows — none
- Checked the page for error messages — none

**Result:** The "Open…" action fails silently. No file picker (neither an in-app modal nor any interactable chooser) is ever presented, so it was impossible to select a .pen file, and nothing was imported — the document remains "Untitled" with an empty Page 1 and no layers. Additionally, the "Back to files" menu item was also non-functional during testing.

The core requirement of the task — selecting a .pen file in the file picker — could not be performed because the file picker never opens after invoking Main menu > File > Open….

verdict: not-approve
```
