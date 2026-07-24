# DesignPen [MCP tools]: bound opacity stays stale after `set_variable` (10063-get-collection-mcp)

Linear: RLCU-2654 — https://linear.app/patronus-ai/issue/RLCU-2654

Description:
When a FLOAT variable is bound to a node's opacity and the variable value is later changed via `set_variable`, the node's stored `opacity` scalar is not recomputed. `get_node` then reports `opacity: 0.3` (the value captured at bind time) while `boundVariables.opacity.resolvedValue: 0.9` — the two contradict each other, and because rendering/export read the stored scalar, the node actually renders at the stale value. The agent flags the inconsistency and votes `not-approve`.

Steps to Reproduce:

1. Open http://cua_designpen.web (MCP tools).
2. Create collection "Motion" with FLOAT variable `speed` = 0.3, bound to the opacity of a rectangle "Runner".
3. `set_variable` speed = 0.9.
4. `get_node` on Runner.

Actual Result:
`opacity: 0.3` on the node, but `boundVariables.opacity.resolvedValue: 0.9`.

Expected Result:
Node `opacity` recomputes to 0.9 (matches resolvedValue).

Estimate: S (1 point) — one call.

Evidence:
- Snapshot `ed08b6ef-079d-4775-8f61-7dc801053712`, job `job-20260724111822Z`, model `claude-opus-4-8`
- `10063-get-collection-mcp`: 4/5 passed
- Failing run `02348053-9b68-49df-a4ae-0ab9ca07d296`
