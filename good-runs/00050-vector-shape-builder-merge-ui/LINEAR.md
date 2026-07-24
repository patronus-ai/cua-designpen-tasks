# DesignPen [vector editing]: 'vector shape builder merge' fails QA — 3/5 runs report broken workflow (00050-vector-shape-builder-merge-ui)

Description:
Shape builder (M) clicks mark cells as filled internally (hover hatch flips from blue to pink) but apply no visible fill paint — the cells stay visually unfilled until a Fill color is manually added in the Design panel, so "click each cell so both are filled" does not happen as described. Two setup-path bugs compound this: the Shape builder only sees the edited vector's own geometry (a divider line drawn as a separate pen object produces no detectable regions), and using Flatten to merge two objects silently drops the stroke and yields geometry with no detectable regions. The sweep-merge across the divider itself works correctly once one vector network with two cells exists.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Press P (Pen tool) and draw a closed square: click 4 corners and close the path back at the first anchor (200×200 "Vector 1").
3. In the same vector, add a line straight across the square so it splits into two cells. Note: a line drawn as a separate pen object is not seen by Shape builder, and Flatten to combine objects drops the stroke and region data — instead, in one pen session insert midpoint nodes on the left/right edges and draw the chord between them.
4. In the vector-edit session, press M to activate the Shape builder subtool.
5. Click each of the two cells — observe the region state changes (hover hatch flips to pink) but no visible fill appears.
6. (Workaround to see fills: manually add a Fill color in the Design panel.)
7. With Shape builder active, drag a sweep from one filled cell across the divider into the other.

Actual Result:

- Shape builder clicks marked each cell as filled (hover hatch flipped to pink, confirming the region state), "However, the clicks produced **no visible fill** — the tool applies no paint of its own", requiring a manual Fill color in the Design panel before both cells actually rendered as filled.
- Drawing the divider as a separate pen object "didn't work for the Shape builder (it only sees the edited vector's own geometry)".
- Using Flatten to merge the two objects "silently dropped the stroke and produced geometry with no detectable regions".
- The sweep across the divider worked: the two cells merged into a single filled square and the divider line was removed.

Expected Result:
Clicking a cell with the Shape builder should render that region as visibly filled (applying a default fill paint) without requiring a manual Design-panel fill; Flatten should preserve stroke styling and produce region-detectable geometry.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 5 runs failed (2 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0f41cf22-64eb-47aa-99bf-0a35c39f9c0b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0f533cb0-4469-4cb7-bade-ee8e9e23bbba.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_15a2df92-a91e-4952-af5f-d91ef34b15cb.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7b58b6c8-4a28-43f4-a9a4-8ad225b86715.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f5f6558c-44ca-4a7e-bda9-e3f179d11793.txt`

Agent report (verbatim tail of failing run):

```
The final state is clean: a single 200×200 vector, gray fill, black stroke, out of edit mode — the two cells were merged into one by the sweep.

**Summary of what I did and found:**

1. **Closed square with Pen tool** ✓ — Clicked 4 corners and closed the path back at the first anchor (200×200 "Vector 1").

2. **Line straight across** ✓ — This took some discovery: drawing the line as a *separate* pen object didn't work for the Shape builder (it only sees the edited vector's own geometry), and using **Flatten** to merge the two objects silently dropped the stroke and produced geometry with no detectable regions. I deleted everything and redrew in one pen session: inserted midpoint nodes on the left/right edges, then drew the chord between them — giving one vector network properly split into two cells.

3. **Shape builder (M), click each cell** ⚠ — Activated via M in the vector-edit session. Hovering highlighted each cell individually (blue hatch), and clicking marked each cell as filled (hover hatch flipped to pink, confirming the region state). However, the clicks produced **no visible fill** — the tool applies no paint of its own, so I had to manually add a Fill color in the Design panel before both cells actually rendered as filled.

4. **Sweep across the divider** ✓ — With Shape builder active, dragged from the top filled cell across the divider into the bottom cell. The two cells merged into a single filled square and the divider line was removed — exactly the expected shape-builder merge behavior.

The end-to-end flow was completed, but it required workarounds: Shape-builder clicks alone left the cells visibly unfilled (no default fill paint is applied, so "click each cell so both are filled" doesn't happen as described without manually adding a fill), and the earlier Flatten path lost stroke styling and region data entirely.

verdict: not-approve
```
