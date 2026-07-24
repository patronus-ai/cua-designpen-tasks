# DesignPen [frames]: 'frame extreme-height stress test' fails QA — 1/5 runs report broken workflow (20008-frame-delete-children-ui)

Description:
During the adversarial frame workflow (frame with two child rectangles; Delete/undo, extreme H values, mid-drag Escape), setting the frame's H field in the Design panel to an extreme value (1e99) and then triggering "Zoom to fit" hangs the app indefinitely. The page's main thread blocks: every subsequent screenshot, click and navigation via CDP times out, and after repeated failures the browser container itself is reported unresponsive ("Browser container unresponsive after 5 consecutive CDP failures"). The app never recovers on its own — the run had to end without a final report because the frozen tab could not even be reloaded. The Design panel accepts the 1e99 input without validation, and the viewport/zoom-to-fit code then apparently enters an unbounded computation on the degenerate bounds.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press F and drag out a frame about 400x300; press R and draw two rectangles inside it so the frame has two children.
3. Select the frame and, in the Design panel, set the H field to 1e99.
4. Trigger "Zoom to fit" (e.g. via the zoom menu or Shift+1).

Actual Result:

- The app freezes: the main thread blocks indefinitely (verified frozen for 18+ seconds and never recovering).
- All CDP commands (Page.captureScreenshot, clicks, navigation) time out; the harness eventually reports "Browser container unresponsive after 5 consecutive CDP failures".
- Reloading the page also times out, so the session is unrecoverable without killing the tab/container.

Expected Result:
The H field should reject or clamp non-renderable extreme values (0, negative, 1e99), and zoom-to-fit should be robust against degenerate/huge bounds — never blocking the main thread. At worst the app should show a validation error and keep the document responsive.

Estimate: L (5 points) — crash-class hang requiring input validation on dimension fields plus a guard in the viewport/zoom-to-fit math against non-finite or astronomically large bounds

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 1 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_98568551-5cb6-4ab7-9f9f-b2cf9a57d120.txt`

Agent report (verbatim tail of failing run; the run was killed by the freeze before a final verdict could be emitted):

```
Still frozen after 3 seconds. Let me wait longer to see if it recovers.

[screenshot] <error>Failed to capture screenshot: CDP command (Page.captureScreenshot) timed out waiting for the browser's acknowledgement — the action may have taken effect; take a screenshot to verify before retrying.</error>

The app remains frozen after 8+ seconds. This is a critical freeze. Let me check the tab list to see the tab's state.

[list_tabs] Available tabs:
  window 1739144289:
    • tabId ADB407F289CCF01725E17C5BFABC4D97: "OpenPencil" (http://cua_designpen.web/localdoc/untitled) (current)

[screenshot] <error>Failed to capture screenshot: CDP command (Page.captureScreenshot) timed out ...</error>

The app has been frozen for ~18 seconds — this is a definitive critical freeze. "Zoom to fit" while a frame has H=1e99 hangs the app indefinitely (main thread blocked, all screenshots/clicks time out).

Let me attempt to recover by reloading the page. This will also test state persistence.

Navigation also timed out (main thread blocked). Let me take a screenshot to check if the reload eventually took effect.

[screenshot] <error>Failed to capture screenshot: CDP command (Page.captureScreenshot) timed out ...</error>

[wait 5] <error>Browser container unresponsive after 5 consecutive CDP failures</error>

[list_tabs] <error>Browser container unresponsive after 5 consecutive CDP failures</error>

The browser container is unresponsive due to the freeze.
```
