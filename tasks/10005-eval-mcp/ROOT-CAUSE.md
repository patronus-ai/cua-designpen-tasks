# pid 10005 — `eval` result serialization throws on non-object returns

## Root cause
`packages/mcp/src/tool/registration.ts:69`
```ts
if (r && 'base64' in r && 'mimeType' in r) {
```
`r` = `res.result` (registration.ts:43), typed `RpcJsonObject | undefined` but at runtime whatever the RPC returns. The `eval` tool (`packages/core/src/tools/analyze/eval/index.ts:13-27`) returns the script's value verbatim (`if (result !== undefined && result !== null) return result`), so arrays/strings/numbers land here. The guard is only `r &&` (truthiness) — no `typeof r === 'object'`. `'base64' in [array]` throws.

The two sibling checks are safe because they use property *access*, not `in`: registration.ts:48 (`typeof r.base64 === 'string'`, export_fig) and :63 (export_image). Only line 69 uses `in`.

Class-mate of the 40014 bug: same generic `{base64,mimeType}`→image branch, different failure (throw vs PIL crash). The gym-side `mcp_proxy._sanitize_non_image_content` sanitizer cannot help — this throws *inside* the app before returning.

## Proposed fix
```ts
if (r && typeof r === 'object' && !Array.isArray(r) && 'base64' in r && 'mimeType' in r) {
```

## Acceptance criteria
- `eval` returning `[1,2,3]` / `"hello"` / `42` passes through as text, no throw.
- Tools returning `{base64, mimeType}` still emit their image/file content block.

## Disposition
APP BUG — filed RLCU-2652. Task cannot pass reliably until the app fix ships. No task/prompt change; staged for retest post-deploy.
