# Blocked tasks

These 8 tasks cannot pass in the Taiga harness and are **not fixable by any
gym-side code change**. They are parked here, out of the `tasks/` verification
set.

## Why they are blocked (root cause)

On the Taiga surface the agent drives the browser with **Taiga's own browser
tool**, not the gym's `browser_*` tools (the gym registers `required_tools:
[browser]` and Taiga injects its client). The missing capabilities live in
Taiga's browser tool, so adding tools or CDP plumbing in this repo has no
effect — Taiga never calls them.

Every one of these tasks has reward `answer STRING_CONTAINS "verdict: approve"`
— a self-report that the action succeeded. The only way to make them "pass"
without the real capability is to rewrite the prompt so the agent tests
something else, which produces a dishonest pass. So they stay blocked until the
harness gains the capability.

The **app features themselves work** (verified via alternate paths during QA).
The block is purely the harness's browser-interaction surface.

## Group 1 — Modifier / non-left-button mouse gestures

Taiga's browser tool has no way to hold a keyboard modifier during a mouse
drag/scroll, and no right-button press-and-hold/drag (only an atomic
right-click). `hold_key` rejects modifier keys; `drag`/`scroll` ignore
modifiers.

- **00051-vector-shape-builder-remove-ui** — Alt+drag a sweep over a filled
  region (Shape builder) to strip the fill. Needs Alt held through the drag.
- **00069-canvas-alt-duplicate-drag-ui** — Alt/Option+drag a square so a copy
  peels off. Needs Alt held through the drag.
- **00085-canvas-pan-right-drag-ui** — right mouse button press-and-hold + drag
  to pan. Needs a right-button drag primitive.
- **00086-canvas-pinch-zoom-ui** — Ctrl+scroll (trackpad-pinch emulation) to
  zoom. Needs a modifier held during scroll.
- **00093-canvas-wheel-pan-zoom-ui** — wheel to pan, then Ctrl+scroll to zoom.
  Needs a modifier held during scroll.

**Unblock requires:** Taiga browser tool gains a `modifiers` option on
drag/scroll (Alt/Ctrl/Cmd/Shift) and a right-button drag / press-and-hold.

## Group 2 — Native OS file dialog / file upload

Selecting a file goes through a native OS file-chooser (or a file `<input>`);
Taiga's browser tool cannot drive the OS dialog, and no seed files are staged
in the container.

- **00265-image-choose-ui** — set a shape's fill from an image via the Image
  tab picker (file upload). Needs a file-upload capability + a provisioned
  image seed. (Possibly rewritable to a built-in/stock image source if the app
  exposes one — not investigated.)
- **00386-file-import-pen-ui** — File > Open… a `.pen` file via the OS picker.
  OS dialog undriveable; no `.pen` provisioned.
- **00388-file-open-ui** — File > Open… (Cmd+O) a `.fig` file via the OS
  picker. OS dialog undriveable; no `.fig` provisioned.

**Unblock requires:** Taiga browser tool supports file-chooser interception
(e.g. CDP `Page.setInterceptFileChooserDialog` + `DOM.setFileInputFiles`) and
the seed file(s) staged in the container's upload dir.
