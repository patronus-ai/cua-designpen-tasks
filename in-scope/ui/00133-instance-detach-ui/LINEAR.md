# DesignPen [component instances]: 'instance detach' fails QA — 3/5 runs report broken workflow (00133-instance-detach-ui)

Description:
Detaching a component instance (Ctrl+Alt+B or Main menu > Object > Detach instance) works in-session but does not persist and can corrupt the document on save/reload. After a page reload the detach was silently reverted (the shape was an INSTANCE again — happened twice); on a third attempt the detach persisted but the detached frame lost its child rectangle (an empty frame was saved — data loss); a further reload corrupted the document even more, with the main component vanishing entirely and only a dangling instance at (0,0) remaining. There is also a minor UI bug: immediately after detaching, the Layers panel keeps showing the old instance styling (purple hollow-diamond icon) until a reload even though the object is actually a FRAME.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a rectangle with the rectangle tool.
3. Make it a component with Ctrl+Alt+K (the literal Cmd modifier does not register in this environment; Ctrl is the equivalent) — the panel shows "COMPONENT".
4. Right-click the component and choose "Create instance" — an instance appears and the panel shows "INSTANCE".
5. Select the instance and detach it with Ctrl+Alt+B (or Main menu > Object > Detach instance) — the panel changes to "FRAME".
6. Reload the page and inspect the Layers panel / Design panel for the detached shape.
7. Repeat the detach + reload cycle to observe the data-loss and corruption modes.

Actual Result:

- In-session the detach works: the panel changes to "FRAME", instance options disappear, and the context menu offers "Create component".
- After reloading the page, the detach was silently reverted — the shape was an INSTANCE again (happened twice).
- On a third attempt the detach persisted but the detached frame lost its child rectangle: an empty frame was saved (data loss).
- After yet another reload the document was corrupted further: the main component vanished entirely, leaving only a single dangling instance at (0,0); the corrupted objects had to be deleted and the flow rebuilt from scratch.
- Minor UI bug: immediately after detaching, the Layers panel kept showing the old instance styling (purple hollow-diamond icon) until a reload, even though the object was actually a frame.

Expected Result:
Detaching an instance should convert it to a plain frame that keeps its child content, persist across page reloads, never corrupt the main component, and update the Layers panel icon immediately.

Estimate: XS (1 point) — likely environment/tooling limitation, verify manually and re-scope

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0956e4dc-fe15-46e9-994d-5c2b2b86f3a6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1d8eabe0-7f2f-4153-8a1e-0ba2f1616c67.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3058255e-cb61-4f6c-8b34-3e0eb52eae0b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_668bd17e-5ec6-4879-960f-091575ed9c5e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fba9be32-ae36-4c4c-bc47-38a92f29b100.txt`

Agent report (verbatim tail of failing run):

```
The final in-session state is now correct:

- **Layers panel:** "Component" (detached frame, expanded to show child "Rectangle 1") + "Component" (main component with filled purple diamond)
- **Design panel:** the detached shape is type "FRAME" with no "Go to Main Component" / "Detach Instance" options
- **Canvas:** both the main component and the detached copy render with their rectangle content

**Summary of what was done:**
1. ✅ Drew a rectangle with the rectangle tool
2. ✅ Made it a component — Ctrl+Alt+K worked (the literal Cmd modifier didn't register in this environment, but Ctrl is the equivalent and the UI confirmed "COMPONENT")
3. ✅ Right-clicked the component → "Create instance" — instance appeared and the panel showed "INSTANCE"
4. ✅ Selected the instance and detached with Ctrl+Alt+B — panel changed to "FRAME", instance options disappeared, and the context menu then offered "Create component" (confirming it's detached)

**Problems encountered:**
- All operations worked correctly in-session, but the app's persistence is broken. After reloading the page, the detach operation was silently reverted (the shape was an INSTANCE again) — this happened twice. On a third attempt the detach persisted but the detached frame **lost its child rectangle** (data loss — an empty frame was saved). After yet another reload, the document was corrupted even further: the main component vanished entirely, leaving only a single dangling instance at (0,0). I had to delete the corrupted objects and rebuild the entire flow from scratch. The final live state is correct, but the detach-instance operation does not persist reliably and can corrupt the document on save/reload.
- Minor UI bug: immediately after detaching, the layers panel kept showing the old instance styling (purple hollow-diamond icon) until a reload, even though the object was actually a frame.

Because of the non-persisting detach operation and the data corruption it caused across reloads, this cannot be approved.

verdict: not-approve
```
