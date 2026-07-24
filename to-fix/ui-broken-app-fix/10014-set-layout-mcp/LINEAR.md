# DesignPen [MCP auto-layout]: 'set_layout child reflow' fails QA — 5/5 runs report broken workflow (10014-set-layout-mcp)

Description:
The MCP `set_layout` tool applies frame-level auto-layout properties but does not reflow the frame's children. After creating a 400x80 frame "Toolbar" with three 40x40 child rectangles and calling `set_layout` with direction HORIZONTAL, spacing 16 and padding 12, `get_node` confirms `layoutMode: HORIZONTAL` and `itemSpacing: 16` on the frame — but only the first child is repositioned (to the 12,12 padding offset). Btn 2 and Btn 3 remain stacked at (0,0), overlapping each other and the frame corner, instead of flowing horizontally at x=68 and x=124. Re-applying `set_layout` changes nothing, so this is a persistent reflow bug, not a transient state. Secondary issues: `set_layout`'s response only echoes `{"id","spacing"}` and never confirms the direction or padding it was asked to set, and `get_node` exposes no padding fields, so padding cannot be verified directly. (2 of the 5 failing runs never reached this point — they were blocked by a separate "OpenPencil app is not connected" MCP error on the first call; the reflow bug reproduced in all 3 runs that got through.)

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport) with the MCP server connected.
2. Call `create_shape` with type FRAME, name "Toolbar", x 0, y 0, width 400, height 80.
3. Call `create_shape` three times to add 40x40 child rectangles "Btn 1", "Btn 2", "Btn 3" parented to the Toolbar.
4. Call `set_layout` on the Toolbar's id with direction HORIZONTAL, spacing 16, padding 12.
5. Call `get_node` on the frame and each child and inspect the child coordinates.

Actual Result:

- Frame reports `layoutMode: HORIZONTAL` and `itemSpacing: 16`, but child positions are: Btn 1 (12,12), Btn 2 (0,0), Btn 3 (0,0) — only the first child was placed; the others overlap at the origin.
- Re-applying `set_layout` yields the identical wrong result.
- `set_layout`'s return value only echoes `{"id":"0:3","spacing":16}` — direction and padding are never confirmed, and `get_node` exposes no padding fields.

Expected Result:
`set_layout` with direction HORIZONTAL, spacing 16, padding 12 should reposition all three children into a horizontal row at (12,12), (68,12) and (124,12), and the tool response / node model should reflect the direction and padding that were set.

Estimate: M (3 points) — auto-layout reflow loop only processes the first child; plus response/model gaps for direction and padding

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5e1ae15c-d82c-4ed2-a98d-6bbf98f97d3d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bf42974b-d0ca-4712-a07d-e5fafd7ec153.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b8407756-4331-41cf-b1db-6fb9e250ea70.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0cdb7bec-f326-4274-aa7e-c4cc31bbebab.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_24f6c68f-96d4-4ac0-97c9-68ba88c29999.txt`

Agent report (verbatim tail of failing run):

```
## Actions performed
1. **Created the Toolbar frame** — `FRAME` named "Toolbar" at (0,0), 400×80 → id `0:3` ✅
2. **Created three child rectangles** inside it — "Btn 1" (`0:4`), "Btn 2" (`0:5`), "Btn 3" (`0:6`), each 40×40 ✅
3. **Called `set_layout`** on `0:3` with direction HORIZONTAL, spacing 16, padding 12
4. **Called `viewport_zoom_to_fit`** — it reported bounds `{0,0,400,80}`, centered at (200,40) ✅
5. **Verified** with `get_node` on the frame and each child.

## What verification revealed
The frame-level settings applied correctly:
- `layoutMode: HORIZONTAL` ✅
- `itemSpacing: 16` ✅
- Frame geometry/name correct ✅

**But the children were not laid out correctly.** For a horizontal auto-layout with padding 12 / spacing 16, the three buttons should sit at x = 12, 68, 124 (all y = 12). Instead:

| Button | Expected (x,y) | Actual (x,y) |
|--------|----------------|--------------|
| Btn 1  | (12, 12)       | (12, 12) ✅ |
| Btn 2  | (68, 12)       | **(0, 0)** ❌ |
| Btn 3  | (124, 12)      | **(0, 0)** ❌ |

Only the first child was repositioned to the padding offset; Btn 2 and Btn 3 remained stacked at (0,0), overlapping each other and the frame corner. I re-applied `set_layout` to rule out a transient glitch, but the result was identical. Additionally, the `set_layout` response only echoed `{"id":"0:3","spacing":16}` (never confirming direction or padding), and `get_node` never reports any padding fields, so padding couldn't be independently confirmed.

## Conclusion
The structure was created as specified, but the auto-layout engine did not reflow the children — the flexbox spacing/positioning only affected the first item, leaving the other two overlapping at the origin. This is a functional bug in the `set_layout` behavior, so the final visual result does not match a correct horizontal toolbar.

verdict: not-approve
```
