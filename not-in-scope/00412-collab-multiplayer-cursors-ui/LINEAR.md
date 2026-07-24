# DesignPen [layers panel]: 'collab multiplayer cursors' fails QA — 3/3 runs report broken workflow (00412-collab-multiplayer-cursors-ui)

Description:
Multiplayer presence/cursor sync between two tabs of the same file does not work at all. Opening the file URL in a second tab assigns a distinct collaborator identity, but no peer session ever forms: neither tab shows the other user's presence avatar (each lists only itself), moving the mouse across the second tab's canvas never produces a remote cursor in the first tab, and shapes drawn in one tab never appear in the other — only a stale snapshot is served on full reload. Compounding this, the share features needed to obtain a peer link are stubs: "Copy link" gives no toast and never displays the URL, the app URL never changes from `http://localhost:3000/` (no file-ID routing; other paths 404 or hang on a splash screen), and "Copy Dev Mode link", "Get embed code", "Publish to Community", invite/access options, "Present", "Back to files", and the ⌘K Actions palette are all non-functional. The collaboration backend appears broken or unimplemented.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Share dialog and click "Copy link" (note: no confirmation appears and the URL is never displayed; the share link resolves to the root URL since the app has no file-ID routing).
3. Open http://localhost:3000/ in a second browser tab/window — it loads the same file under a different collaborator identity.
4. In the second tab, move the mouse across the canvas in several sustained sweeps.
5. Watch the first tab's canvas for a remote collaborator cursor, and check both toolbars for peer presence avatars.
6. Optionally draw a shape in one tab and check whether it appears in the other.

Actual Result:
- No peer session forms: "neither tab ever shows the other user's presence avatar; each session only lists itself ('Ellis (you)' / 'Skyler (you)')."
- No collaborator cursor: mouse movement across the second tab's canvas never produced a remote cursor on the first tab's canvas (verified across many samples, both directions).
- No live sync: shapes drawn in one tab never appeared in the other; only a stale snapshot is served on full reload.
- Share features are stubs: "Copy link" gives no toast and the link is never displayed; "Copy Dev Mode link", "Get embed code", "Publish to Community", invite/access options, "Present", "Back to files", and the ⌘K Actions palette are all non-functional.

Expected Result:
Opening the file's share link in a second tab should join the same live session: both tabs should show each other's presence avatars, mouse movement in one tab should render as a named collaborator cursor on the other tab's canvas, and edits should sync live.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 3 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2dba4813-70c7-4e95-b850-bd8eb639953c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_393311b2-0fa9-437f-8162-a5edfa4b71e5.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_cb856bc1-ce08-4526-9bd2-bf84af1401d9.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e06ba258-a550-4004-8c98-38d06d251416.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f440b085-7452-4eac-b946-9356fdae2088.txt`

Agent report (verbatim tail of failing run):

```
Cleanup complete — both tabs are back to their pre-test state. Here is a summary of everything I did and found:

**What I did**
1. **Got the share link:** Opened the Share dialog in tab 1 ("Untitled", user "Ellis") and clicked "Copy link" (also tried the Code panel's "Copy URL for file"). The app gives no visible confirmation and never displays the URL anywhere. Since the app's URL never changes from `http://cua_designpen.web/` (no file-ID routing; all other paths 404 or hang on a splash screen), the share link resolves to that root URL.
2. **Opened it in a second tab** (its own window). It loaded the same file and was assigned a different collaborator identity ("Skyler" vs "Ellis"), and after a reload it even showed tab 1's content (retitled "snapshot") — so it points at the same document.
3. **Moved the mouse across the canvas in the second tab** in several sustained sweeps (and also in the reverse direction as a control), **while repeatedly watching the first tab's canvas** via screenshots between and after movements.

**Problems found**
- **No peer session actually forms:** neither tab ever shows the other user's presence avatar; each session only lists itself ("Ellis (you)" / "Skyler (you)").
- **No collaborator cursor:** moving the mouse across the second tab's canvas never produced a remote cursor on the first tab's canvas (verified across many samples, both directions).
- **No live sync at all:** shapes drawn in one tab never appeared in the other (only a stale snapshot is served on full reload).
- **Share features are stubs:** "Copy link" gives no toast and the link is never displayed; "Copy Dev Mode link", "Get embed code", "Publish to Community", invite/access options, "Present", "Back to files", and the ⌘K Actions palette are all non-functional — so there is no way to obtain or verify a working peer-session link in-app.

(I undid the test rectangles in both tabs afterward, restoring the original state.)

The core goal — an active peer session whose mouse movement in the second tab is visible as a collaborator cursor on the first tab's canvas — could not be achieved because the app's collaboration/share functionality is broken or unimplemented: the share link opens an isolated session, and no presence, cursor, or document sync ever occurs between the two tabs.

verdict: not-approve
```
