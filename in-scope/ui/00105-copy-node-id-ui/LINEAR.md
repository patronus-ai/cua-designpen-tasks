# DesignPen [clipboard / copy-paste]: 'copy node id' fails QA — 5/5 runs report broken workflow (00105-copy-node-id-ui)

Description:
The context-menu action Copy/Paste as > Copy node ID silently does nothing: the menu item exists and the click executes with no error, but the clipboard is left untouched — a controlled round-trip test showed a stale marker string ("cliptest") still pasted after invoking the action. Root cause per the app's own toast: "Clipboard access is blocked in this browser context" (app served over plain HTTP, so the async Clipboard API is unavailable). Copy-side operations ("Copy node ID", "Copy as SVG", Ctrl+C) fail silently with no fallback and no error message to the user, which is itself a UX bug — only "Paste here" surfaces the error.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the shape tool dropdown in the bottom toolbar, choose "Polygon", and drag on the canvas to draw a polygon ("Polygon 1").
3. Ensure the polygon is selected (highlighted in Layers panel, POLYGON properties in Design panel).
4. Optionally seed the clipboard with a known string via a text input and Ctrl+C to enable verification.
5. Right-click the polygon, hover "Copy/Paste as", and click "Copy node ID".
6. Paste into a text input (Ctrl+V) to check what is on the clipboard.

Actual Result:

- Clicking "Copy node ID" gives no feedback at all — no success toast, no error — and the clipboard is left untouched: pasting still produces the previously seeded marker string ("cliptest") instead of a node ID. Reproduced 3 times.
- The system clipboard itself works in the environment (a copy/paste round-trip of a known string inside a text input succeeded), so the copy silently did nothing.
- Root cause confirmed by the app: using "Paste here" displays a red error toast "Clipboard access is blocked in this browser context" (plain HTTP origin, async Clipboard API unavailable), but the copy-side operations fail silently with no fallback and no error message.

Expected Result:
Copy/Paste as > Copy node ID should place the editor's internal layer identifier on the clipboard; if clipboard access is unavailable, the app should surface an error (or use a working fallback) rather than silently no-op.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2244b66d-9ef9-46e5-8571-d9c2890e586b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3b9c9a1b-cfa9-4bb0-a43f-f8a5eac18a15.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6caa7e02-6a1f-4a23-ac82-d97084e7eaf8.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b90d71c1-42f1-461e-99a4-ce721ddcdfc6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bf814a8b-33af-4f04-b0a2-3ac1fd40dbc1.txt`

Agent report (verbatim tail of failing run):

```
The editor is back in a clean state with "Polygon 1" selected on the canvas.

## Summary

**What I did:**
1. ✅ **Drew a polygon** — opened the shape tool dropdown in the bottom toolbar, chose "Polygon", and dragged on the canvas to create "Polygon 1" (200×180 triangle).
2. ✅ **Selected it** — it was selected, shown highlighted in the Layers panel with the POLYGON properties in the Design panel.
3. ✅ **Right-clicked it** — the context menu appeared with a "Copy/Paste as" submenu.
4. ✅ **Chose Copy/Paste as > Copy node ID** — the menu item exists and the click executed without any visible error (tried 3 times).

**What went wrong — the node ID was never actually copied:**
- Clicking "Copy node ID" gives no feedback (no success toast, no error), but the clipboard is left untouched. I proved this with a controlled test: I first verified the system clipboard works in this environment by copying/pasting a known string ("cliptest") inside a text input (round-trip succeeded). Then, after clicking "Copy node ID", pasting still produced the stale "cliptest" string instead of a node ID — the copy silently did nothing.
- The app itself confirms the root cause: using "Paste here" displays a red error toast, **"Clipboard access is blocked in this browser context"** (the app is served over plain HTTP, so the async Clipboard API is unavailable). The copy-side operations ("Copy node ID", "Copy as SVG", Ctrl+C) fail silently with no fallback and no error message to the user.

So while the UI flow (polygon → right-click → Copy/Paste as → Copy node ID) is present and clickable, the feature's actual purpose — copying the editor's internal layer identifier to the clipboard — does not work in this context, and the failure is silent, which is itself a UX bug.

verdict: not-approve
```
