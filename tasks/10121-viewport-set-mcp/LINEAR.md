# DesignPen [MCP tools]: 'viewport set' fails QA — 5/5 runs report broken workflow (10121-viewport-set-mcp)

Description:
The `viewport_set` MCP tool in the DesignPen/OpenPencil design app claims success but its values are never reflected by `viewport_get`. After `viewport_set(x=140, y=260, zoom=2)` returns success echoing `{x: 140, y: 260, zoom: 2}`, `viewport_get` reports center (640, 360) at zoom 1 — a stale/default state it keeps returning regardless of set or zoom-to-fit operations (it also contradicted the center (660, 380) that `viewport_zoom_to_fit` reported). The set/get mismatch was reproduced twice in the same run. Shape creation works fine; the bug is confined to the viewport tooling.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Call the `viewport_set` MCP tool with x=140, y=260, zoom=2 — it returns success.
3. Call `viewport_get` and compare against the values just set; repeat the set/get cycle to rule out a fluke.
4. Create a 40x40 rectangle named "Marker" at the coordinates `viewport_get` reported.
5. Call `viewport_zoom_to_fit` on the rectangle.
6. Call `viewport_get` again and compare against the center that `viewport_zoom_to_fit` reported.

Actual Result:

- `viewport_set(x=140, y=260, zoom=2)` returns success, echoing `{x: 140, y: 260, zoom: 2}`.
- `viewport_get` reports center (640, 360) at zoom 1, not the values just set; the same mismatch occurred on a repeated set/get cycle.
- After `viewport_zoom_to_fit` reported a new center of (660, 380), a final `viewport_get` still reported center (640, 360) at zoom 1 — contradicting both the earlier `viewport_set` values and the zoom-to-fit center.
- The rectangle itself was created and verified correctly: `get_node("0:3")` shows RECTANGLE "Marker" at (640, 360), 40x40, and `find_nodes` finds exactly 1 match.

Expected Result:
`viewport_set(x=140, y=260, zoom=2)` should actually apply to the canvas viewport, and `viewport_get` should read back the current viewport state (including changes made by `viewport_zoom_to_fit`), making the set/get round-trip consistent and reliable.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6bfce8df-4b09-4ec4-b42a-ed04f84ccff1.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7c66c5ba-d763-4432-8828-07d2295e3fa7.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a45bc198-96bd-40fa-9568-9616513408af.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e0e695aa-7f55-435c-8720-7266243f0ed2.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e6a43894-de8b-45f7-9208-969dda3e03c6.txt`

Agent report (verbatim tail of failing run):

```
All verification steps complete. Here's my report:

## Report

**What I did:**
1. **`viewport_set(x=140, y=260, zoom=2)`** — returned success, echoing `{x: 140, y: 260, zoom: 2}`.
2. **`viewport_get`** — reported center **(640, 360) at zoom 1**, which does *not* match the values just set. I repeated the set/get cycle to rule out a fluke and got the same mismatch both times.
3. **Created the rectangle** — per instructions, I dropped the 40×40 rectangle named "Marker" at the *reported* coordinates (640, 360). Creation succeeded, returning node ID `0:3`.
4. **`viewport_zoom_to_fit(["0:3"])`** — succeeded, reporting bounds (640, 360, 40×40) and a new center of (660, 380).

**Verification findings:**
- `get_node("0:3")` confirms: `RECTANGLE` named **"Marker"**, at x=640, y=360, width=40, height=40 — exactly as intended. ✅
- `find_nodes(name="Marker", type=RECTANGLE)` confirms exactly **1 matching node** (`0:3`) exists on the canvas. ✅
- A final `viewport_get` still reports center (640, 360) at zoom 1 — which contradicts *both* the earlier `viewport_set` values (140, 260, zoom 2) *and* the center (660, 380) that `viewport_zoom_to_fit` just reported. ❌

**Conclusion:** The rectangle itself was created and verified correctly (correct name, size, and position). However, there is a clear bug in the viewport tooling: `viewport_set` claims success but its values are never reflected by `viewport_get`, and `viewport_get` appears to return a stale/default state (640, 360, zoom 1) regardless of set or zoom-to-fit operations. The viewport state reported by the tools is inconsistent and unreliable.

Because of this viewport_set/viewport_get inconsistency, the task did not go fully smoothly.

verdict: not-approve
```
