# DesignPen [MCP tools]: rotation is unverifiable — `get_node` never serializes `rotation` (10106-set-rotation-mcp)

Linear: RLCU-2653 — https://linear.app/patronus-ai/issue/RLCU-2653

Description:
`set_rotation` mutates `node.rotation`, but `get_node` (`nodeProxyToJSON`, `packages/core/src/figma-api/serialization.ts:64-126`) never serializes a `rotation` field or an absolute/axis-aligned bounding box. After rotating a node there is no read tool that can confirm the rotation, so an agent verifying its own work legitimately reports the result as unverifiable and votes `not-approve`.

Steps to Reproduce:

1. Open http://cua_designpen.web (MCP tools).
2. `create_shape` a 100x100 RECTANGLE named Tilted.
3. `set_rotation` angle 45.
4. `get_node` on the rectangle and look for the rotation.

Actual Result:
`get_node` returns `width:100, height:100` with no `rotation` field and no AABB. Rotation cannot be confirmed; a 45° rotation should imply an AABB of ~141x141 but none is exposed.

Expected Result:
`get_node` exposes `rotation` (and ideally an absoluteBoundingBox) so applied rotation is verifiable.

Estimate: S/M — add a serialized field.

Evidence:
- Snapshot `ed08b6ef-079d-4775-8f61-7dc801053712`, job `job-20260724111822Z`, model `claude-opus-4-8`
- `10106-set-rotation-mcp`: 2/5 passed
- Failing runs `06697d4a-3297-404f-98cf-46ee8821b80c`, `c4bd0706-e84b-4c9e-86b0-7080ef4d183f`, `01afc19c-665e-4982-8621-a9ce93de6b3b`
