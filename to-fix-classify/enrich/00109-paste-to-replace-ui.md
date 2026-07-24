# Enrichment: pid 00109 — "Paste to replace" reports no design content after context-menu Copy; "Paste here" ignores the clicked location

## Root cause analysis

Two distinct defects, both confirmed in source.

### Primary: context-menu Copy leaves the internal buffer empty, so "Paste to replace" fails

The toast text comes from `cua_designpen/src/app/editor/clipboard/paste-to-replace.ts:16-35`:

```ts
export async function pasteClipboardToReplace(store: EditorStore) {
  ...
  const buffered = store.state.clipboardHtml
  if (buffered) {
    await store.pasteFromHTML(buffered, undefined, { replaceSelection: true })
    return
  }
  try {
    const html = await readClipboardHtml()
    if (!html) {
      toast.error('Clipboard has no design content to paste')
      ...
```

On the gym host (insecure origin, CDP automation) `navigator.clipboard.read` is
unavailable (`readClipboardHtml` returns null, see also `systemClipboardReadable()` in
`src/app/editor/clipboard/plain-paste.ts:8-16`), so `state.clipboardHtml` is the only
viable source. Context-menu Copy fails to populate it — and actively clobbers a prior
Ctrl+C payload — because of the copy-event DataTransfer-lifetime bug:

- `src/components/CanvasMenu.vue:111` → `execCommand('copy')` →
  `src/app/editor/canvas/menu/actions.ts:30-38` `window.document.execCommand('copy')`
  fires a synthetic `copy` ClipboardEvent;
- handled at `src/app/shell/keyboard/clipboard.ts:44-50` →
  `void store.writeCopyData(e.clipboardData)`;
- the wrapper (`src/app/editor/mobile-clipboard/index.ts:10-15`) does
  `await editor.writeCopyData(clipboardData)` (which itself awaits
  `buildFigmaClipboardHTML`, `packages/core/src/editor/clipboard/copy.ts:13`) and only
  then `state.clipboardHtml = clipboardData.getData('text/html')`. By that time the
  event's DataTransfer has been placed in *protected* mode (spec behavior once dispatch
  completes), so `getData` returns `''` → `state.clipboardHtml = ''`.

Keyboard Ctrl+C works because the `VITE_OPENPENCIL_AUTOMATION=1` build
(`Dockerfile:40-44`) binds it to `store.mobileCopy()`
(`src/app/shell/keyboard/clipboard.ts:26-30`), which uses a script-constructed
`new DataTransfer()` that is never neutered. Full write-path analysis with quoted code is
in the sibling appendix `00100-clipboard-paste-ui.md`; the fix there (route menu Copy
through `mobileCopy` / assign the buffer before any `await`) also resolves this pid's
"no design content" symptom.

### Secondary: "Paste here" pastes at the viewport center / a fixed offset, never at the click point

"Paste here" (`CanvasMenu.vue:126-133`) calls `canvasMenuActions.pasteHere` →
`plainPaste(store)` (`src/app/editor/canvas/menu/actions.ts:118`). On the gym,
`choosePasteSource` picks `'buffer'` and `plainPaste`
(`src/app/editor/clipboard/plain-paste.ts:47-49`) calls `store.mobilePaste()` — **with
no position argument**. `mobilePaste`
(`src/app/editor/mobile-clipboard/index.ts:46-63`) then pastes at the viewport center:

```ts
function mobilePaste() {
  ...
  void editor.pasteFromHTML(state.clipboardHtml, viewportCenter())
}
```

Downstream (`packages/core/src/editor/clipboard.ts`): the Figma-format branch centers
the created nodes at `cursorPos ?? viewport center` (lines 176-179,
`placementActions.centerNodesAt(created, cx, cy)`); the OpenPencil branch creates nodes
at `source.x + 20, source.y + 20` (lines 205-212) and re-centers only if `cursorPos` is
given (line 269). Either way the clicked canvas location never reaches the paste — the
menu path drops it. Depending on which HTML flavor is in the buffer, the observed
placement is the viewport center (fixed on screen) or a constant +20/+20 offset from the
source — matching the QA report of a "fixed offset instead of the clicked location".

The working reference is the native paste handler,
`src/app/shell/keyboard/clipboard.ts:66-70`:

