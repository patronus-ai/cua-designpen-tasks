# Enrichment: pid 00099 — Cut deletes the object but leaves nothing pasteable on the clipboard

## Root cause analysis

Confirmed in source. Both Cut entry points funnel into `document.execCommand('cut')`:

- Right-click > Cut: `cua_designpen/src/components/CanvasMenu.vue:121` —
  `@select="execCommand('cut')"` → `src/app/editor/canvas/menu/actions.ts:30-38`
  (`window.document.execCommand(cmd)`).
- Edit > Cut (web menu): `cua_designpen/src/app/shell/menu/app-menu.ts:88` —
  `cut: () => document.execCommand('cut')`.

`execCommand('cut')` fires a synthetic `cut` ClipboardEvent, handled at
`cua_designpen/src/app/shell/keyboard/clipboard.ts:52-59`:

```ts
useEventListener(window, 'cut', (e: ClipboardEvent) => {
  if (isEditing(e)) return
  if (isEditorReadOnly(store.state)) return
  e.preventDefault()
  if (e.clipboardData) void store.writeCopyData(e.clipboardData)
  store.deleteSelected()
})
```

`store.deleteSelected()` runs synchronously — that is why the object reliably
disappears. The clipboard write, however, is the async mobile-clipboard override
(`cua_designpen/src/app/editor/mobile-clipboard/index.ts:10-15`):

```ts
async function writeCopyData(clipboardData: DataTransfer) {
  await editor.writeCopyData(clipboardData)
  state.clipboardHtml = clipboardData.getData('text/html')
  if (state.clipboardHtml) state.clipboardText = ''
}
```

`editor.writeCopyData` (`packages/core/src/editor/clipboard/copy.ts:6-15`) sets
`text/html` + `text/plain` synchronously, then `await buildFigmaClipboardHTML(...)`
before a second `setData`. Per the Clipboard Events spec, the `cut` event's
`clipboardData` data store is writable only during synchronous dispatch and is put into
*protected* mode as soon as dispatch returns. Everything after the `await` therefore
operates on a neutered DataTransfer:

- the final `setData` is a silent no-op,
- `getData('text/html')` in `mobile-clipboard/index.ts:12` returns `''`,
- so `state.clipboardHtml = ''` — the internal buffer (the **only** paste source in the
  gym: insecure origin + CDP automation, see `systemClipboardReadable()` in
  `src/app/editor/clipboard/plain-paste.ts:8-16`) is emptied. This simultaneously
  explains both symptoms: paste-after-cut finds nothing, and a previously Ctrl+C-copied
  payload is **overwritten with unusable (empty) data**.

Note the selected nodes themselves are captured correctly before deletion — the bridge
(`packages/core/src/editor/bridges/clipboard.ts:11-12`) snapshots
`selection.getSelectedNodes()` synchronously — so this is purely the
DataTransfer-lifetime bug, not a delete-before-copy race.

**Why keyboard Ctrl+X works:** the gym build sets `VITE_OPENPENCIL_AUTOMATION=1`
(`Dockerfile:40-44`), so `src/app/shell/keyboard/clipboard.ts:31-35` binds Ctrl+X
directly to `store.mobileCut()` → `mobileCut` (`mobile-clipboard/index.ts:28-31`) does
`await mobileCopy()` on a **script-constructed** `new DataTransfer()` (never neutered,
`getData` works) and only then `editor.deleteSelected()`. Same wrapper, different
DataTransfer provenance — that is the entire divergence between the working and broken
paths.

## Proposed fix

Route the menu Cut entries through the already-correct internal path: in
`createCanvasMenuActions.execCommand` (`src/app/editor/canvas/menu/actions.ts:30-38`)
and in `app-menu.ts:88`, call `store.mobileCut()` (guarded by
`isEditorReadOnly(store.state)`, matching the keydown branch) instead of relying on the
`document.execCommand('cut')` event round-trip. `mobileCut` copies into a fresh
DataTransfer and deletes afterwards, exactly like the working Ctrl+X shortcut and the
mobile toolbar (`src/components/Toolbar/actions.ts:29`).

Additionally (fixes the native cut event for real users too): in the window `cut`
handler and/or `writeCopyData`, populate `state.clipboardHtml` synchronously (build the
OpenPencil HTML before any `await`; never read the event's DataTransfer back after an
`await`), and only delete the selection after the buffer is known-good.

Risk: low — `mobileCut` is already the shortcut/toolbar code path. Preserve the
synchronous `setData` calls on the event DataTransfer so secure-origin cross-app cut
still exports content to the OS clipboard. Ensure undo still records the delete as one
step ("Cut" should remain a single undoable action).

## Acceptance criteria

- Right-click a node > Cut: node disappears AND a subsequent Ctrl+V / "Paste here" /
  "Paste to replace" recreates it (identical subtree), on an insecure origin under CDP
  automation.
- Edit > Cut behaves identically to right-click > Cut.
- Cut then paste twice: both pastes succeed (buffer is not consumed by the first paste).
- Ctrl+C node A, then menu-Cut node B, then paste → **B** is pasted; the buffer is never
  left empty after cutting a non-empty selection.
- Cut in a read-only/view-only session does nothing (no delete, no buffer change).
- Undo after Cut restores the node in one step; keyboard Ctrl+X is unchanged.

## Regression tests to add

- **Unit (`src/app/editor/mobile-clipboard/index.test.ts`):** `mobileCut` populates
  `state.clipboardHtml` with the selection's HTML *before* `deleteSelected` is invoked
  (assert call order with spies) and never leaves the buffer empty for a non-empty
  selection.
- **Unit:** `writeCopyData` given a DataTransfer that becomes read-protected after one
  microtask (getData → `''`, setData → no-op post-await) still yields a non-empty
  `state.clipboardHtml` and does not clobber a pre-existing buffer value.
- **Unit (`src/app/editor/canvas/menu/actions.test.ts` / app-menu tests):** the menu
  Cut action calls `store.mobileCut` (spy) and is gated on `isEditorReadOnly`.
- **Integration (jsdom):** bind `bindEditorClipboard`, dispatch a synthetic `cut`
  ClipboardEvent with a dispatch-scoped DataTransfer; assert the selected node is
  deleted, `state.clipboardHtml` is non-empty, and `mobilePaste()` recreates the node.
- **E2E (gym/CDP):** create rect → right-click > Cut → assert canvas node count -1 →
  right-click > "Paste here" → assert count back to original and pasted node matches the
  cut node's type/size; repeat via Edit > Cut. Second scenario: Ctrl+C node A, menu-Cut
  node B, paste, assert B (not nothing, not A... assert exactly B) is created.
