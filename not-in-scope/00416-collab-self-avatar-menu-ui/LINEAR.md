# DesignPen [sharing & collab]: 'collab self avatar menu' fails QA — 5/5 runs report broken workflow (00416-collab-self-avatar-menu-ui)

Description:
Clicking your own avatar button in the top toolbar (e.g. `button "Skyler (you)"`, next to the Share button) never opens the collaborators popover — only the hover tooltip appears, and DOM/accessibility-tree inspection confirms no popover, menu, or dialog is ever mounted. At the 1280x720 viewport the avatar is partially clipped at the right-panel boundary (~x=1135) and the adjacent "Present" button is entirely hidden, so the toolbar overflows/clips and the clipping is the likely cause of the dead click target. The neighboring Share button works fine, proving the app's click handling and overlay system are otherwise functional.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Locate your own avatar button in the top toolbar, right side, next to the Share button (note: it is partially clipped at the right-panel boundary and the adjacent "Present" button is hidden).
3. Click the avatar — via its accessibility reference, via coordinates within the visible portion, double-click, or focus it and press Enter/Space.
4. Watch for a collaborators popover to open.

Actual Result:
- In every case only the hover tooltip (e.g. "Skyler (you)") appears; "no popover, menu, or dialog is ever mounted" in the DOM, confirmed by screenshots and full accessibility-tree reads after each click.
- The avatar button is partially clipped at the right-panel boundary (~x=1135) and the adjacent "Present" button is entirely hidden — the toolbar overflows/clips at the 1280px viewport width.
- Sanity check: the neighboring "Share" button works perfectly (its dialog opened and listed "Skyler (you) — can edit"), so the failure is specific to the avatar button.

Expected Result:
Clicking your own toolbar avatar should open the collaborators popover. The toolbar should not clip the avatar or hide the "Present" button at a 1280px-wide viewport.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0cedc874-7540-459a-a508-27212681ef8e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_18759fcd-98bb-49e7-9566-c77e451b719b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7bed21e6-cb3c-4351-88b0-162702f29c7a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f15a5001-f8d0-4ce4-a16e-3ca614d8f15a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fcdf3ad8-8d1c-4b71-a61a-b57600c066b3.txt`

Agent report (verbatim tail of failing run):

```
I clicked the avatar one final time and it still only shows the hover tooltip — no popover opens.

**Summary of what I did and found:**

1. **Located the avatar**: The "Skyler (you)" avatar (pink circle with "S") sits in the top toolbar at the right side, next to the Share button. Notably, it is partially clipped at the right-panel boundary (~x=1135), and the adjacent "Present" button is entirely hidden — the toolbar appears to overflow/clip at this 1280px viewport width.

2. **Attempted to open the collaborators popover** many ways:
   - Clicked the button via its accessibility reference (`button "Skyler (you)"`)
   - Clicked directly on several coordinates within the visible avatar
   - Double-clicked, held mouse down/up separately, and pressed Enter/Space after clicking
   
3. **Result**: In every case, only the hover tooltip "Skyler (you)" appeared. Screenshots and full accessibility-tree reads (including off-viewport/hidden elements) immediately after each click confirmed that **no popover, menu, or dialog is ever mounted** in the DOM.

4. **Sanity check**: The neighboring "Share" button works perfectly (its dialog opened and listed "Skyler (you) — can edit"), proving the app's click handling and overlay system work in general — the avatar button specifically is non-functional.

The collaborators popover could not be opened: clicking the avatar does nothing beyond showing a tooltip, so the requested interaction is broken (possibly related to the toolbar being clipped/overlapped by the right panel at this viewport width).

verdict: not-approve
```
