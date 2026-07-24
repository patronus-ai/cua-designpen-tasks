# DesignPen [MCP / describe]: 'describe on document root' fails QA — 4/5 runs report broken workflow (10004-describe-mcp)

Description:
The MCP `describe` tool cannot be run against the document as a whole. Calling `describe` with the document root id `0:0` returns `Node "0:0" not found`, even though the `viewport_zoom_to_fit` tool's own documentation explicitly calls `0:0` the document root — an inconsistency between two tools over the same id. Calling `describe` with no id returns `Provide id (string) or ids (string[])`, and `find_nodes` surfaces no page/document container node to target, only the leaf shapes. As a result there is no working way to "describe the document" as the task instructs; agents had to fall back to describing the individual shape node ids. The rename/zoom/verify steps otherwise succeed, so the actionable defect is `describe` rejecting the document root id.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport); use only MCP tools.
2. `create_shape` a rectangle (default name) → `0:3`; `create_shape` an ellipse (default name) → `0:4`.
3. Call `describe` with id `"0:0"` (the document root per `viewport_zoom_to_fit` docs).
4. Also call `describe` with no id.
5. Call `find_nodes` and look for a document/page container node.

Actual Result:
- `describe("0:0")` → `Node "0:0" not found`.
- `describe` with no id → `Provide id (string) or ids (string[])`.
- `find_nodes` returns only the two shape nodes (`0:3`, `0:4`) — no page/document node exists to describe.
- The document-level describe step is impossible; agents worked around it by describing the child shape ids directly.

Expected Result:
`describe` should accept the document root id `0:0` (consistently with `viewport_zoom_to_fit`) and/or support a document-level describe (no id, or an exposed page/document node), so that "call describe on the document" can be carried out as documented.

Estimate: S (2 points) — reconcile the root-node id handling in `describe` with the rest of the MCP toolset.

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 4 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0324a199-9e3c-4966-9f2a-e5de646ad993.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c8ef0b1b-fe82-407a-bbb6-19e29f933453.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6aabb973-3153-4693-b6f8-1bd39846d20a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_57b54a44-1daa-4d3d-9a73-00fac8280380.txt`

Agent report (verbatim tail of failing run):

```
All steps are complete and verified. Here's my report of what I did and what I found.

## What I did
1. Created a rectangle with a default name → came in as "Rectangle 1" (id 0:3).
2. Created an ellipse with a default name → came in as "Ellipse 1" (id 0:4).
3. Attempted describe on the document, then renamed both shapes.
4. Renamed 0:3 → Rectangle and 0:4 → Ellipse.
5. Called viewport_zoom_to_fit (bounds x:100, y:100, 400×150; center 300,175).
6. Verified with find_nodes and describe.

## Verification result
- find_nodes confirms: 0:3 is now named exactly "Rectangle" (type RECTANGLE), and 0:4 is named exactly "Ellipse" (type ELLIPSE).
- describe confirms the same names/types. (Both shapes carry a cosmetic "no fill and no stroke — invisible" warning, which is expected since I created them with default styling and the task didn't ask for fills.)

## Problems I hit
1. describe on "the document" failed. Calling describe with the document root id "0:0" returned "Node \"0:0\" not found" — even though the viewport_zoom_to_fit documentation explicitly states "0:0" is the document root. This is an inconsistency between tools, and it blocked the literal instruction to "call describe on the document." I worked around it by calling describe on the shape node ids directly.
2. No rename_node tool exists. The task offered "rename_node or update_node," but only update_node is actually available. Not a blocker (update_node worked), but the mentioned tool is missing.
3. Casing mismatch. The task said describe reported the shape kind as 'Rectangle' / 'Ellipse', but describe actually reports the type field in uppercase ("RECTANGLE" / "ELLIPSE"). Title-case "Rectangle"/"Ellipse" only appeared inside the auto-generated default names. I renamed to Rectangle / Ellipse as the instruction explicitly directed.

The end state is correct (shapes named exactly Rectangle and Ellipse, zoomed to fit), but I did encounter a genuine tool bug/inconsistency: describe could not be run on the document root despite it being documented as valid.

verdict: not-approve
```