```ts
const { cursorCanvasX: ccx, cursorCanvasY: ccy } = store.state
const cursorPos = ccx != null && ccy != null ? { x: ccx, y: ccy } : undefined
```

`state.cursorCanvasX/Y` is updated on every canvas mouse move
(`packages/vue/src/canvas/useCanvasInput.ts:510-513` → `onCursorMove` →
`src/app/editor/canvas/collaboration-awareness.ts:7-11`), so at the moment the context
menu opens it holds exactly the right-click point (the pointer moved there immediately
before the `contextmenu` event; menu interaction happens over DOM and does not update
it). The comment in `mobile-clipboard/index.ts:33-35` ("the automation Ctrl+V path has
no tracked cursor") is stale — the cursor *is* tracked; `mobilePaste` simply never reads
it.

## Proposed fix

Primary: same fix as pid 00100 — populate the internal buffer via `store.mobileCopy()`
(or assign `state.clipboardHtml` before any `await` in `writeCopyData`) so context-menu
Copy fills `state.clipboardHtml`; `pasteClipboardToReplace` then takes its `buffered`
branch and the toast disappears.

Secondary: thread the click position into the buffer paste.

- Add an optional `pos?: {x, y}` parameter to `mobilePaste`
  (`src/app/editor/mobile-clipboard/index.ts:46`) and use `pos ?? viewportCenter()` when
  calling `editor.pasteFromHTML` (and for the SVG/text branches).
- In `plainPaste` (`src/app/editor/clipboard/plain-paste.ts:37`), accept and forward a
  position; in `createCanvasMenuActions.pasteHere`
  (`src/app/editor/canvas/menu/actions.ts:118`), pass the right-click canvas point —
  simplest source is `store.state.cursorCanvasX/Y` read when the menu action fires
  (mirroring `shell/keyboard/clipboard.ts:66-70`); more robust is capturing the
  `contextmenu` event's canvas coordinates when the menu opens and passing them
  explicitly.

Risk: low. Keep `viewportCenter()` as the fallback when no cursor is known so the
automation Ctrl+V and toolbar paste keep their current placement. "Paste to replace"
positioning is unaffected (it centers onto the replaced targets). Verify multi-node
pastes stay centered as a group at the point (which `centerNodesAt` already does).

## Acceptance criteria

- Ctrl+C a node, right-click at an empty canvas location, "Paste here": the pasted
  content is centered at the clicked canvas point (within rounding), at any pan/zoom.
- The same holds after a context-menu Copy (once the primary fix lands).
- Right-click Copy on node A, select node B, Edit/context "Paste to replace": B is
  replaced by a copy of A; no "Clipboard has no design content to paste" toast appears
  when an in-app copy was made in the same session.
- Two "Paste here" invocations at two different points place content at two different,
  correct points (not the same fixed location twice).
- Ctrl+V (no menu) placement behavior is unchanged: cursor position when known, viewport
  center otherwise.

## Regression tests to add

- **Unit (`src/app/editor/mobile-clipboard/index.test.ts`):** `mobilePaste({x, y})`
  forwards the given position to `editor.pasteFromHTML` (and the SVG/text branches);
  without an argument it falls back to `viewportCenter()`.
- **Unit (`src/app/editor/clipboard/plain-paste.test.ts`):** `plainPaste(store, pos)` on
  an unreadable system clipboard passes `pos` through to `mobilePaste`.
- **Unit (`src/app/editor/canvas/menu/actions.test.ts`):** `pasteHere` reads the tracked
  cursor canvas position (seed `state.cursorCanvasX/Y`) and forwards it; when the cursor
  is unknown it forwards `undefined`.
- **Unit (`src/app/editor/clipboard/paste-to-replace.test.ts`):** with
  `state.clipboardHtml` populated (as a fixed context-menu Copy now guarantees),
  `pasteClipboardToReplace` uses the buffer and never shows the no-content toast;
  with an empty buffer and no readable clipboard it still shows the toast.
- **E2E (gym/CDP):** pan/zoom the canvas, Ctrl+C a rect, right-click at a known screen
  point, "Paste here", convert the point to canvas coordinates and assert the pasted
  node's center equals it (±1px). Second scenario: context-menu Copy → select another
  node → "Paste to replace" → assert the target was replaced and no error toast was
  logged.
