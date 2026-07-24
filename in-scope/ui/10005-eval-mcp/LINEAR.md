# DesignPen [MCP tools]: `eval` reports success as an error — "Cannot use 'in' operator to search for 'base64'" (10005-eval-mcp)

Linear: RLCU-2652 — https://linear.app/patronus-ai/issue/RLCU-2652

Description:
The MCP tool-result post-processor (`packages/mcp/src/tool/registration.ts:69`) applies the JS `in` operator to the raw tool return value without checking it is an object. `eval` returns arbitrary JS (arrays/strings/numbers), so `'base64' in r` throws `Cannot use 'in' operator to search for 'base64' in [...]`. The script has already executed successfully; the crash happens only in result serialization, so a correct run is surfaced to the agent as an error and it ends `verdict: not-approve`.

Steps to Reproduce:

1. Open http://cua_designpen.web (MCP tools).
2. Call `eval` with a script that returns a non-object, e.g. an array of created-node descriptors (`JSON.stringify(created)` or returning the array directly).
3. Observe the tool response.

Actual Result:
`{"error":"Cannot use 'in' operator to search for 'base64' in [...]"}` — even though the five rectangles were created correctly (confirmed by follow-up `find_nodes`/`get_node`).

Expected Result:
A non-object return (array/string/number) is passed through as text; no throw.

Estimate: S (1 point) — one-line guard.

Evidence:
- Snapshot `ed08b6ef-079d-4775-8f61-7dc801053712`, job `job-20260724111822Z`, model `claude-opus-4-8`
- `10005-eval-mcp`: 1/5 passed (fails whenever the eval return is a non-object)
- Failing run `a823015a-54a5-48cb-9ad5-168518ac5ef3`

Fix: `if (r && typeof r === 'object' && !Array.isArray(r) && 'base64' in r && 'mimeType' in r)` at registration.ts:69.
