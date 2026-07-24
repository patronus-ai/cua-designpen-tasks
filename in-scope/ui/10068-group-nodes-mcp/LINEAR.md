# DesignPen [MCP tools]: 'group nodes' fails QA — 5/5 runs report broken workflow (10068-group-nodes-mcp)

Description:
The `group_nodes` MCP tool in the DesignPen/OpenPencil design app creates the group correctly but does not compute the group node's bounding box from its children. Grouping two 80x80 rectangles at (100,100) and (180,100) yields a group reporting `x:0, y:0, width:100, height:100` — an apparent default — instead of the correct combined box `x:100, y:100, width:160, height:80`. As a result, `viewport_zoom_to_fit` on the group frames a region at the origin that does not contain the rectangles at all (they span x:100-260, y:100-180). All tool calls return success; the defect is silent.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools, create an 80x80 rectangle at (100, 100).
3. Create a second 80x80 rectangle at (180, 100), side by side with the first (edges touching at x=180).
4. Call `group_nodes` with both rectangle ids.
5. Call `viewport_zoom_to_fit` on the resulting group node.
6. Inspect the group with `get_node` and compare its reported x/y/width/height against the children's combined bounding box.

Actual Result:

- The group node reports its own geometry as `x:0, y:0, width:100, height:100`, which does not match its children's combined bounding box (should be `x:100, y:100, width:160, height:80`).
- `viewport_zoom_to_fit` returned bounds `{x:0, y:0, 100×100}` centered at (50, 50) — a region that does not contain the rectangles (they span x:100-260, y:100-180), so zoom-to-fit framed the wrong area.
- Group structure itself is correct: exactly one group exists containing both 80x80 rectangles as children, and all tool calls executed without errors.

Expected Result:
The group's bounding box should be computed from its children (160x80 at (100,100) in this case), and `viewport_zoom_to_fit` on the group should frame the region actually containing the grouped shapes.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_24a5b5e0-de86-44a7-a7db-6ab2f76b35b2.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_97ec6a98-f9d4-4f7b-beec-5dd24e7921fe.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ba1c5419-79d1-4c7a-aca1-1ed85a87e46a.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ba7fc22c-1f26-48f8-b976-b0e2ed4101e6.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_dcef8f57-1afc-46fa-bf06-2f54233c2499.txt`

Agent report (verbatim tail of failing run):

```
All verification checks are complete. Here's my report:

## Report

**Actions performed (all via MCP tools):**
1. Created `Rect Left` (id `0:3`) — 80×80 at (100, 100) ✅
2. Created `Rect Right` (id `0:4`) — 80×80 at (180, 100), exactly adjacent to the first (side by side, edges touching at x=180) ✅
3. Called `group_nodes` with both ids → created `Group 1` (id `0:5`) ✅
4. Called `viewport_zoom_to_fit` on the group — the call returned successfully ✅

**Verification findings:**
- `find_nodes` confirms exactly 2 rectangles exist (`Rect Left`, `Rect Right`) and exactly 1 group (`Group 1`).
- `get_node("0:5")` confirms the group contains both rectangles as children, each 80×80, side by side at y=100 (x=100 and x=180).
- **Problem found:** the group node reports its own geometry as `x:0, y:0, width:100, height:100`, which does **not** match its children's combined bounding box (which should be `x:100, y:100, width:160, height:80`). Consequently, `viewport_zoom_to_fit` returned bounds `{x:0, y:0, 100×100}` centered at (50, 50) — a region that doesn't actually contain the rectangles (they span x:100–260, y:100–180). So the zoom-to-fit operation framed the wrong area due to the group's incorrect bounds.

**Summary:** The rectangles and group were created correctly and all tool calls executed without errors, but verification revealed a bug: the group's bounding box is not computed from its children (it reports 100×100 at the origin instead of 160×80 at (100,100)), which caused `viewport_zoom_to_fit` to fit an incorrect viewport region that excludes the actual shapes.

verdict: not-approve
```
