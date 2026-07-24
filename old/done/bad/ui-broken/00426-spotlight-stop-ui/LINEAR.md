# DesignPen [sharing & collab]: 'spotlight stop' fails QA — 5/5 runs report broken workflow (00426-spotlight-stop-ui)

Description:
Spotlight start/stop itself works correctly, but the feature is unreachable through the normal UI because of a toolbar layout bug in the default layout: the avatar button is visually clipped/overlapped by the right Design panel, and clicking it there never opens the avatar popover (no popover element is even added to the DOM — only a tooltip appears). The adjacent "Present" button and a neighboring toolbar button render as invisible blank space. The flow only becomes accessible after hiding the UI panels with Ctrl+\, where the compact floating toolbar shows the avatar fully; from there "Spotlight me" starts presenting and "Stop spotlight" stops it cleanly. Fix the default-layout toolbar clipping so the avatar popover opens without the Ctrl+\ workaround.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. In the default layout, click your own avatar (e.g. "Morgan (you)") in the toolbar — try coordinate clicks, element-ref clicks, double-click, keyboard Enter/Space, and slow press-and-release. The popover does not open (only a tooltip).
3. Workaround to reach the feature: press Ctrl+\ to hide the UI panels; in the compact floating toolbar the avatar is fully visible.
4. Click the avatar — the avatar popover opens with the "Spotlight me" toggle.
5. Click "Spotlight me" to start presenting (blue viewport border, "Waiting for followers..." banner, dashed spotlight ring, toggle reads "Stop spotlight").
6. Click "Stop spotlight" to stop presenting.

Actual Result:
- In the default layout, clicking the avatar repeatedly fails to open the popover: "only a tooltip ever appeared, and DOM inspection confirmed no popover was rendered." The avatar is visually clipped by the right Design panel, and the adjacent "Present" button is rendered invisible (blank area next to the avatar).
- After hiding the panels with Ctrl+\, the flow works: "Spotlight me" starts presenting (blue viewport border, "Waiting for followers..." banner with Cancel, dashed spotlight ring, toggle switches to "Stop spotlight"), and "Stop spotlight" stops it cleanly (border and banner disappear, toggle reverts to "Spotlight me").
- The primary path is broken and requires the Ctrl+\ workaround.

Expected Result:
In the default layout, clicking the toolbar avatar should open the avatar popover so Spotlight can be started and stopped without hiding the UI panels; the "Present" button should also render visibly.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_110e9096-9418-4a53-a452-51d1d6821cb5.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3f61dc28-3890-468d-a025-251e39d71af1.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6c9689ea-9484-4caa-8c2b-5a00a3348093.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7ca5c59c-4930-431a-b7fb-3660fba595f5.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_be16f7d7-8bd6-4e4d-adc7-e4e18761aef2.txt`

Agent report (verbatim tail of failing run):

```
The task flow is complete and the UI is restored to its original state. Here's a summary of what happened:

**What I did:**
1. Attempted to open the avatar popover by clicking the "Morgan (you)" avatar in the default layout — repeatedly failed (coordinate clicks, element-ref clicks, double-click, keyboard Enter/Space, slow press-and-release; only a tooltip ever appeared, and DOM inspection confirmed no popover was rendered).
2. Discovered the avatar is visually clipped by the right Design panel in the default layout, and the adjacent "Present" button is rendered invisible (blank area next to the avatar).
3. As a workaround, I hid the UI panels with Ctrl+\ — in the compact floating toolbar the avatar is fully visible, and clicking it successfully opened the avatar popover with the "Spotlight me" toggle.
4. Clicked **"Spotlight me"** → presenting started successfully (blue viewport border, "Waiting for followers..." spotlight banner with Cancel, dashed spotlight ring around the avatar, and the toggle switched to "Stop spotlight").
5. Clicked **"Stop spotlight"** (toggle off) → presenting stopped cleanly (border and banner disappeared, toggle reverted to "Spotlight me").
6. Closed the popover and restored the full UI with Ctrl+\.

**Problems encountered:** The spotlight start/stop functionality itself works correctly, but there is a real bug in the default layout: the avatar button is clipped/overlapped by the right panel and its popover never opens when clicked there (no popover element is even added to the DOM), making the Spotlight feature unreachable through the normal UI. It only became accessible after hiding the UI panels via Ctrl+\. Additionally, the "Present" button and a neighboring toolbar button are invisible (rendered as blank space) in the default top bar.

Because the primary path was broken and required a workaround, I can't call this a smooth pass.

verdict: not-approve
```
