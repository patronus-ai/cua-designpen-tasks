# 10124 — Failed `open_file` (invalid zip) clobbers the active unsaved document

All paths below are in the app source at `/Users/mateuszszczech/Desktop/patronus-gyms/cua_designpen` (working tree == deployed release `cua_designpen-0.1.8` for every cited file; `src/app/tabs/index.ts` is byte-identical between the two).

This pid also hits the same `save_file` 404 as pid 10125 (see `10125-save-file-mcp.md` — `/save-file` routes not registered because `SAVE_FILE_ENABLED` is false at runtime, `scripts/serve.js:255-278`). The section below covers the additional data-loss defect.

## Root cause analysis

`openFileInNewTab` **creates and activates the destination tab/store before parsing the file, and has no error rollback**, so a parse failure strands the app on a fresh blank document; the automation build's snapshot autosave then persists that blank document over the previous one within ~3s, making the loss durable.

Call chain for MCP `open_file`:

1. `packages/mcp/src/tool/registration.ts:132-154` → RPC `open_file` to the browser.
2. `src/app/automation/bridge/file-handlers.ts:82-104` (`handleOpenFile`): with `snapshotEnabled` it fetches the bytes back via `GET /save-file` (`fetchSavedFile`, `src/app/automation/snapshot.ts:99-106`) — this succeeds for any existing `.fig`-named file regardless of content — then:
   ```ts
   await openFileInNewTab(new File([blob], name), undefined, path)
   ```
3. **The defect** — `src/app/tabs/index.ts:108-148` (`openFileInNewTab`):
   ```ts
   const current = activeTab.value
   const isUntouched =
     current?.store.state.documentName === 'Untitled' && !current.store.undo.canUndo
   let store: EditorStore
   if (isUntouched && current) {
     notifyTabWillOpenDocument?.(current.id)   // re-keys the collab room BEFORE parse
     store = current.store
   } else {
     store = createTab().store                  // line 121: NEW BLANK TAB, ACTIVATED
   }
   ...
   store.state.documentName = documentName      // line 125: name overwritten BEFORE parse
   store.state.loading = true
   ...
   try {
     const { graph: imported, ... } = isFig
       ? { graph: await readFigFile(file, ...), ... }   // line 133: THROWS on invalid zip
       : ...
     await applyImportedDocument(store, imported)
   } finally {
     progress.done()
     store.state.loading = false                // no catch: no closeTab / no re-activate
   }
   ```
   - With an unsaved edited document (`canUndo` true, or name ≠ "Untitled"), line 121 runs `createTab()` (`tabs/index.ts:58-64`), which **immediately activates** the new empty store via `activateTab` (`tabs/index.ts:66-72`): `setActiveEditorStore`, `setOpenPencilStore` — the MCP bridge and every panel now point at a blank document.
   - `readFigFile` then throws on the invalid zip. The `try/finally` (lines 130-147) has **no catch**: the blank tab is never closed, the previous tab is never re-activated, and the error propagates to the MCP client as a failed tool call while the UI/bridge remain on the blank document.
4. **Durable clobber** — the snapshot autosave tracks the *active* store: `src/views/EditorView.vue:178-184` wires `startSnapshotAutosave(getActiveStore, ...)`, and `startSnapshotAutosave` (`src/app/automation/snapshot.ts:215-242`) debounce-POSTs the active store's bytes to `/snapshot` (3s debounce / 10s maxWait). After the failed open, the active store is the blank tab, so the container-global snapshot — the only durable copy in the gym, and what grading reads via `OPENPENCIL_SNAPSHOT_PATH` — is overwritten with an empty document. The old store still exists in the background tab's memory, but for a headless agent (and after any reload, which restores from the clobbered snapshot) the previous nodes are gone.
   - The `isUntouched` in-place branch has the analogous problem in milder form: it re-keys the collab room (line 118) and overwrites `documentName` (line 125) before validation, though it does not discard the graph.

So the answer to "why does it tear down the current document before validating the file loads?" is: it doesn't tear down the old store — it *switches the app to a brand-new blank store first* (tab creation doubles as activation), parses second, and on failure never switches back; autosave then makes the blank state authoritative.

## Proposed fix

In `src/app/tabs/index.ts`, parse before mutating any live state, and roll back on failure:

1. Reorder: read/parse the file into `imported` **before** choosing/creating the destination store — i.e., move the `readFigFile` / `io.readDocument` call above the `isUntouched`/`createTab()` block. Only after a successful parse: re-key the room (`notifyTabWillOpenDocument`), create/activate the tab, set `documentName`, and `applyImportedDocument`.
2. If reordering is too invasive (progress toast wants a target store), wrap the body in `try/catch`: on error, if a new tab was created, `closeTab(newTab.id)` and re-`activateTab(previousTab)`; if the in-place branch ran, restore the previous `documentName` (and re-key the room back). Re-throw so the MCP tool still reports failure.
3. Defense in depth in `handleOpenFile` (`src/app/automation/bridge/file-handlers.ts:94-97`): validate magic bytes (`PK`) of the fetched blob before calling `openFileInNewTab`, mirroring the server-side check in `POST /save-file` (`scripts/serve.js:322`), so obviously-corrupt files fail before any UI state is touched.

## Acceptance criteria

- With an unsaved document containing nodes, MCP `open_file` on an existing but corrupt (non-zip) `.fig` returns a tool error AND the active document afterwards is the original one: same tab id, same `documentName`, same node ids/count (verifiable via `get_node`/document snapshot tools).
- No new tab remains after the failed open (`tabCount()` unchanged).
- The server snapshot is not overwritten with a blank document: waiting >10s (autosave maxWait) after the failed open and then reloading the page restores the original nodes.
- A successful `open_file` on a valid `.fig` still opens in a new tab (edited current doc) or in place (untouched "Untitled" doc), unchanged behavior.
- The in-place ("untouched") failure path leaves `documentName === 'Untitled'` and the collab room key unchanged.

## Regression tests to add

- **Unit (`src/app/tabs/index.ts`, vitest):** create a tab, add a node (so `canUndo` true), call `openFileInNewTab(new File([Uint8Array.of(1,2,3)], 'bad.fig'))`, assert it rejects, `tabCount()` is unchanged, `activeTab.value` is the original tab, and the original store's graph still contains the node.
- **Unit (untouched branch):** fresh "Untitled" tab, same corrupt file — assert rejection, `documentName` still `'Untitled'`, and the `setTabWillOpenDocumentListener` callback was either not fired or fired-and-reverted (room key unchanged).
- **Unit (success path preserved):** valid `.fig` fixture opens into a new tab, becomes active, graph populated — guards the reorder against breaking normal opens.
- **Integration (bridge):** `handleOpenFile` with a store containing nodes and a mocked `fetchSavedFile` returning non-zip bytes — assert it throws and `getActiveStore()` is the same store instance with an unchanged scene graph.
- **E2E (gym):** seed a doc, edit it via MCP, `save_file` a corrupt file to disk out-of-band (or stage one), `open_file` it, assert tool error, then `get_node` on a pre-existing node id still succeeds; reload the page and assert the document restores with the original nodes (snapshot not clobbered).
