# DesignPen [sharing & collab]: 'ask to spotlight' fails QA — 3/3 runs report broken workflow (00405-ask-to-spotlight-ui)

Description:
The "Ask to spotlight" collaboration flow is unreachable due to three stacked defects. First, the Share dialog's "Copy link" button writes nothing to the clipboard (verified with a controlled clipboard round-trip test; likely a silent `navigator.clipboard?.writeText` no-op on the insecure http origin), and no other UI reveals the file link. Second, opening the file URL in a second tab creates a distinct user identity but no peer presence ever appears in either tab — each toolbar only shows the local user's single avatar. Third, clicking your own toolbar avatar only produces a hover tooltip; no collaborators popover is ever added to the DOM, so the peer row's "…" menu and its "Ask to spotlight" option are never reachable. The agent also noted the "Present" button and a neighboring toolbar button are invisible/zero-size at the 1280x720 viewport, suggesting broken toolbar rendering.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Click the toolbar Share button and click "Copy link"; verify the clipboard contents (e.g. by pasting into a text field).
3. Open the file URL (http://localhost:3000/) in a second browser tab so a peer should be present; wait, generate cursor activity, edit the document, and reload.
4. In the first tab, check the toolbar avatar stack for a second (peer) avatar.
5. Click your own avatar in the first tab's toolbar to open the collaborators popover.
6. Attempt to open the peer row's "…" menu and choose "Ask to spotlight".

Actual Result:
- "The app's 'Copy link' writes nothing to the clipboard" — after clicking Copy link (and the Code panel's "Copy URL for file"), pasting still produced the old clipboard contents, even though a controlled Ctrl+C/Ctrl+V test round-tripped "F5F5F5" perfectly. No other UI reveals the link; "Get embed code", "Publish to Community", "Copy Dev Mode link", the access rows, the invite input (which cannot receive focus), and the "Actions…" search are all inert.
- The second tab gets a distinct identity ("Finley" vs "Noa") and after a reload even loads the same persisted document, but "no peer presence ever appeared in either tab" — each toolbar only ever shows the local user's single avatar.
- Clicking your own avatar (by coordinates and element reference, multiple times, in both tabs) only produces a hover tooltip ("Noa (you)"); "No collaborators popover ever opens" — full accessibility-tree reads confirm no popover/menu is added to the DOM. The peer row, its "…" menu, and "Ask to spotlight" are therefore unreachable.
- Additionally, the "Present" button and a neighboring toolbar button are invisible/zero-size at this viewport.

Expected Result:
Copy link should place the file's share URL on the clipboard; opening that link in a second tab should register a peer whose avatar appears in both tabs; and clicking your own avatar should open the collaborators popover where the peer row's "…" menu offers "Ask to spotlight".

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 3 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_26ac3905-7d9c-4b34-a8fd-600e1d574d29.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_31db3b64-3aeb-4c24-81ee-68c107415792.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_49e940a2-bd82-4568-9560-d42ebaa0869b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_555062b5-b8e0-442f-9365-4d232200aed9.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6ebc8fbd-067e-4358-b86f-d7d5e809cb90.txt`

Agent report (verbatim tail of failing run):

```
I have now exhaustively tested every avenue. Let me summarize what happened.

**What I attempted and found:**

1. **Copying the share link:** I opened the Share dialog and clicked "Copy link" several times. To verify the clipboard, I ran a controlled test: selecting text in the page-color field and pressing Ctrl+C/Ctrl+V round-tripped "F5F5F5" perfectly — so the clipboard itself works in this browser. However, after clicking "Copy link" (and also the Code panel's "Copy URL for file"), pasting still produced the *old* clipboard contents. **The app's "Copy link" writes nothing to the clipboard** (likely a silent `navigator.clipboard?.writeText` no-op on this insecure http origin). No other UI reveals the link: "Get embed code", "Publish to Community", "Copy Dev Mode link", the access rows, the invite input (which can't even receive focus), and the "Actions…" search are all inert.

2. **Opening a second tab so a peer is present:** Since no link could be copied, I opened the file's URL (`http://cua_designpen.web/`) in a second tab. The second tab did get a distinct identity ("Finley" vs. "Noa" in tab 1), and after a reload it even loaded the same persisted document (it showed the test rectangle I drew in tab 1). But **no peer presence ever appeared in either tab** — each toolbar only ever showed the local user's single avatar, even after waiting, generating cursor activity, editing the document, and reloading.

3. **Avatar → collaborators popover → peer "…" menu → "Ask to spotlight":** Clicking my own avatar in tab 1's toolbar (by coordinates and by element reference, multiple times, in both tabs) only produces a hover tooltip ("Noa (you)"). **No collaborators popover ever opens** — I confirmed via full accessibility-tree reads (including off-viewport elements) that no popover/menu is added to the DOM. Therefore the peer row, its "…" menu, and the "Ask to spotlight" option were never reachable. (Additionally, the "Present" button and a neighboring toolbar button are invisible/zero-size at this viewport, suggesting broken toolbar rendering.)

I cleaned up after my diagnostics (removed the test rectangle, restored the page color), and the second tab remains open at the file URL.

**Conclusion:** The task could not be completed due to app defects: the "Copy link" button silently fails to copy anything, opening the file in a second tab never registers a peer in the collaborators UI, and clicking your own avatar never opens the collaborators popover — so the "…" menu and "Ask to spotlight" action are unreachable.

verdict: not-approve
```
