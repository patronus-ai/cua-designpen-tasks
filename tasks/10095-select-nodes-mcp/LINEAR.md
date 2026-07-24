# DesignPen [MCP tools]: 'select nodes' fails QA — 5/5 runs report broken workflow (10095-select-nodes-mcp)

Description:
Selection state does not persist between MCP tool calls in the DesignPen/OpenPencil design app. The `select_nodes` tool returns success (echoing `"selected": ["0:3","0:4"]`), but an immediate `get_selection` returns an empty `selection: []`, so any selection-dependent operation fails — specifically, `distribute` called without explicit `ids` errors with `"Select or pass at least 2 nodes"`. The distribute logic itself is fine: calling `distribute` with explicit `ids` succeeds and produces correct geometry, proving the bug is isolated to selection persistence between tool calls.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Create two 100x100 rectangles via MCP: P1 at (0,0) and P2 at (150,0).
3. Call `select_nodes` with both node ids (e.g. `["0:3","0:4"]`) — it returns success.
4. Call `get_selection` — observe it returns empty.
5. Call `distribute` with `axis: horizontal`, `gap: 30`, WITHOUT passing `ids`, so it should operate on the selection.

Actual Result:

- `select_nodes(["0:3","0:4"])` returns success (`"selected": ["0:3","0:4"]`), but the selection does not persist: an immediate `get_selection` returns `selection: []`.
- `distribute` without `ids` fails with `"Select or pass at least 2 nodes"`. Reproduced twice with identical failures.
- Workaround: `distribute(axis: horizontal, gap: 30, ids: ["0:3","0:4"])` with explicit ids succeeds (`"distributed": 2`) and produces the correct 30px gap (P2 moved to x=130).

Expected Result:
The selection set by `select_nodes` should persist across subsequent tool calls: `get_selection` should return the selected ids, and `distribute` (and other selection-dependent tools) called without `ids` should operate on that selection.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0402d33c-0275-4011-8a3d-fa236e35154b.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_1e18d08c-95ed-4dbd-8c26-bf14570f2617.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6163d279-80e1-4239-a740-890551d77952.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_70b2ebae-91ed-4171-905a-0638b559f5fe.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_cb239e60-99c8-4c19-ad7c-7d84f3bfb718.txt`

Agent report (verbatim tail of failing run):

```
## Report

**What I did and found:**

1. **Created rectangles** — P1 (`0:3`) at (0,0) and P2 (`0:4`) at (150,0), both 100×100. ✅ Verified via `find_nodes` and `get_node`.

2. **Selection bug encountered** — `select_nodes(["0:3","0:4"])` returned success (`"selected": ["0:3","0:4"]`), but the selection did not persist: an immediate `get_selection` returned an empty `selection: []`. Consequently, `distribute` called **without ids** (as required) failed with `"Select or pass at least 2 nodes"`. I reproduced this twice (select → distribute, and select → get_selection), with identical failures.

3. **Diagnostic workaround** — Calling `distribute(axis: horizontal, gap: 30, ids: ["0:3","0:4"])` with explicit ids succeeded (`"distributed": 2`), proving the distribute logic itself is fine and the bug is isolated to selection persistence between tool calls.

4. **Zoom to fit** — succeeded; viewport centered on (115, 50) with bounds (0, 0, 230×100).

5. **Final verification** —
   - P1: x=0, y=0, 100×100 (anchored, unchanged) ✅
   - P2: x=130, y=0, 100×100 → gap = 130 − 100 = **30 px exactly** ✅
   - Combined bounds 0→230 wide match the zoomed viewport ✅

**Conclusion:** The final geometry is correct (P2 moved from x=150 to x=130, giving exactly the requested 30px gap), but this was only achieved via a workaround. The specifically requested path — running `distribute` without ids so it operates on the selection — is broken: `select_nodes` claims success while the selection is not actually retained, making any selection-dependent operation fail.

The selection state does not persist after `select_nodes` (get_selection returns empty, and distribute-on-selection errors out), so the task as specified could not be completed without passing ids explicitly.

verdict: not-approve
```
