# DesignPen [MCP boolean ops]: 'boolean_subtract result geometry' fails QA — 4/5 runs report broken workflow (10033-boolean-subtract-mcp)

Description:
The MCP `boolean_subtract` tool creates a `BOOLEAN_OPERATION` node with the correct type, name and child order, but the resulting geometry/bounds are wrong: they equal the UNION of the operands instead of the subtraction. With Rect A 100x100 at (0,0) and Rect B 100x100 at (50,50), A−B is an L-shape fully contained in A, so the result's bounding box must be 100x100 at (0,0). Instead the node reports width 150 x height 150 at (0,0) — exactly the union bounding box — meaning the part of B that protrudes beyond A (the [100,150] corner) was not discarded by the cut. `viewport_zoom_to_fit` independently confirms the oversized 150x150 extent, so this is not a read glitch. All four failing runs reproduced the identical 150x150-instead-of-100x100 result.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport) with the MCP server connected.
2. Call `create_shape` for a 100x100 rectangle "Rect A" at (0,0).
3. Call `create_shape` for a 100x100 rectangle "Rect B" at (50,50).
4. Call `boolean_subtract` with ["<Rect A id>", "<Rect B id>"].
5. Call `get_node` on the resulting BOOLEAN_OPERATION node and inspect its width/height; call `viewport_zoom_to_fit` and inspect the reported bounds.

Actual Result:

- The BOOLEAN_OPERATION node reports x 0, y 0, width 150, height 150 — the union bounding box of the two inputs.
- `viewport_zoom_to_fit` agrees: bounds (0,0)→(150,150), center (75,75).
- The protruding portion of the subtracted rectangle contributes to the result's extent, so the subtract behaves like a union/group as far as bounds and rendering extent go.

Expected Result:
A−B should yield an L-shape bounded by Rect A: the result node's bounding box should be 100x100 at (0,0), and zoom-to-fit should frame those bounds.

Estimate: M (3 points) — boolean result bounds computed as union of operands instead of evaluating the subtract geometry; scoped to the boolean-operation bounds/render path

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 4 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9b240bff-910a-40d2-b887-c997e4a1d6ac.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_65851f9d-04b3-45c2-bc5d-eaf377dcedf7.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_3f6414d3-416f-4b50-893c-8074c6b4ca03.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_772c2b8f-d5d0-4d3f-ab58-f0cf6d176d56.txt`

Agent report (verbatim tail of failing run):

```
## Summary of actions

1. **Created Rect A** (`0:3`): a 100×100 rectangle at (0,0). ✅
2. **Created Rect B** (`0:4`): a 100×100 rectangle at (50,50), offset by 50px on both axes so it overlaps Rect A in the (50,50)–(100,100) region. ✅
3. **Called `boolean_subtract(["0:3","0:4"])`** → created node `0:5`, a `BOOLEAN_OPERATION` named "Boolean subtract". ✅
4. **Called `viewport_zoom_to_fit`** → centered at (75,75), bounds (0,0)→(150,150). ✅
5. **Verified** node `0:5` with `get_node`.

## Verification finding (problem)

The subtraction result is **geometrically wrong**. The boolean node reports:

- `x: 0, y: 0, width: 150, height: 150`

For a correct subtraction of Rect B out of Rect A, the result is an L-shape that can never extend beyond the base shape (Rect A). The expected bounding box is therefore **100×100** at (0,0).

Instead the node's bounds are **150×150** — which is exactly the *union* of the two rectangles' bounding boxes (Rect A [0–100] ∪ Rect B [50–150] = [0–150] on each axis). That means the portion of Rect B sticking out beyond Rect A (the [100–150]×[100–150] corner) was **not** discarded by the cut. The operation behaved like a grouping/union of the operands' bounds rather than a true subtract, so the second rectangle was not actually cut out of the first.

The operands are preserved as editable children (normal for Figma), so the tell-tale sign is the parent bounding box, which is inconsistent with a real subtract.

Everything else (shape creation, the boolean node getting created, and zoom-to-fit) worked, but the core boolean_subtract produced an incorrect result.

verdict: not-approve
```
