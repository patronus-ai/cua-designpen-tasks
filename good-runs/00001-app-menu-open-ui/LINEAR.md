# DesignPen [app menu]: 'app menu open' fails QA — 5/5 runs report broken workflow (00001-app-menu-open-ui)

Description:
The main application dropdown menu (opened via the "Open main menu" OpenPencil logo button at the left end of the toolbar) cannot be dismissed with the Escape key. The menu opens correctly and lists every expected section (Back to files, Actions, File, Edit, View, Preferences, Open in desktop app, AI balance, Help and account), but pressing Escape leaves the dropdown open — only clicking elsewhere on the canvas closes it. Standard menu UX expects Escape to dismiss an open dropdown, so the Escape key handler for this menu is missing or not wired up.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Click the main menu button (labeled "Open main menu", the OpenPencil logo button at the top-left end of the toolbar) to open the application dropdown menu.
3. Confirm the menu lists the expected sections: Back to files, Actions, File, Edit, View, Preferences, Open in desktop app, AI balance, and Help and account.
4. Press Escape to close the menu.

Actual Result:

- The menu opens and lists all expected sections (plus additional items: Object, Text, Arrange, and disabled entries for Vector, Plugins, Widgets, and Libraries).
- "Pressing **Escape did not close the menu** (verified twice; the dropdown remained open after each Escape press)."
- Clicking elsewhere on the canvas does dismiss the menu, so only one of the two standard closing methods works.

Expected Result:
Pressing Escape while the main application dropdown menu is open should dismiss the menu and return the app to its normal state, just as clicking elsewhere does.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1507f88f-a7b1-4a76-8528-ad2fb783832f.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_18cf0b37-b6bb-43c8-8d24-913b065af850.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5ef4af22-d0ed-4e13-81f7-644e5eeeee1d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9b493171-242a-4d42-a03a-c61e61703285.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ae9bfe88-8e5b-4d10-8123-fc608e03e0fc.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Here's a summary of what I did and found:

**Steps performed:**
1. **Opened the main menu** — Clicked the main menu button (labeled "Open main menu", the OpenPencil logo button at the top-left end of the toolbar). The application dropdown menu opened.

2. **Verified the menu contents** — All expected sections are present:
   - ✅ Back to files
   - ✅ Actions… (⌘K)
   - ✅ File
   - ✅ Edit
   - ✅ View
   - ✅ Preferences
   - ✅ Open in desktop app
   - ✅ AI balance
   - ✅ Help and account
   
   (The menu also contains additional items: Object, Text, Arrange, and disabled entries for Vector, Plugins, Widgets, and Libraries.)

3. **Closed the menu** — Pressing **Escape did not close the menu** (verified twice; the dropdown remained open after each Escape press). I then closed it by **clicking elsewhere** on the canvas, which worked — the menu dismissed and the app returned to its normal state.

**Issue encountered:** While the menu opened correctly and listed all expected sections, the Escape key — one of the two closing methods specified in the task — consistently failed to dismiss the dropdown. Only clicking elsewhere closed it. Standard menu UX (and the task itself) expects Escape to dismiss the menu, so this appears to be a bug in the application.

verdict: not-approve
```
