# 10125 — MCP `save_file` with explicit path returns 404

All paths below are in the app source at `/Users/mateuszszczech/Desktop/patronus-gyms/cua_designpen` (working tree == deployed release `cua_designpen-0.1.8` for every cited file; verified by diff against `apps/cua_designpen/release.tar.gz`).

## Root cause analysis

The `/save-file` HTTP endpoint that named saves depend on is **never registered at runtime in the gym**, because its enable-gate reads env vars that only exist at *build* time. The MCP tool layer, meanwhile, enables named saves unconditionally (it falls back to `process.cwd()`), so the two layers disagree.

Full request chain:

1. **MCP tool** `save_file` — `packages/mcp/src/tool/registration.ts:101-130`. Named-path support is keyed off `resolvedRoot` (`registration.ts:26`):
   ```ts
   const resolvedRoot = options.mcpRoot ? resolve(options.mcpRoot) : null
   ```
   and `mcpRoot` **always has a value** because serve.js falls back to cwd (`scripts/serve.js:35`):
   ```js
   mcpRoot: process.env.OPENPENCIL_MCP_ROOT?.trim() || process.cwd(),
   ```
   In the gym the app is launched via `npm start` from `/opt/patronus-gym/apps/cua_designpen`, so both `"artifact.fig"` and `"/opt/patronus-gym/apps/cua_designpen/artifact.fig"` pass `resolveSafePath` (registration.ts:120-121) and the RPC is forwarded to the browser.

2. **Browser handler** — `src/app/automation/bridge/file-handlers.ts:26-48` (`handleSaveFile`). In automation builds `snapshotEnabled` is true (baked in by `VITE_OPENPENCIL_AUTOMATION=1` at *vite build* time, `src/app/automation/snapshot.ts:21-24`), so an explicit path goes to the server:
   ```ts
   if (snapshotEnabled) {
     const written = path ? await postSaveFile(store, path) : undefined
     await postSnapshot(store)
     return written ? { ok: true, path: written } : { ok: true }
   }
   ```

3. **Client POST** — `src/app/automation/snapshot.ts:77-94` (`postSaveFile`, release 0.1.8: lines 71-88):
   ```ts
   const res = await fetch(`/save-file?path=${encodeURIComponent(path)}`, { method: 'POST', ... })
   if (!res.ok) {
     const message = await readErrorMessage(res)
     throw new Error(message || `Save to "${path}" failed: ${res.status} ${res.statusText}`)
   }
   ```
   This is the exact error string observed (`Save to "<path>" failed: 404 Not Found`).

