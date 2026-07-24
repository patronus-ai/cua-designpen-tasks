# Enrichment: pid 00100 — context-menu "Copy" never populates the design clipboard

## Root cause analysis

Confirmed in source. The context-menu Copy path and the keyboard Ctrl+C path write the
internal design clipboard through two different mechanisms, and the context-menu one is
broken by an async/DataTransfer-lifetime bug.

**Broken path (right-click > Copy):**

1. `cua_designpen/src/components/CanvasMenu.vue:111` — the Copy item dispatches
   `execCommand('copy')`:

   ```html
   <ContextMenuItem data-test-id="context-copy" ... @select="execCommand('copy')">
   ```

2. `cua_designpen/src/app/editor/canvas/menu/actions.ts:30-38`:

   ```ts
   function execCommand(cmd: 'copy' | 'cut') {
     try {
       if (window.document.execCommand(cmd)) return
     } catch (error) { ... }
     toast.error(CLIPBOARD_BLOCKED_MESSAGE)
   }
   ```

   `document.execCommand('copy')` fires a **synthetic `copy` ClipboardEvent** (Chrome
   allows this during a user gesture even with no DOM selection, and returns `true`, so
   no error toast is shown — hence the *silent* failure).

3. `cua_designpen/src/app/shell/keyboard/clipboard.ts:44-50` handles that event:

   ```ts
   useEventListener(window, 'copy', (e: ClipboardEvent) => {
     if (isEditing(e)) return
     e.preventDefault()
     if (!store.state.viewerCanCopy) return
     if (e.clipboardData) void store.writeCopyData(e.clipboardData)
   })
   ```

4. `store.writeCopyData` is the mobile-clipboard override,
   `cua_designpen/src/app/editor/mobile-clipboard/index.ts:10-15`:

   ```ts
   async function writeCopyData(clipboardData: DataTransfer) {
     await editor.writeCopyData(clipboardData)
     state.clipboardHtml = clipboardData.getData('text/html')
     // Last copy wins: a node copy supersedes an earlier text-flavored copy.
     if (state.clipboardHtml) state.clipboardText = ''
   }
   ```

5. `editor.writeCopyData` is async,
   `cua_designpen/packages/core/src/editor/clipboard/copy.ts:6-15`:

   ```ts
   async function writeCopyData(clipboardData: DataTransfer, selectedNodes: SceneNode[]) {
     if (selectedNodes.length === 0) return
     clipboardData.setData('text/html', buildOpenPencilClipboardHTML(selectedNodes, ctx.graph))
     clipboardData.setData('text/plain', names)
     const html = await buildFigmaClipboardHTML(selectedNodes, ctx.graph)   // <-- suspends
     if (html) clipboardData.setData('text/html', html)
   }
   ```

**The defect:** per the Clipboard Events spec, a `copy` event's `event.clipboardData`
data store is read/write **only during synchronous event dispatch**; once the dispatch
returns, the DataTransfer is put into *protected* mode ("neutered"). The handler chain
above crosses an `await` (`buildFigmaClipboardHTML`) before it (a) re-does the final
`setData`, and (b) reads the payload back with `getData('text/html')` in
`mobile-clipboard/index.ts:12`. Both happen after dispatch has completed, so:

- the post-await `setData` is a silent no-op,
- `getData('text/html')` returns `''`,
- `state.clipboardHtml = ''` — the internal design buffer is **assigned the empty
  string**, which both leaves nothing to paste and **clobbers content previously copied
  via Ctrl+C** (the second reported symptom). `state.clipboardText` survives only because
  of the `if (state.clipboardHtml)` guard on line 14.

The synchronously-set OpenPencil HTML *does* land on the OS clipboard, but the gym runs
on an insecure origin under CDP automation, where the system clipboard is unreadable
(`systemClipboardReadable()` in `src/app/editor/clipboard/plain-paste.ts:8-16` is false),
so every paste path reads only the now-empty internal buffer.

**Working path (Ctrl+C), for contrast:** the gym image is built with
`VITE_OPENPENCIL_AUTOMATION=1` (`cua_designpen/Dockerfile:40-44`), which activates the
keydown binding in `src/app/shell/keyboard/clipboard.ts:21-30`:

```ts
if (key === 'c') { ... e.preventDefault(); void store.mobileCopy() }
```

