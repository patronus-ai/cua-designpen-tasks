# DesignPen [MCP tools]: 'eval' fails QA — 5/5 runs report broken workflow (10005-eval-mcp)

Description:
The `eval` MCP tool for DesignPen/OpenPencil (gated behind `OPENPENCIL_MCP_EVAL=1`) is not exposed in the QA environment, so the workflow cannot even start. The agent's available MCP toolset consisted of only three tools — `get_node`, `find_nodes`, and `viewport_zoom_to_fit` — all read-only or viewport-only, indicating the `OPENPENCIL_MCP_EVAL=1` flag is not enabled. With no tool capable of creating or modifying nodes, the five requested "Box" rectangles were never created and the document stayed completely empty. The fix is environment/config: expose the `eval` tool (enable the flag) for this task.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Connect via MCP (task requires the environment to be started with OPENPENCIL_MCP_EVAL=1) and list the available MCP tools.
3. Attempt to call the eval tool with JavaScript that creates five 60x60 rectangles named Box 1 through Box 5 at y=0 with x positions 0, 80, 160, 240 and 320.
4. Call viewport_zoom_to_fit.
5. Verify with find_nodes (name "Box", type RECTANGLE) and get_node on the document root.

Actual Result:

- No `eval` tool is exposed; the available MCP toolset consists of only `get_node`, `find_nodes`, and `viewport_zoom_to_fit` — all read-only or viewport-only, none can create or modify nodes.
- `find_nodes` for name "Box" returns 0 results; `find_nodes` for type `RECTANGLE` returns 0 results.
- `get_node` on the document root (`0:1`) shows only a single empty canvas "Page 1" (`0:2`) with no children; `viewport_zoom_to_fit` reports bounds `0×0` at origin — the document is entirely empty.
- The five 60x60 "Box 1"–"Box 5" rectangles were never created because no tool capable of creating them exists in the toolset.

Expected Result:
With `OPENPENCIL_MCP_EVAL=1` set, the `eval` MCP tool should be present in the toolset and executing the JavaScript should create the five Box rectangles, verifiable via `find_nodes`/`get_node`.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_22f3a923-353a-45e9-b5f7-cf15df032016.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_25fa6812-bbcb-4a38-b050-858156efa4a3.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_326d1403-e211-43dc-abb2-a905d57ddb04.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4f16503f-103e-47eb-b46e-c68150d3d553.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bcc9d8bf-9d2b-47ce-b92e-ca7a37e6f7a4.txt`

Agent report (verbatim tail of failing run):

```
## Report

**Task outcome: Could not be completed — the required `eval` tool is not available.**

### What I found:

1. **Missing `eval` tool**: The task requires calling an `eval` MCP tool with JavaScript (gated behind `OPENPENCIL_MCP_EVAL=1`). My available MCP toolset consists of only three tools: `get_node`, `find_nodes`, and `viewport_zoom_to_fit`. No `eval` tool is exposed, indicating the `OPENPENCIL_MCP_EVAL=1` flag is not enabled in this environment. All of my available tools are read-only or viewport-only — none can create or modify nodes.

2. **Verification results** (using the available tools):
   - `find_nodes` for name "Box" → **0 results**
   - `find_nodes` for type `RECTANGLE` → **0 results**
   - `get_node` on the document root (`0:1`) → contains only a single empty canvas "Page 1" (`0:2`) with no children
   - `viewport_zoom_to_fit` on the page → bounds are `0×0` at origin, confirming an entirely empty document

3. **Conclusion**: The five 60×60 rectangles ("Box 1" through "Box 5" at y=0, x=0/80/160/240/320) were **not created**, because there is no tool capable of creating them. The document remains empty.

### What went wrong

The core blocker is that the `eval` MCP tool required by the task is not present in my toolset (`OPENPENCIL_MCP_EVAL=1` appears not to be set), so node creation was impossible; verification confirmed the document is empty and no Box rectangles exist.

verdict: not-approve
```