4. **Server gate — the defect** — `scripts/serve.js:255-257` and `278`:
   ```js
   const SAVE_FILE_ENABLED =
     Boolean(process.env.OPENPENCIL_MCP_ROOT?.trim()) || process.env.VITE_OPENPENCIL_AUTOMATION === '1'
   const SAVE_ROOT = resolve(process.env.OPENPENCIL_MCP_ROOT?.trim() || process.cwd())
   ...
   if (SAVE_FILE_ENABLED) {
     app.post('/save-file', ...)   // serve.js:279
     app.get('/save-file', ...)    // serve.js:349
   }
   ```
   In the gym runtime **neither env var is set**:
   - `VITE_OPENPENCIL_AUTOMATION=1` is set only as an inline prefix of the `build:gym` npm script (`package.json:21`: `"build:gym": "... VITE_OPENPENCIL_AUTOMATION=1 VITE_OPENPENCIL_SNAPSHOT=1 vite build"`), consumed by Vite and gone before `npm start` runs. (The comment at serve.js:250-252 claims "the automation build flag baked into gym images (whose ENV persists to the runtime process)" — that is only true of the app's own `Dockerfile`, whose builder stage sets `ENV VITE_OPENPENCIL_AUTOMATION` (Dockerfile:41-42); the gym image is built by `gym-browser-use/scripts/install_apps.sh:69-70`, which runs `npm run build:gym` and preserves no env.)
   - `OPENPENCIL_MCP_ROOT` is set nowhere in gym-browser-use (grep of `gym_browser_use/`, `environments/cua_designpen/*.yaml`, and the launcher `patronus_gym_cua/webapp.py` finds no occurrence; `environments/cua_designpen/gym.config.yaml` has no `web.env`).

   So `SAVE_FILE_ENABLED === false`, the route block is skipped, and `POST /save-file` falls through `serveStatic` (serve.js:406) to a **GET-only** SPA fallback (`app.get('/*')`, serve.js:410) → Hono's default `404 Not Found`.

Why pathless save succeeds: `handleSaveFile` without a path only calls `postSnapshot` → `POST /snapshot`, which is registered unconditionally (`scripts/serve.js:151`), so the tool returns `{"saved":true}`.

Summary: **client and MCP bridge decide "named saves supported" via a cwd fallback; the server decides via raw env vars with no fallback.** In any deployment that neither sets `OPENPENCIL_MCP_ROOT` nor carries `VITE_OPENPENCIL_AUTOMATION` into the runtime env — i.e., the gym — every explicit-path `save_file` 404s.

## Proposed fix

Make the server gate consistent with the bridge, in `scripts/serve.js`:

1. Since the bridge already runs in-process with `mcpRoot` falling back to `process.cwd()` (serve.js:35), register `/save-file` whenever the MCP bridge is up, and root it at the same directory. Concretely, replace serve.js:255-256 with:
   ```js
   const SAVE_FILE_ENABLED = Boolean(mcpApp) // same surface as the bridge that advertises named saves
   ```
   (keep `SAVE_ROOT` as is — it already uses the same `OPENPENCIL_MCP_ROOT || cwd` expression as the bridge, so containment stays aligned with the bridge's `resolveSafePath`).
2. If the unauthenticated-write concern for hosted snapshot builds must be preserved, gate instead on the same condition that distinguishes automation from hosted builds at runtime — e.g. have the gym launcher (or `environments/cua_designpen/gym.config.yaml` `apps.cua_designpen.web.env`) set `OPENPENCIL_MCP_ROOT=/opt/patronus-gym/apps/cua_designpen`. This is the minimal no-app-change fix, but it leaves the latent client/server inconsistency; option 1 is the real fix.
3. Optional hardening: when the route is disabled, `postSaveFile`'s 404 should surface a self-explanatory error; add an explicit `app.post('/save-file', c => c.json({ error: 'Named saves are disabled on this server' }, 501))` in the else-branch so the MCP error is actionable rather than a bare 404.

## Acceptance criteria

- In a gym container (launched via `npm start` with neither `OPENPENCIL_MCP_ROOT` nor `VITE_OPENPENCIL_AUTOMATION` in the runtime env), MCP `save_file` with `path: "artifact.fig"` returns success and the file exists at `/opt/patronus-gym/apps/cua_designpen/artifact.fig` with ZIP (`PK`) magic bytes.
- Same for the absolute in-root path `/opt/patronus-gym/apps/cua_designpen/artifact.fig`; the tool result `path` equals the server-confirmed written path.
- `save_file` with an out-of-root path (e.g. `/tmp/x.fig`) still fails with a containment error (400 from the server or the bridge's `resolveSafePath` error), not a 404.
- Pathless `save_file` still returns `{"saved":true}` and flushes `/snapshot`.
- `open_file` of a path just written by `save_file` round-trips (GET `/save-file` serves the bytes).
- Hosted snapshot-only builds (if option 2/gating retained): `/save-file` is absent or returns a deliberate, non-404 error; no unauthenticated arbitrary write surface appears.

## Regression tests to add

- **Server unit (serve.js route registration):** boot serve.js with env `{}` (no `OPENPENCIL_MCP_ROOT`, no `VITE_OPENPENCIL_AUTOMATION`) and assert `POST /save-file?path=a.fig` with valid ZIP bytes returns 200 with `{ written: <abs path under cwd> }` (option 1) — i.e., assert it does NOT return 404. Companion case: out-of-root path returns 400 with `Path is outside the allowed root`.
- **Server unit:** `GET /save-file?path=a.fig` after the POST returns the same bytes; `GET` of a missing file returns 404 with `File not found` (the only legitimate 404).
- **Consistency test:** assert the gate used to register `/save-file` and the `mcpRoot` passed to `startMcpBridge` are derived from the same expression (e.g. export both from serve.js or a shared module and compare in a unit test), so the bridge can never advertise named saves the HTTP surface rejects.
- **E2E (gym image):** run the container, call MCP `save_file {"path":"artifact.fig"}`, assert tool result `{saved:true, path:".../artifact.fig"}` and that a follow-up `open_file` on that path succeeds; repeat with the absolute in-root path.
