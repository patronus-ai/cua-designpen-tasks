# DesignPen [MCP tools]: 'get jsx' fails QA — 5/5 runs report broken workflow (10007-get-jsx-mcp)

Description:
The get_jsx MCP workflow in DesignPen/OpenPencil structurally works (frame, child rectangle, get_jsx output, text layer with the JSX, zoom, verification all succeed), but two toolset defects break the task. First, there is no way to set a fill color via MCP: `create_shape` accepts only type/position/size/name/parent and no style/update tool exists, so the "green rectangle" requirement is impossible — `get_node` and `get_jsx` confirm the rectangle has no fill. Second, when creating a child with `parent_id`, `create_shape` interprets x/y as absolute canvas coordinates rather than parent-relative, so a child intended for a frame at (100,100) lands at (-50,-50) inside it, partially clipped by the frame's `overflow="hidden"`, with no move or delete tool available to correct it.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools only, call create_shape to create a frame named Card (e.g. at (100,100), 300x200).
3. Call create_shape with the Card frame's id as parent_id to create a rectangle intended to be green (note: no fill-color parameter or style tool is available).
4. Call get_jsx on the Card frame.
5. Create a text layer named Code and set its content to the returned JSX.
6. Call viewport_zoom_to_fit.
7. Verify with find_nodes and get_node — inspect the rectangle's fill and its position inside the frame.

Actual Result:

- The rectangle cannot be made green: the MCP toolset has no way to set a fill color (`create_shape` accepts only type/position/size/name/parent; no style/update tool exists). `get_node` and `get_jsx` both confirm the rectangle has no fill applied — it could only be named "Green Rect".
- Coordinate quirk: with `parent_id`, `create_shape` interpreted x/y as absolute canvas coordinates rather than parent-relative, so the rectangle landed at (-50, -50) inside the frame — partially clipped by the frame's `overflow="hidden"` — and no move or delete tool exists to correct it without leaving duplicate stray nodes.
- Everything else worked: frame "Card" (0:3) created, get_jsx returned valid JSX, text layer "Code" (0:5) matches the JSX character for character, viewport_zoom_to_fit succeeded.

Expected Result:
The MCP toolset should allow creating an actually green rectangle (a fill-color capability on create or via an update/style tool), and `create_shape` with `parent_id` should place the child at parent-relative coordinates (or the behavior should be correctable via move/delete tools), so the get_jsx workflow can produce a correctly styled and positioned Card frame.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_727a4ab0-e6ad-45a7-bed8-3957900609ac.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_865587f1-1825-4464-979c-446a61a1b604.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e7987781-5232-40af-9c18-fee5e653cc3d.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e7cf9b7d-5860-4fd8-be51-f119ae48d761.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f199752a-a403-48d3-8e11-d4b54a79b5fe.txt`

Agent report (verbatim tail of failing run):

```
Verification complete. Here's my report:

---

## Report

**What was created and verified:**

1. ✅ **Frame "Card"** (`0:3`) — exists at (100, 100), 300×200. Confirmed via `find_nodes` (exactly 1 match) and `get_node`.
2. ⚠️ **Rectangle "Green Rect"** (`0:4`) — confirmed as a child of the Card frame via `get_node` on the frame. **However, it is not actually green** (see problems below).
3. ✅ **`get_jsx` on Card** returned:
   ```jsx
   <Frame name="Card" x={100} y={100} w={300} h={200} overflow="hidden">
     <Rectangle name="Green Rect" x={-50} y={-50} w={200} h={100} />
   </Frame>
   ```
4. ✅ **Text layer "Code"** (`0:5`) — created and verified via `find_nodes` and `get_node`; its `characters` property matches the returned JSX exactly, character for character.
5. ✅ **`viewport_zoom_to_fit`** succeeded — viewport centered at (535, 200) over bounds covering both the Card frame and the Code text layer.

**Problems encountered:**

1. **Cannot make the rectangle green (blocker):** The available MCP toolset has no way to set a fill color. `create_shape` accepts only type/position/size/name/parent, and there is no style/update tool. `get_node` and `get_jsx` both confirm the rectangle has no fill applied — I could only name it "Green Rect", not actually color it green. The explicit "green rectangle" requirement could not be fulfilled.
2. **Coordinate quirk:** When creating a child with `parent_id`, `create_shape` interpreted x/y as absolute canvas coordinates rather than parent-relative, so the rectangle landed at (-50, -50) inside the frame — partially clipped by the frame's `overflow="hidden"`. With no move or delete tool available, this could not be corrected without leaving duplicate stray nodes.

The structural workflow (frame → child rectangle → get_jsx → text layer with JSX → zoom → verify) completed successfully, but the rectangle is not green due to missing fill-color capability in the tools, and its placement inside the frame is offset due to the absolute-coordinate behavior.

verdict: not-approve
```
