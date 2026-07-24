# DesignPen [MCP tools]: 'viewport get' fails QA — 5/5 runs report broken workflow (10120-viewport-get-mcp)

Description:
The viewport set/get round-trip is broken in the DesignPen/OpenPencil design app. `viewport_set(x=100, y=200, zoom=1)` echoes success (`{x: 100, y: 200, zoom: 1}`), but `viewport_get` then reports `center: {x: 640, y: 360}, zoom: 1` — exactly the browser viewport's pixel center (1280/2, 720/2), not the values just set. `viewport_get` also fails to reflect a subsequent `viewport_zoom_to_fit` (which reported center (665, 385)), still returning (640, 360). Either `viewport_set` silently fails to apply, or `viewport_get` returns a fixed screen-space center instead of the actual canvas viewport state. Node creation itself works correctly.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Call the `viewport_set` MCP tool with x=100, y=200, zoom=1 — it returns success.
3. Call `viewport_get` and compare against the values just set.
4. Create a 50x50 rectangle named "Anchor" at the x,y that `viewport_get` returned.
5. Call `viewport_zoom_to_fit` on the rectangle.
6. Call `viewport_get` again and compare against the center that `viewport_zoom_to_fit` reported.

Actual Result:

- `viewport_set(x=100, y=200, zoom=1)` returns `{x: 100, y: 200, zoom: 1}`, claiming success.
- `viewport_get` returns `center: {x: 640, y: 360}, zoom: 1` — not matching the set values; (640, 360) is exactly the browser viewport's pixel center (1280/2, 720/2).
- After `viewport_zoom_to_fit` reports `center: {x: 665, y: 385}`, a final `viewport_get` still returns `center: {x: 640, y: 360}, zoom: 1`, inconsistent with the zoom-to-fit result.
- The rectangle deliverable itself succeeded: `get_node("0:3")` shows RECTANGLE "Anchor" at (640, 360), 50x50, and `find_nodes` finds exactly 1 match.

Expected Result:
`viewport_get` should return the actual current canvas viewport state: after `viewport_set(100, 200, zoom=1)` it should report those values, and after `viewport_zoom_to_fit` it should report the new fitted center, so the set/get round-trip is consistent.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7b356036-a226-414a-a3f3-9d650eaf692e.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7ff7654f-0e8d-4213-8855-9e2a163733e8.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8c8cff12-0fd3-4004-982a-b9ea31761fce.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_abb5226c-8dff-4f7a-a397-c39e35e0352f.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ec4fb5e6-e8bf-4937-90e7-04123001b0b8.txt`

Agent report (verbatim tail of failing run):

```
**Report of findings:**

All requested operations executed, and verification confirms the rectangle is correct:

1. **viewport_set(x=100, y=200, zoom=1)** → returned `{x: 100, y: 200, zoom: 1}`, claiming success.
2. **viewport_get** → returned `center: {x: 640, y: 360}, zoom: 1`. ⚠️ This does **not** match the values I just set (100, 200) — despite viewport_set echoing success, viewport_get reported the viewport centered at (640, 360), which is exactly the browser viewport's pixel center (1280/2, 720/2).
3. **create_shape** → Per the instructions, I created the 50×50 RECTANGLE named "Anchor" at exactly the returned coordinates (640, 360). Created as node `0:3`.
4. **viewport_zoom_to_fit(["0:3"])** → returned `center: {x: 665, y: 385}` and `bounds: {x: 640, y: 360, width: 50, height: 50}` — bounds exactly match the created rectangle.
5. **Verification:**
   - `get_node("0:3")` → RECTANGLE "Anchor" at x=640, y=360, width=50, height=50 ✅ (correct name, size, and position per spec)
   - `find_nodes(name="Anchor", type=RECTANGLE)` → exactly 1 match, id `0:3` ✅
   - Final `viewport_get` → `center: {x: 640, y: 360}, zoom: 1` — ⚠️ again inconsistent, since zoom_to_fit had just reported centering on (665, 385).

**Summary:** The rectangle "Anchor" (50×50 at 640, 360) was created exactly at the coordinates viewport_get returned and verified successfully. However, I observed a tooling inconsistency/bug: `viewport_get` never reflected viewport changes — it reported (640, 360) both after `viewport_set(100, 200)` and after `viewport_zoom_to_fit` reported a center of (665, 385). Either `viewport_set` silently fails to apply, or `viewport_get` returns a fixed screen-space center instead of the actual canvas viewport state. The main deliverable succeeded, but the viewport set/get round-trip did not behave correctly.

verdict: not-approve
```
