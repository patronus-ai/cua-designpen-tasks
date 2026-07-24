# DesignPen [clipboard / copy-paste]: 'clipboard paste' fails QA — 5/5 runs report broken workflow (00100-clipboard-paste-ui)

Description:
The canvas context-menu clipboard flow is broken: after copying a rectangle via right-click > Copy, choosing right-click > "Paste here" on empty canvas shows a red error toast "Clipboard access is blocked in this browser context" and pastes nothing. The agent's diagnostic shows the root cause: the context-menu Copy/"Paste here" actions rely on the async `navigator.clipboard` API, which is unavailable because the app is served over insecure HTTP; the keyboard shortcuts Ctrl+C/Ctrl+V use DOM clipboard events and work fine on the same content. The context-menu actions need to fall back to the DOM-event/internal clipboard path (or the menu items should be disabled) instead of failing with an error.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the rectangle tool from the bottom toolbar and drag on the canvas to draw one rectangle ("Rectangle 1").
3. Right-click the rectangle and choose "Copy" from the context menu (no error is shown at this step).
4. Right-click on empty canvas and choose "Paste here" (the item is enabled).

Actual Result:

- Clicking "Paste here" triggers a red error toast: "Clipboard access is blocked in this browser context".
- No rectangle is pasted — the Layers panel still shows only the single "Rectangle 1". The full copy/paste flow was retried three times with the same failure each time.
- Control test: keyboard Ctrl+C/Ctrl+V on the same rectangle worked perfectly and pasted a duplicate, confirming the failure is specific to the context-menu path using the async `navigator.clipboard` API on insecure HTTP.

Expected Result:
Right-click > Copy followed by right-click > "Paste here" should paste a copy of the rectangle at the clicked location, matching the behavior of the working Ctrl+C/Ctrl+V shortcuts, with no error toast.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3746d3ec-b5ec-4dd5-8f35-eb098bd73327.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7dbaf2b8-0294-4315-8370-f724f99983b3.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8a8fb31b-d470-43b6-8dbc-7815533786f7.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_925b11ea-1e4c-4dbb-bab7-4cf45b8d00ee.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ae7ad02c-8197-4608-98c0-59a6488036f9.txt`

Agent report (verbatim tail of failing run):

```
The error toast has auto-dismissed. I've completed all the requested steps and verified the outcome across three attempts.

**Summary of what I did:**

1. **Drew one rectangle** ✅ — Selected the rectangle tool from the bottom toolbar and dragged on the canvas, creating a 170×110 "Rectangle 1" (confirmed in the Layers panel and right-side Design panel).

2. **Right-click > Copy** ✅ — Right-clicked the rectangle; the context menu appeared and I clicked "Copy". No error was shown at this step.

3. **Right-click on empty canvas > "Paste here"** ❌ — The context menu appeared with "Paste here" enabled, but clicking it triggered a red error toast: **"Clipboard access is blocked in this browser context"**, and no rectangle was pasted (the Layers panel still showed only the single "Rectangle 1"). I retried this full copy/paste flow three times with the same failure each time.

**Diagnostic:** To isolate the issue, I tested keyboard shortcuts Ctrl+C/Ctrl+V — these worked perfectly, pasting a duplicate rectangle (which I then undid to keep state clean). This confirms the clipboard feature itself works via DOM clipboard events, but the context-menu "Copy"/"Paste here" actions rely on the async `navigator.clipboard` API, which is blocked in this browser context (the app is served over insecure HTTP, where that API is unavailable).

The specific flow requested — right-click > Copy followed by right-click > "Paste here" — consistently fails with an error and does not paste the rectangle.

verdict: not-approve
```
