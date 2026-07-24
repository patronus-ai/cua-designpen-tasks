# DesignPen [sharing & collab]: 'share open settings' fails QA — 3/3 runs report broken workflow (00396-share-open-settings-ui)

Description:
In the Share dialog ("Share this file", opened via the toolbar Share button), the audience rows under "Who has access" ("Only invited people", "Anyone in <name> projects") are inert despite showing a chevron ">" affordance that implies a sub-view. Clicking a row (any part: text, lock icon, chevron), double-clicking, and keyboard navigation all fail to open the share settings sub-view. The accessibility tree shows the rows are plain generic `div`s with no button role — unlike the dialog's working buttons (Close, Copy link, Invite) — and Tab order skips them entirely. Other chevron rows such as "Publish to Community" are equally unresponsive, indicating these sub-view rows are non-functional/unimplemented in this build.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Click the "Share" button in the top-right toolbar — the "Share this file" dialog opens with a "Who has access" section listing audience rows ("Only invited people", "Anyone in <name> projects").
3. Click the audience row "Only invited people" (try the row text, the lock icon, and the chevron ">"); also try double-click and Tab keyboard navigation.
4. Watch for a share settings sub-view to open.

Actual Result:
- Clicking the audience row does not open any share settings sub-view — no navigation ever occurs, regardless of click target (middle of the row, row text via element reference, lock icon, chevron), double-click, or clicking the other audience row.
- The rows are not keyboard focusable: Tab order skips them entirely.
- The accessibility tree confirms the audience rows are plain generic `div`s with no button role, and there is no hover affordance; other chevron rows like "Publish to Community" are equally unresponsive.

Expected Result:
Clicking an audience row in the Share dialog should open the share settings sub-view where the file's access/audience can be viewed and changed. The rows should be real buttons (focusable, with button role).

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 3 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_44428d74-c001-48a5-ba91-4645bfe1cf14.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_77c0a526-21f3-452c-98f0-6aaa79e06784.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8598420e-9cc3-469b-a0ca-533ff93a0123.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_97e62489-2579-4db8-91d1-058009797b1b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f9b26986-5aba-45b5-bf0a-b06036b2f4bf.txt`

Agent report (verbatim tail of failing run):

```
I've completed a thorough investigation. Here's a summary of what happened:

**What worked:**
- Opened the app at http://cua_designpen.web (OpenPencil design tool)
- Clicked the toolbar **Share** button in the top-right corner — the "Share this file" dialog opened correctly, showing an invite field, a "Who has access" section with audience rows ("Only invited people" and "Anyone in Kai projects"), and additional options (Publish to Community, Copy Dev Mode link, Get embed code)

**What failed:**
- Clicking the audience row ("Only invited people", which has a chevron `>` suggesting a sub-view) did **not** open any share settings sub-view. I tried:
  - Clicking the middle of the row, the row text (via element reference), the lock icon, and the chevron
  - Double-clicking the row
  - Clicking the other audience row ("Anyone in Kai projects")
  - Waiting after clicking in case of delayed rendering
  - Keyboard navigation — the rows are not focusable (Tab order skips them entirely)
- The accessibility tree confirms the audience rows are plain generic `div`s with no button role, unlike the real buttons in the dialog (Close, Copy link, Invite). There's no hover affordance on the rows either. Other chevron rows like "Publish to Community" are equally unresponsive, indicating these sub-view rows are non-functional/unimplemented in this build.

The Share dialog opens fine, but the audience row is inert — clicking it never opens the share settings sub-view, which blocks completing the requested flow. This appears to be a bug (non-interactive audience row despite the chevron affordance).

verdict: not-approve
```
