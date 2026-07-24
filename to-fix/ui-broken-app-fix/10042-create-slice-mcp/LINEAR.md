# DesignPen [MCP create_slice]: 'create slice via MCP' fails QA — 5/5 runs report broken workflow (10042-create-slice-mcp)

Description:
The MCP `create_slice` tool does not create a SLICE node. Calling `create_slice` with name "Hero cut" covering (0,0) to 300x200 returns a node whose name, position, and size are correct, but whose type is FRAME instead of SLICE — verified independently via `get_node` and `find_nodes` in two separate runs. The core purpose of the tool (creating an export slice) is therefore not fulfilled; it silently produces a plain frame. The remaining three runs of this job could not even reach the bug because the MCP bridge reported "OpenPencil app is not connected" on the first call (separate infra issue), so on every run where the tool actually executed, it produced the wrong node type.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport) so the OpenPencil SPA is live and connected to the MCP server.
2. Via MCP, call `create_slice` with name 'Hero cut', position (0,0), width 300, height 200.
3. Call `viewport_zoom_to_fit`.
4. Call `get_node` (or `find_nodes`) on the returned node id and inspect its `type`.

Actual Result:

- The returned node (e.g., `0:3`) has name "Hero cut", x 0, y 0, width 300, height 200 — all correct — but `type` is **FRAME**, not SLICE.
- `viewport_zoom_to_fit` centers on (150,100) with bounds {x:0, y:0, w:300, h:200}, confirming the geometry; only the node type is wrong.

Expected Result:
`create_slice` should create a node of type SLICE with the given name and bounds, so the object behaves as an export slice rather than a regular frame.

Estimate: S (2 points) — the MCP handler creates the node with the wrong node type; likely a one-line type mapping fix in the create_slice implementation

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 5 of 5 runs failed (2 on the FRAME-instead-of-SLICE bug; 3 blocked earlier by "OpenPencil app is not connected" infra errors)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ffd451a9-da4f-4fa7-88d2-b8002c2378df.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7b20c0c8-2a97-4c09-a7d9-bccaf55c7002.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_51b8c50c-af41-4447-ae99-4ab25385ed67.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2103ff9b-a839-4dfc-b746-c88d1ed5bd11.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_861f37c9-d089-40d5-8b27-fdbbddf0b8f6.txt`

Agent report (verbatim tail of failing run):

```
1. **`create_slice`** — name 'Hero cut', position (0,0), size 300×200 → returned node `0:3`.
2. **`viewport_zoom_to_fit`** → centered on (150,100) with bounds x:0, y:0, w:300, h:200 (correctly framing the new node).
3. **Verification** via `get_node` and `find_nodes`.

**Verification results:**
| Property | Expected | Actual | Match |
|----------|----------|--------|-------|
| Name | Hero cut | Hero cut | ✅ |
| X / Y | 0 / 0 | 0 / 0 | ✅ |
| Width | 300 | 300 | ✅ |
| Height | 200 | 200 | ✅ |
| **Type** | **SLICE** | **FRAME** | ❌ |

The geometry and zoom worked fine, but the core requirement — creating a *slice* — was not fulfilled because the tool created a frame instead.

verdict: not-approve
```
