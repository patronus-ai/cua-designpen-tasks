# DesignPen [text & typography]: 'text vertical trim' fails QA — 3/5 runs report broken workflow (00316-text-vertical-trim-ui)

Description:
The vertical trim feature itself works (Type settings popover → Basics tab → second Vertical trim option sets cap height, tightening the layer's bounding box from 68x17 to 68x11), but the session is unstable: while working, the app tab twice spontaneously navigated to about:blank, wiping the in-memory document. The app does not persist the document across reloads — a reload also loses all layers — so each blanking forced the entire task to be redone. The agent could only complete the workflow reliably in a fresh browser window.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create a text layer with the text "Tight crop" using the Text tool.
3. With the layer selected, open the Type settings popover via the sliders button (tooltip "Type settings") at the end of the Alignment row in the Typography section of the Design panel.
4. In the Basics tab, select the second Vertical trim option (cap height).
5. Keep working in the tab and watch for it spontaneously navigating to about:blank; also reload the page to check document persistence.

Actual Result:
- The app tab twice spontaneously navigated to about:blank mid-task, wiping the in-memory document and forcing the task to be redone multiple times.
- The document does not persist across reloads — reloading also loses all layers.
- The feature steps themselves work: text creation, the Type settings popover, and the cap-height trim (highlighted toggle; bounding box tightens from 68 x 17 to 68 x 11) all functioned correctly, verified in a fresh, stable browser window.

Expected Result:
The app tab should never spontaneously navigate to about:blank, and the document should survive (or be recoverable after) a reload so completed work is not lost.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 completed runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_132bfb84-e2fa-4e45-b232-45c404e380df.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_260f0cdf-26d0-48f4-8b9a-6ab7eb4a361b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_558e9d61-ee5d-4963-bc6c-fbb78ebfe8d2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5a2796cd-100c-4df5-946a-75458d60f19c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_787e13eb-69f8-419c-8da7-db21ad5295b4.txt`

Agent report (verbatim tail of failing run):

```
The task is now complete and stable in the active window. Final state confirmed:

- **Text layer created**: A text layer named "Tight crop" exists in the Layers panel and displays "Tight crop" on the canvas.
- **Type settings popover**: Opened via the sliders button (tooltip "Type settings") at the end of the Alignment row in the Typography section of the Design panel.
- **Vertical trim set to cap height**: In the Basics tab, the second Vertical trim option (cap height) is selected — confirmed by the highlighted toggle and the text layer's bounding box tightening from 68 × 17 to 68 × 11 (trimmed from cap height to baseline).

However, the session was not problem-free: while working, the app tab twice spontaneously navigated to about:blank, wiping the in-memory document (the app does not persist the document across reloads, which I confirmed — a reload also loses all layers). This forced me to redo the entire task multiple times. I finally completed it in a fresh browser window, which remained stable, and verified the end state there. The required steps themselves all functioned correctly (text creation, popover, cap-height trim), but the unexplained tab-blanking glitch and lack of persistence were real blockers during execution.

verdict: not-approve
```
