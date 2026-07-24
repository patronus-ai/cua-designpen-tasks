# pid 10101 — flaky truncation on large self-encoded base64 input

## Root cause
NOT an app bug. `set_image_fill` returns a plain object with no `base64`/`mimeType` (`packages/core/src/tools/modify/paint.ts:137`), so it emits no image content block and is not the 40014 PIL-crash class. The failure is a self-inflicted input-size/variance problem: "encode a base64 PNG yourself" led to large/variable inputs whose echo occasionally truncated the run before the marker.

## Fix (prompt)
Give the exact 1x1 PNG base64 string to pass verbatim; forbid self-encoding. Small deterministic input eliminates the truncation.

## Disposition
PROMPT FIX applied to definition.yaml. Retest on Taiga.
