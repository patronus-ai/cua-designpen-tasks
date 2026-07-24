# DesignPen [boolean ops / MCP]: 'boolean_intersect' fails QA — 5/5 runs report broken workflow (10032-boolean-intersect-mcp)

Description:
`boolean_intersect` creates a BOOLEAN_OPERATION node and nests both source rectangles as children, but the resulting node's geometry is that of a UNION, not an intersection. Intersecting two 100×100 rectangles offset by (50,50) should produce the 50×50 overlap region; instead the boolean node reports 150×150 bounds — the union extent of the two inputs. A 150×150 bounding box is mathematically impossible for an intersection of two 100×100 shapes (which can be at most 100×100), so the intersect geometry is not being computed at all — the node behaves like a group/union wrapper. Reproduced across multiple runs; corroborated by both `get_node` and `viewport_zoom_to_fit` reporting the 150×150 extent. (Note: two of the five failing runs were instead blocked by a transient "OpenPencil app is not connected" error at the first create call; the dominant, actionable defect is the incorrect intersect geometry seen in the runs that got past connection.)

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport) with MCP tools available.
2. `create_shape` a 100×100 RECTANGLE at (0,0) → Rect A.
3. `create_shape` a 100×100 RECTANGLE at (50,50) → Rect B (offset +50 on both axes; overlaps A in (50,50)→(100,100)).
4. `boolean_intersect` with both ids.
5. `viewport_zoom_to_fit`, then `get_node` on the resulting boolean node to inspect its bounds.

Actual Result:

- A BOOLEAN_OPERATION node ("Boolean intersect") is created with both rectangles nested as children.
- The node reports `x:0, y:0, width:150, height:150` — the union bounding box of the two inputs.
- `viewport_zoom_to_fit` confirms 150×150 content extent.
- No 50×50 overlap geometry is produced.

Expected Result:
`boolean_intersect` should compute the true overlap: a result whose geometry/bounds are the 50×50 intersection region at (50,50)→(100,100), not the 150×150 union extent.

Estimate: M (3 points) — boolean intersection geometry computation is broken (produces union bounds); scoped to the boolean-operation path in the MCP/app engine.

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7cfc26b4-8334-4eb8-8f68-d47ee5c4c60d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_28da516a-a136-4c24-befe-d69a567c46c4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_98a3a091-37bc-4612-8121-5036dc49247b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_03a21872-1387-4fe8-b250-3ee1ab251c56.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_08037bdf-b5d7-4c86-a0cd-cb6bcd97c704.txt`

Agent report (verbatim tail of failing run):

```
I've completed all the requested steps and verified the result. Here's what I found.

## Actions performed
1. **Created Rect A** — 100×100 at (0,0) → ID `0:3`
2. **Created Rect B** — 100×100 at (50,50), offset +50px on both axes → ID `0:4`
3. **boolean_intersect** on `["0:3","0:4"]` → returned a `BOOLEAN_OPERATION` node named "Boolean intersect", ID `0:5`
4. **viewport_zoom_to_fit** → returned center (75,75), bounds {x:0, y:0, w:150, h:150}

## Verification findings
- `get_node 0:5`: a `BOOLEAN_OPERATION` node containing both rectangles as children (Rect A at 0,0,100×100 and Rect B at 50,50,100×100). Good structure.
- The page tree confirms a single top-level `BOOLEAN_OPERATION` on Page 1, with the two rectangles nested inside it (no stray leftover shapes).

**However, there's a problem with the geometry of the result.** The boolean node reports `x:0, y:0, width:150, height:150`. That is the **union** bounding box of the two inputs. A correct *intersection* of a rect at (0,0)–(100,100) with a rect at (50,50)–(150,150) should produce only the overlapping 50×50 region, i.e. bounds `x:50, y:50, width:50, height:50`.

A 150×150 bounding box is what you'd expect from a UNION/EXCLUDE, not an INTERSECT. So while the node is correctly *typed/labeled* as an intersect and holds both children, its resulting bounds do not reflect the actual intersected geometry — the operation did not tighten to the overlap region. The `viewport_zoom_to_fit` result (150×150) corroborates this.

Because the intersection result's geometry is incorrect (150×150 union bounds instead of the expected 50×50 overlap), the task did not go entirely smoothly.

verdict: not-approve
```
