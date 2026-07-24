# DesignPen [pen tool]: 'branch a new chain from an existing vertex' fails QA — 5/5 runs report broken workflow (00063-pen-chain-from-vertex-ui)

Description:
The Pen tool cannot branch a new chain from a vertex that has become an interior/shared node of the path. Starting a chain from an open endpoint works, but once a vertex is shared by two subpaths, pen-clicking it again does not begin a new chain. Instead the click grabs the node and converts it to a smooth point — spawning Bézier control handles and curving the already-drawn segment — and the follow-up click drops a disconnected floating point rather than joining the arm to the junction. This was reproduced consistently across all runs (including with guaranteed zero-movement press/release, ruling out an accidental drag), so it is a genuine tool behavior bug, not a mis-click.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Select the Pen tool (P).
3. Draw the stem: click (300,500), then click (300,350). Press Escape once to break the chain while staying in the vector edit session.
4. Pen-click the top stem vertex (300,350) to branch a new chain, then click (240,250) to draw the first arm. (This works — (300,350) is still an open endpoint.)
5. Press Escape to break the chain again.
6. Pen-click (300,350) once more to branch the second arm, then click (360,250).

Actual Result:

- Steps 1–5 succeed: stem drawn, chain broken, first arm branched cleanly.
- At step 6, pen-clicking the now-interior junction (300,350) does NOT start a new chain. It converts the node to a smooth point, adding Bézier handles and curving the existing first arm (bounding-box width jumped from 60 to ~63.6). The subsequent click at (360,250) starts a disconnected subpath instead of connecting to the junction.
- The only way to produce the intended straight second arm was a workaround: draw the arm in reverse, clicking (360,250) first and snapping back onto (300,350).

Expected Result:
Pen-clicking an existing vertex — whether an open endpoint or an interior/shared node — should branch a new chain from that vertex, allowing a straight segment to be drawn out from it, matching the branch behavior that already works for the first arm.

Estimate: M (3 points) — pen-tool hit-testing/branch logic must distinguish "branch from existing node" from "edit node to smooth"; scoped to one interaction in the vector editor.

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_55bc7939-1d50-441b-9b4e-02f44a6a543d.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_18358ec6-131a-4346-ba3c-a3bc26b5aedb.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4959d844-db78-4d8e-b25c-19e98b95bd25.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e08258a9-f793-42ce-8429-24fba40c9e41.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_82304022-94c0-43d2-9f71-1732506fc97c.txt`

Agent report (verbatim tail of failing run):

```
The final Y-shape is clean and correct — stem descending from the junction, two straight arms reaching the top corners, clean junction, bounding box 120 × 250. The path is committed as a single "Vector 1" object.

## Summary

I completed the Y-shaped path, and the final geometry is exactly correct (vertices at (300,500), (300,350), (240,250), (360,250); bounding box X:240, Y:250, W:120, H:250). However, the task did **not** go entirely smoothly — I hit a real problem with the described workflow:

**What worked:**
- Pen tool activated, stem drawn from (300,500)→(300,350), Escape broke the chain while staying in the edit session.
- Pen-clicking the top vertex (300,350) to branch the **first** arm to (240,250) worked cleanly (the vertex was an open endpoint at that moment).

**What went wrong:**
- The second branch step — "pen-click (300,350) once more, and draw the second arm" — did **not** behave as described. By that point the vertex had become an interior junction node (stem + first arm), and pen-clicking it did not start a new chain. Instead it converted the node to a smooth point, adding bezier control handles and **curving the existing first arm**. This was reproducible: it happened with a normal click *and* with a zero-movement mouse press/release, and it was not a precision issue (I clicked the exact junction center, verified by zoom). Each time, I had to undo.
- I worked around it by drawing the second arm as a separate chain in reverse — clicking the far endpoint (360,250) on empty canvas first, then clicking back onto the vertex (300,350), which connected cleanly with no handles. This produced the identical, correct Y geometry, and I committed it.

So while the end result is a correct, clean Y-shaped path, the specific instructed interaction (re-clicking the shared vertex to branch the second arm) is effectively blocked in this tool — clicking an interior/junction node edits it rather than branching from it — which required a non-obvious workaround.

verdict: not-approve
```
