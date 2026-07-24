# DesignPen [sharing & collab]: 'spotlight me' fails QA — 5/5 runs report broken workflow (00424-spotlight-me-ui)

Description:
The Spotlight feature itself works, but a layout/occlusion bug at the default 1280x720 viewport blocks the normal entry path. The toolbar avatar button is clipped/occluded by the right properties panel and the invisible panel-resize handle sitting on top of it (only ~4px of the avatar visible), so direct clicks and keyboard activation (Tab focus + Enter/Space) fail to open the collaborators popover. Only after resizing the right panel (keyboard-focusing the panel-resizer separator and using arrow keys) does the layout reflow, after which clicking the avatar opens the popover and "Spotlight me" successfully starts presenting. Fix the toolbar/panel layering so the avatar is fully visible and clickable at 1280px width.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Locate your own avatar button in the top toolbar (at this viewport it is clipped/occluded by the right properties panel; only a ~4px sliver is visible).
3. Click the avatar (coordinate clicks and element-ref clicks), or Tab-focus the avatar button and press Enter/Space — the collaborators popover does not open.
4. Workaround to reach the feature: keyboard-focus the panel-resizer separator and press arrow keys to resize the right panel so the avatar becomes fully visible.
5. Click the avatar — the collaborators popover opens; click "Spotlight me" on your own row.

Actual Result:
- In the default layout, repeated direct clicks on the avatar and keyboard activation all fail to open the collaborators popover; the avatar is occluded by the right panel and the invisible panel-resize handle.
- After resizing the right panel, the flow works: the popover opens, "Spotlight me" starts presenting — the button reads "Stop spotlight", the toolbar avatar gets a dashed blue "presenting" ring, the canvas gets a blue border, and a "Waiting for followers… / Cancel" banner appears (expected with no peers connected).
- The feature works but only via the panel-resize workaround; the normal "click your avatar" flow is blocked at this viewport size.

Expected Result:
At the default 1280x720 viewport, the avatar button should be fully visible and clickable, and one click should open the collaborators popover so "Spotlight me" can be toggled without resizing panels.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_462b4e68-4e79-4968-9c1b-d9b659e18270.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8c8f006f-7a59-4281-94a4-4dba2ed8b2f5.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8ff4f584-8188-4fa8-9b4c-a00dd52d3101.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b240e4f6-3bb6-45cd-9af7-c0e18b099c66.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bb2d75b0-fc84-407d-987c-b02e33bd76dd.txt`

Agent report (verbatim tail of failing run):

```
The task's end state is achieved. Verification of the final state:

- **Avatar popover**: Opened, showing my row "Finley (you)" with the red "F" avatar
- **Spotlight**: Turned ON — the button on my row now reads "Stop spotlight"
- **Presenting indicators**: My toolbar avatar has a dashed blue "presenting" ring, the canvas has a blue border, and a "Waiting for followers… / Cancel" banner is shown (expected behavior with no peers connected)

**Summary of what happened:**

I eventually completed the task, but it did not go smoothly. At the default 1280×720 viewport, the avatar button in the toolbar was clipped/occluded by the right properties panel and the invisible panel-resize handle sitting on top of it — only a ~4px sliver of the red avatar was visible. Repeated direct clicks on the avatar (coordinate clicks and element-ref clicks), as well as keyboard activation (focusing the avatar button via Tab and pressing Enter/Space), all failed to open the collaborators popover in that state.

The workaround: I keyboard-focused the panel-resizer separator and used arrow keys to resize the right panel, which caused the layout to reflow so the avatar became fully visible. After that, clicking the avatar opened the collaborators popover immediately, and clicking "Spotlight me" on my own row successfully started presenting ("Stop spotlight" + waiting-for-followers banner confirmed).

So the feature itself works, but there's a layout/occlusion bug at this viewport size that blocks the normal "click your avatar" flow until the panel is resized.

verdict: not-approve
```
