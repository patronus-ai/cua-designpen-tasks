# pid 10106 — rotation not exposed by the read API

## Root cause
- `set_rotation` (`packages/core/src/tools/modify/geometry.ts:11-16`) sets `node.rotation = angle` and returns only `{ id, rotation }` — a minimal echo, not read-back state.
- `get_node` → `nodeToResult` → `nodeProxyToJSON` (`packages/core/src/figma-api/serialization.ts:64-126`) emits `id,type,name,x,y,width,height`, conditional `fills/strokes/effects/opacity/cornerRadius/visible`, text props, `vectorNetwork`, auto-layout props, `boundVariables`, `children`. There is **no** `rotation` and **no** `absoluteBoundingBox`. `width`/`height` are node-local (unrotated), so they stay 100x100 after a 45° rotation.

The failing agents were correct: the geometry cannot be verified through the read API. (Their "center moved / wrong AABB" observations came from `viewport_zoom_to_fit` bounds, not from `set_rotation`.)

## Proposed fix
Add `rotation` to `nodeProxyToJSON`, emitted when non-zero (mirror the `opacity !== 1` pattern). Optionally expose `absoluteBoundingBox`.

## Acceptance criteria
- `get_node` on a rotated node includes `rotation`.
- (If AABB added) 100x100 square rotated 45° reports AABB ~141.42x141.42.

## Disposition
APP BUG / read-API gap — filed RLCU-2653. Task cannot pass until rotation is readable. No task/prompt change; staged for retest post-deploy.
