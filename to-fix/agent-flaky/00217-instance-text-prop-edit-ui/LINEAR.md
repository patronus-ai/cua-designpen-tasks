# DesignPen [component instances]: 'instance text prop edit' fails QA — 4/4 runs report broken workflow (00217-instance-text-prop-edit-ui)

Description:
The workflow requires exposing a component's text label as a TEXT component property and editing it via a Design panel "Properties" section — but this OpenPencil build has no such feature. An exhaustive search (Design panel sections for the main component/instance/text layers, all context and "..." More-actions menus, the main menu, the Code/Inspect tab, the Assets panel, the Variables modal, and an accessibility-tree search) found no "Properties" heading or "Add property" control anywhere. The instance label could only be changed as a direct text override (double-click into the instance text and retype). Additionally, a mid-task navigation glitch sent the tab to `about:blank`, and reloading restored an older "snapshot" state that wiped the originally built component and instance, forcing a rebuild from scratch.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Build a small button component: a 120x40 rounded rectangle plus a text label "Click me"; convert to a main component via Create component (Ctrl+Alt+K).
3. Attempt to expose the label as a TEXT component property with default value "Click me" — search the Design panel for a "Properties" section or "Add property" control.
4. Place an instance via the component's "..." menu > "Create instance" and select it.
5. Attempt to change the text property to "Buy now" via the Design panel Properties section.

Actual Result:

- The label could not be exposed as a TEXT component property: the app has no "Properties" section (Design panel sections are only Position, Layout, Dimensions, Appearance, Typography, Fill, Stroke, Effects, Export, etc.), and no property feature exists in any context menu, "..." More-actions menu, the main menu (File/Edit/Object/Text/Preferences/Libraries), the Code/Inspect tab, the Assets panel, or the Variables modal; an accessibility-tree search confirmed no "Properties" heading or "Add property" control exists anywhere.
- The instance label was changed to "Buy now" only as a direct text override (double-click into the instance text and retype), not via any Properties UI.
- A mid-task navigation glitch sent the tab to `about:blank`; reloading the app restored an older "snapshot" state, wiping the originally built component and instance, which had to be rebuilt from scratch.
- Minor UI trap: the chevron button in the COMPONENT panel header silently toggles "ready for dev" status, and the right panel occasionally shifts horizontally, clipping its tabs.

Expected Result:
The Design panel should offer a Properties section where a component's text label can be exposed as a TEXT property with a default value, and instances should expose that property as an editable field that overrides the label text. The app should not crash to `about:blank` mid-task or lose work to a stale snapshot on reload.

Estimate: L (5 points) — state/undo consistency issue, needs investigation across the edit pipeline

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 4 of 4 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_441427ae-2188-4032-8254-83fdb5d9411c.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_54712e22-f90a-45b3-a022-04f6edee3d35.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_7269e720-a721-4b66-a0c0-c2c064ee8421.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_80bc246b-21ef-4b33-aee2-f51f6429cd10.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_d1b3cba9-f6a0-4f44-a022-1dcb9a8328c5.txt`

Agent report (verbatim tail of failing run):

```
The final state is confirmed. The Layers panel shows the main component (◆ Component) and the instance (◇ Component, selected). On canvas, the main component reads "Click me" and the instance reads "Buy now" with the INSTANCE panel active on the right.

**Summary of what was accomplished:**
1. ✅ Built a small button component (120×40 rounded rectangle + text label "Click me"), converted to a main component via Create component (Ctrl+Alt+K)
2. ❌ **Could not expose the label as a TEXT component property** — this app (OpenPencil) has no such feature. I exhaustively searched: the Design panel for the main component, instance, and text layers contains no "Properties" section (only Position, Layout, Dimensions, Appearance, Typography, Fill, Stroke, Effects, Export, etc.); all context menus, the "..." More-actions menus, the main menu (File/Edit/Object/Text/Preferences/Libraries), the Code/Inspect tab, Assets panel, and the Variables modal offer nothing for component text properties. An accessibility-tree search confirmed no "Properties" heading or "Add property" control exists anywhere.
3. ✅ Placed an instance (via component "..." → Create instance) and selected it
4. ⚠️ Changed the instance label to "Buy now" — but only as a **direct text override** (double-click into the instance text and retype), not via a Design-panel Properties section, since that UI does not exist.

**Problems encountered:**
- The core task requirement (TEXT component property with default "Click me", edited via a "Properties section") is impossible in this build — the feature is missing from the app.
- A mid-task navigation glitch sent the tab to about:blank; reloading the app restored an older "snapshot" state, wiping the originally built component and instance, which I had to rebuild from scratch.
- A minor UI trap: the chevron button in the COMPONENT panel header silently toggles "ready for dev" status (I reverted it), and the right panel occasionally shifts horizontally, clipping its tabs.

Because the TEXT component property could not be exposed or edited through a Properties section (feature absent), and due to the data-loss reload bug along the way, the task did not go smoothly.

verdict: not-approve
```
