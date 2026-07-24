# DesignPen [component instances]: 'instance switch variant' fails QA — 4/4 runs report broken workflow (00216-instance-switch-variant-ui)

Description:
After creating a component set (right-click > "Create component set") and placing an instance, the "Variants" section does not appear in the Design panel at all — not for the instance, the variant components, or the set — even after renaming variants to the `Size=Value` convention and recreating the instance fresh. The section only appears after a full page reload, which re-derives the variant properties. This stale-state bug blocks the intended flow of switching an instance's variant via the Variant section select; the switch itself works correctly once the section appears post-reload.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Draw a 120x40 rectangle, name it "Button", and convert it to a component (diamond icon in the Design panel).
3. Duplicate the component, select both, and use right-click > "Create component set" to build a set named "Button".
4. Rename the variants using the `Size=Small` / `Size=Large` convention; set the Large variant (frame + inner rectangle) to 220 wide, keeping Small at 120 wide.
5. Create an instance of the Small variant on the canvas via right-click > "Create instance".
6. Select the instance and look for the "Variants" section in the Design panel.

Actual Result:

- After creating the component set and placing the instance, the "Variants" section did not appear in the Design panel at all — not for the instance, the variant components, or the set — even after renaming variants to the `Size=Value` convention and recreating the instance fresh.
- The section only appeared after a full page reload, which re-derived the variant properties.
- After the reload workaround, switching the instance's "Size" from Small to Large via the Variant section select worked correctly (instance resized from 120 to 220 wide).

Expected Result:
The Variants section (with the "Size" select) should appear in the Design panel immediately after the component set is created and the instance is selected, without requiring a full page reload to re-derive variant properties.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2e2c8ba0-433b-46e6-9511-42377420c0b6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6fbf553b-30d8-44bb-89a2-5b936eff28a4.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_872b186a-6116-4e80-bb46-5ac71daa6519.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a804cb61-19c5-497e-8c55-8ede4fe1943e.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fc894717-d404-4b98-937a-e7fe0e6a5368.txt`

Agent report (verbatim tail of failing run):

```
The task is now complete. Final state verification:

- **Layers panel**: "Button" component set contains two variant components — "Size=Large" and "Size=Small"; the instance "Size=Large" (originally placed as Small) sits on the canvas as a separate top-level layer.
- **Canvas**: The component set frame "Button" holds the Small (120×40) and Large (220×40) variants; the instance at top is now 220×40.
- **Design panel**: The instance shows the "Variants" section with the "Size" select now reading "Large".

**Summary of what was done:**
1. Drew a 120×40 rectangle, named it "Button", and converted it to a component via the diamond icon in the Design panel.
2. Duplicated the component, selected both, and used right-click → "Create component set" to build the set named "Button".
3. Named the variants using the `Size=Small` / `Size=Large` convention and set the Large variant (frame + inner rectangle) to 220 wide, keeping Small at 120 wide.
4. Created an instance of the Small variant on the canvas via right-click → "Create instance".
5. Selected the instance and switched its "Size" from Small to Large using the Variant section select in the Design panel — the instance correctly resized from 120 to 220 wide.

**Problem encountered:** After creating the component set and placing the instance, the "Variants" section did not appear in the Design panel at all — not for the instance, the variant components, or the set — even after renaming variants to the `Size=Value` convention and recreating the instance fresh. The section only appeared after a full page reload, which re-derived the variant properties. This stale-state behavior was a genuine blocker in the intended flow and required a non-obvious workaround (reloading the app) before the variant switch could be performed. The switch itself then worked correctly.

verdict: not-approve
```
