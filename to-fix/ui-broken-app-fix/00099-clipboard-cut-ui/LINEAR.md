# DesignPen [clipboard]: 'cut to clipboard' fails QA — 1/5 runs report broken workflow (00099-clipboard-cut-ui)

Description:
Cutting a shape (right-click > Cut or Main menu > Edit > Cut) removes the object from the canvas but does not place a usable copy on the clipboard — the cut object can never be pasted back. Ctrl+V and right-click > "Paste here" both produce nothing after a Cut. The clipboard itself works: Copy > Paste on the same document duplicates reliably. Worse, Cut corrupts the clipboard state: after copying a rectangle (known-good clipboard content) and then cutting a star, pasting yields nothing at all — neither the star nor the previously copied rectangle — showing Cut overwrote the clipboard with unusable data. The behavior is identical for both cut entry points. Effectively Cut is a Delete, and the object is only recoverable via Undo.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a rectangle with the Rectangle tool (R).
3. Draw a star via the shape tool dropdown > Star.
4. Select the star and cut it via right-click > Cut (or Main menu > Edit > Cut).
5. Press Ctrl+V (or right-click > Paste here) to paste the star back.
6. Optionally: copy the rectangle first (Ctrl+C), then cut the star, then paste — to observe the clipboard being clobbered.

Actual Result:

- The star is removed from the canvas, but pasting produces nothing — the star cannot be restored via paste with either Ctrl+V or right-click > "Paste here".
- After Cut, even previously copied clipboard content (the rectangle) no longer pastes; Cut cleared/overwrote the clipboard with unusable data.
- Copy > Paste works reliably, isolating the defect to the Cut operation.

Expected Result:
Cut should remove the object from the canvas AND place it on the clipboard so a subsequent Paste re-inserts it, matching standard editor behavior and the working Copy > Paste path.

Estimate: M (3 points) — Cut's clipboard-write path is broken while Copy's works; likely a serialization/ordering bug in the cut handler

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 1 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9050faf4-aeb4-4877-8b55-bba3d3dfa8e5.txt`

Agent report (verbatim tail of failing run):

```
I completed the requested actions:
1. **Created a rectangle** on the canvas (via the Rectangle tool).
2. **Created a star** on the canvas (via the shape dropdown → Star).
3. **Selected the star** (it was auto-selected after drawing).
4. **Cut it** via right-click → **Cut** — the star was removed from the canvas. I also confirmed the alternate path, Main menu → Edit → Cut, behaves the same way.

However, while verifying the result, I found a **bug in the Cut operation**:

- After cutting the star, it could **not be pasted back** — neither via `Ctrl+V` nor via right-click → "Paste here". Nothing appears on the canvas.
- To rule out an environment/clipboard limitation, I tested **Copy → Paste** on the rectangle: it works reliably every time (a duplicate appears, even after deselecting first). So the clipboard itself functions.
- I then set the clipboard to a known object (copied the rectangle), created a star, and cut it. Afterward, pasting produced **nothing at all** — not the star, and not even the previously-copied rectangle. This shows the Cut cleared/overwrote the clipboard with unusable data rather than placing the cut object there.
- This occurs with **both** cut methods the task mentions (right-click → Cut *and* Main menu → Edit → Cut).

In short: Cut behaves like a Delete — it removes the object from the canvas but fails to place a usable copy on the clipboard, so the cut object cannot be pasted. The object is only recoverable via Undo, not via paste. Since the task's goal is specifically to "cut it **to the clipboard**," this is a real, reproducible defect.

verdict: not-approve
```
