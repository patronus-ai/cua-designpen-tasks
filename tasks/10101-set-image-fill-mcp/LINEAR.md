# DesignPen [MCP tools]: 10101-set-image-fill flaky — NOT an app bug (prompt fix)

No Linear issue — root cause is task/prompt, not the app. The `set_image_fill` return path is clean (`packages/core/src/tools/modify/paint.ts:137` returns `{id, imageHash, scaleMode}`, no image content block), so it is not a 40014-class crash.

Description:
The prompt told the agent to "encode yourself" a base64 PNG. Agents produced variable/large base64 blobs; the large tool *input* being echoed into the transcript occasionally truncated the run before the final verdict, yielding score 0 (4/5 passed).

Fix applied (definition.yaml):
- Provide an exact, tiny 1x1 PNG base64 literal to pass verbatim; forbid self-encoding. Deterministic, small input removes the truncation vector.

Evidence:
- Snapshot `ed08b6ef-079d-4775-8f61-7dc801053712`, job `job-20260724111822Z`, model `claude-opus-4-8`
- `10101-set-image-fill-mcp`: 4/5 passed
- Failing run `08bd9719-f278-4b87-bcd9-49ceeaed0ea2` (transcript truncates right after create_shape, before set_image_fill completes).
