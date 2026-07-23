# DesignPen [boolean operations]: 'boolean subtract' fails QA — 4/5 runs report broken workflow (00121-boolean-subtract-ui)

Description:
Main menu > Object > Subtract selection subtracts in the inverted direction. With the natural draw order (big rectangle first, small on top — layers show Rectangle 2 above Rectangle 1), the operation kept the small rectangle and subtracted the big one (small − big), leaving only an L-shaped sliver, instead of the conventional Penpot/Figma behavior of subtracting the upper shape from the bottom shape (big − small). The correct result was only reachable by undoing and re-selecting in the opposite order. Additionally, undoing the subtract restored the two rectangles with their z-order swapped in the Layers panel (Rectangle 1 above Rectangle 2), an undo-fidelity inconsistency.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a large rectangle of about 300x200 with the rectangle tool.
3. Draw a smaller ~100x100 rectangle partly overlapping the big one (e.g. overlapping its bottom-right corner), so layers show Rectangle 2 above Rectangle 1.
4. Select both shapes (click one, shift-click the other).
5. Apply Main menu > Object > Subtract selection.
6. To see the undo bug: press undo after the subtract and inspect the Layers panel z-order.

Actual Result:

- The subtract is inverted: with the natural draw order (big first, small on top), "Subtract selection" kept the small rectangle and subtracted the big one (small − big), leaving only an L-shaped sliver of the small rect instead of the big rectangle with the overlap carved out.
- The expected result (small carved out of big) required a workaround: undo, then re-select in the opposite order (big first, then shift-click small).
- Undo restored the two rectangles with their z-order swapped in the Layers panel (Rectangle 1 ended up above Rectangle 2).

Expected Result:
Subtract selection should follow the conventional Penpot/Figma semantics — subtract the upper shape from the bottom shape (big − small) regardless of selection order — and undo should restore the original layer z-order exactly.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 5 runs failed (1 approved)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4432f02a-3ad6-4a28-9370-179c483961ec.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5237e55e-1c8c-4828-8ee4-a37a354fed07.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7f59a1ae-43c4-4fff-abb8-5697feb741e7.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d2cf96fb-0e22-44dd-be21-42069410f072.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f098d435-a5c3-4232-8fa9-70cb87b7ed6e.txt`

Agent report (verbatim tail of failing run):

```
The task is complete. Here's a summary of what happened:

**Steps performed:**
1. Drew a large rectangle of exactly 300×200 at (154, 150) using the rectangle tool.
2. Drew a smaller 100×100 rectangle at (404, 300), partly overlapping the big one's bottom-right corner (50×50 overlap).
3. Selected both shapes (shift-click) and applied **Main menu > Object > Subtract selection**.
4. Final result: a "Subtract" boolean group containing both rectangles, rendering the big rectangle with the small rectangle's overlapping region carved out — as requested.

**Problem encountered:** The first Subtract attempt produced the *inverted* result. With the natural draw order (big first, small on top — layers showed Rectangle 2 above Rectangle 1), "Subtract selection" kept the small rectangle and subtracted the big one (small − big), leaving only an L-shaped sliver of the small rect, instead of the conventional Penpot/Figma behavior of subtracting the upper shape from the bottom shape (big − small). I had to undo and re-select in the opposite order (big first, then shift-click small) to get the correct "small carved out of big" result. Additionally, the undo restored the two rectangles with their z-order swapped in the Layers panel (Rectangle 1 ended up above Rectangle 2), which is an undo-fidelity inconsistency.

The intended end state was ultimately achieved, but only via a workaround for the inverted subtract direction, and the undo z-order swap is a genuine anomaly.

verdict: not-approve
```
