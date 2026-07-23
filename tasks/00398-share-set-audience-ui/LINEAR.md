# DesignPen [sharing & collab]: 'share set audience' fails QA — 3/3 runs report broken workflow (00398-share-set-audience-ui)

Description:
The entire body of the Share dialog ("Share this file") is non-interactive, which makes it impossible to change the file's audience. Clicking the audience row "Only invited people" (or any other body row: "Anyone in <name> projects", the "can edit" permission, "Publish to Community", "Copy Dev Mode link", "Get embed code") does nothing, and even the email invite field cannot be focused — focus lands on a container DIV, indicating an invisible overlay or an inert body container swallowing pointer events. Keyboard Tab only cycles between the header's "Copy link" and "Close" buttons, which are the only working controls. Because the audience row never opens the share-settings view, the audience dropdown is unreachable and the "Only invited people" → "Anyone" → Save flow cannot be executed.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Click the "Share" button in the toolbar — the "Share this file" dialog opens with a "Who has access" section listing the audience row "Only invited people".
3. Click the audience row "Only invited people" (try the lock icon, the label text, the chevron ">", and the middle of the row).
4. Attempt to reach the share-settings view to change the audience dropdown from "Only invited people" to "Anyone" and click Save.
5. Also try clicking the email invite field, and press Tab repeatedly to check which dialog elements are focusable.

Actual Result:
- Clicking the audience row "Only invited people" does nothing — no navigation to share settings ever occurs, via coordinate clicks, accessibility-tree element references, single-click, double-click, or manual mouse-down/mouse-up sequences.
- The entire dialog body is non-interactive: clicking the email invite field fails to focus it (focus lands on a container DIV, indicating an invisible overlay or inert body swallowing pointer events); keyboard Tab only cycles between the header's "Copy link" and "Close" buttons.
- Every other body row ("Anyone in Parker projects", the "can edit" permission, "Publish to Community", "Copy Dev Mode link", "Get embed code") is equally unresponsive, while the header buttons work fine.
- A full page reload, reopening the dialog, and waiting for async loading do not help. The audience dropdown is therefore unreachable, so the audience cannot be changed to "Anyone" or saved.

Expected Result:
The Share dialog body should be interactive: clicking the audience row should open the share-settings view, where the audience dropdown can be changed from "Only invited people" to "Anyone" and confirmed with Save.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 3 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3f079423-922c-49c6-84ed-3b6f559d8d2c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_403c8046-c99e-47fe-ae05-0308f13ad0ba.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_42af838a-4273-4edd-a7c0-c152a53f24b8.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9bc06878-e8c1-416b-9c18-8a7b64978830.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bec9ff0c-9595-47a7-8a04-d6610d250d30.txt`

Agent report (verbatim tail of failing run):

```
I was unable to complete the task due to what appears to be a bug in the app. Here's a summary of what happened:

**What worked:**
1. ✅ Opened the Share dialog by clicking the "Share" button — the dialog appeared correctly, showing "Share this file" with the "Who has access" section listing the audience row "Only invited people".

**What failed:**
2. ❌ Clicking the audience row "Only invited people" did nothing. I tried extensively:
   - Clicking the row via coordinates (on the lock icon, the label text, the chevron ">", and the middle of the row), via accessibility-tree element references, single-click, double-click, and manual mouse-down/mouse-up sequences — no navigation to share settings ever occurred.
   - Diagnosis confirmed the entire dialog **body** is non-interactive: clicking the email invite field fails to focus it (focus lands on a container DIV, indicating an invisible overlay or inert body swallowing pointer events), and keyboard Tab only cycles between the header's "Copy link" and "Close" buttons — no body element is reachable.
   - Every other body row ("Anyone in Parker projects", the "can edit" permission, "Publish to Community", "Copy Dev Mode link", "Get embed code") is equally unresponsive, while the header buttons (Copy link, Close) work fine.
   - A full page reload, reopening the dialog, and waiting for potential async loading did not help.

Because the audience row never opens the share-settings view, the audience dropdown could not be reached, so I could not change it from "Only invited people" to "Anyone" or click Save.

**What went wrong:** The Share dialog's body is completely inert (clicks and keyboard focus are blocked, likely by an overlay or an inert/disabled content container), making the "enter share settings → change audience → Save" flow impossible to execute.

verdict: not-approve
```
