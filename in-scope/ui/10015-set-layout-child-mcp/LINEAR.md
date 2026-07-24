# DesignPen [MCP tools]: 'set layout child' fails QA — 5/5 runs report broken workflow (10015-set-layout-child-mcp)

Description:
Combining `set_layout` and `set_layout_child` via the DesignPen/OpenPencil MCP tools collapses the frame geometry. Applying auto-layout via `set_layout` (HORIZONTAL, padding 0, spacing 0) resets a 300x100 frame to hug-contents sizing, discarding its explicit size (it hugs to the 50x50 child). Then calling `set_layout_child` with `sizing_horizontal: FILL` on the child inside a hug-width parent creates a circular dependency that collapses the width to 0 — both the frame and the rectangle end up 0x50. Every individual tool call reports success, and the toolset has no resize operation to restore the frame, so the intended layout (a 300x100 row with the child stretched to full width) is unreachable.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools only, call create_shape to create a 300x100 frame named Row at (0,0).
3. Call set_layout on the Row frame with direction HORIZONTAL, padding 0, spacing 0.
4. Call create_shape to create a 50x50 rectangle named Stretch inside the Row frame.
5. Call set_layout_child on Stretch with sizing_horizontal FILL.
6. Call viewport_zoom_to_fit on the Row frame and verify with get_node.

Actual Result:

- All tool calls report success (`set_layout_child` reports `layoutSizingHorizontal` updated), but `viewport_zoom_to_fit` returns bounds `width: 0, height: 50`.
- `get_node` shows frame "Row" (0:3) with correct auto-layout settings (`layoutMode: HORIZONTAL`, `itemSpacing: 0`) but dimensions 0x50 instead of 300x100.
- Rectangle "Stretch" (0:4) is 0x50 instead of 50x50 (or the expected 300x50 after FILL).
- Cause chain: `set_layout` reset the frame to hug-contents sizing (discarding the explicit 300x100), then child FILL inside a hug-width parent created a circular dependency collapsing width to 0; no resize tool exists to restore the frame.

Expected Result:
Applying auto-layout should preserve the frame's explicit 300x100 size (or a resize tool should exist to restore it), and setting the child's sizing_horizontal to FILL should stretch the rectangle to the frame's full width, yielding a 300x100 row containing a 300x50 (full-width) rectangle.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2b603577-16b8-413e-b515-9ea0f4164979.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4c475354-ca4b-45b1-841c-af54a506baca.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7100458c-4142-4457-a36d-60812525f167.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_744f7519-8d4f-4a51-845b-2babcb82d1bb.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d7dafbac-9fef-4de6-af8d-96d7475fb409.txt`

Agent report (verbatim tail of failing run):

```
All requested operations were executed, and verification is complete. Here is my report:

## Report

**Actions performed (all via MCP tools):**
1. ✅ `create_shape` — FRAME "Row" at (0,0), 300×100 → created as `0:3`
2. ✅ `set_layout` — direction HORIZONTAL, padding 0, spacing 0 on `0:3` → succeeded
3. ✅ `create_shape` — RECTANGLE "Stretch" 50×50 inside `0:3` → created as `0:4`
4. ✅ `set_layout_child` — `sizing_horizontal: FILL` on `0:4` → reported `layoutSizingHorizontal` updated
5. ✅ `viewport_zoom_to_fit` on `0:3` → succeeded, but returned bounds `width: 0, height: 50`

**Verification findings (`get_node`):**
- Frame "Row" (`0:3`): `layoutMode: HORIZONTAL`, `itemSpacing: 0`, at (0,0) — the auto-layout settings are correct.
- **However, the frame's dimensions are now 0×50 instead of 300×100.**
- Rectangle "Stretch" (`0:4`): dimensions are **0×50 instead of 50×50** (or the expected 300×50 after FILL).

**What went wrong:** Applying auto-layout via `set_layout` appears to have reset the frame to hug-contents sizing, discarding its explicit 300×100 size (it hugged to the 50×50 child). Then setting the child to `sizing_horizontal: FILL` inside a hug-width parent created a circular dependency that collapsed the width to 0 — leaving both the frame and rectangle at 0×50. The available MCP toolset has no resize operation, so I could not restore the frame to 300×100 to achieve the intended result (a 300×100 row with the rectangle stretched to full width).

All tool calls succeeded individually, but the final canvas state does not match the intended layout: the frame collapsed to 0×50 due to the hug/FILL interaction, and there is no tool available to fix the dimensions.

verdict: not-approve
```