`mobileCopy()` (`src/app/editor/mobile-clipboard/index.ts:24-26`) calls
`writeCopyData(new DataTransfer())`. A **script-constructed** DataTransfer is never
neutered, so the post-await `getData` works and `state.clipboardHtml` gets the real
payload. That is the entire divergence: same wrapper, event-provided vs
script-constructed DataTransfer.

**Adjacent defect found while tracing:** in the web app menu
(`src/app/shell/menu/app-menu.ts:66-93`) the `actions` map defines `cut` (line 88) but
**no `copy`, `paste`, or `paste-to-replace` entries** — those exist only in the
Tauri-only `src/app/shell/menu/use.ts:82-85`. So Edit > Copy in the web build has
`action: undefined` and is completely inert.

## Proposed fix

Stop round-tripping the internal buffer through the event's DataTransfer. In
`createCanvasMenuActions.execCommand` (`src/app/editor/canvas/menu/actions.ts:30-38`),
call `store.mobileCopy()` (respecting `viewerCanCopy`) instead of — or in addition to —
`document.execCommand('copy')`; `mobileCopy` already populates both an internal
DataTransfer and `state.clipboardHtml` correctly and is the exact code path the working
Ctrl+C shortcut uses.

Defense in depth (recommended, fixes the event path for *all* callers, including real
non-automation Ctrl+C): in `mobile-clipboard/index.ts` `writeCopyData`, capture the
payload before the await boundary — e.g. build the OpenPencil HTML synchronously and
assign `state.clipboardHtml` from it *before* awaiting `buildFigmaClipboardHTML`, or have
`editor.writeCopyData` return the final HTML string instead of reading it back via
`getData`. Never call `getData` on an event-provided DataTransfer after an `await`.

Also wire `copy`/`paste`/`paste-to-replace` actions in the web `app-menu.ts` map
(mirroring `cut`), using the same internal-buffer calls.

Risk: low. `mobileCopy` is already exercised by the shortcut path and the mobile toolbar
(`src/components/Toolbar/actions.ts:27-29`). Keep the synchronous `setData` on the event
DataTransfer so the OS clipboard still receives content on secure origins (cross-app
copy parity).

## Acceptance criteria

- Right-click a canvas node > Copy, then Ctrl+V (or context-menu "Paste here"): a copy of
  the node is created. Works on an insecure origin under CDP automation.
- Right-click > Copy then Edit > Paste and "Paste to replace" also succeed (no
  "Clipboard has no design content to paste" toast).
- Copy node A with Ctrl+C, then right-click node B > Copy, then paste: **B** is pasted
  (last copy wins) — and in no scenario does a context-menu Copy leave the buffer empty
  or containing stale/empty data that erases the prior Ctrl+C payload.
- `state.clipboardHtml` is non-empty immediately after a context-menu Copy with a
  selection, and unchanged when Copy is invoked with `viewerCanCopy === false`.
- Keyboard Ctrl+C behavior is unchanged; Edit > Copy in the web menu is no longer inert.

## Regression tests to add

- **Unit (`src/app/editor/mobile-clipboard/index.test.ts`):** simulate an event-lifetime
  DataTransfer — a stub whose `setData`/`getData` throw or return `''` after a microtask
  ("neutered after dispatch") — pass it to `writeCopyData`, and assert
  `state.clipboardHtml` still ends up with the copied nodes' HTML and never becomes `''`
  while nodes are selected.
- **Unit (`src/app/editor/mobile-clipboard/index.test.ts`):** pre-populate
  `state.clipboardHtml = '<prior copy>'`; run `writeCopyData` with a DataTransfer that
  yields `''` from `getData`; assert the prior buffer content is not clobbered.
- **Unit (`src/app/editor/canvas/menu/actions.test.ts`):** `execCommand('copy')` (or its
  replacement) invokes the internal-buffer copy (`store.mobileCopy` spy) and does not
  depend on `document.execCommand`'s event round-trip to populate the buffer.
- **Integration (jsdom, `src/app/shell/keyboard/clipboard`):** mount
  `bindEditorClipboard`, dispatch a synthetic `copy` ClipboardEvent whose `clipboardData`
  is frozen after dispatch, then run `mobilePaste`; assert nodes are pasted.
- **E2E (gym/CDP):** select node → right-click > Copy → right-click empty canvas >
  "Paste here" → assert node count increased by 1 and the new node's content matches;
  repeat with Ctrl+C-then-context-Copy ordering to cover the clobber case.
