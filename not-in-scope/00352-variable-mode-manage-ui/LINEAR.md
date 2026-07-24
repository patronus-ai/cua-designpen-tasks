# DesignPen [variables]: 'variable mode manage' fails QA — 3/3 runs report broken workflow (00352-variable-mode-manage-ui)

Description:
"Set as default" on a variable mode's context menu in the Local variables dialog does not re-resolve bound properties on the canvas: after setting a second mode ("High contrast", panel-width = 480) as default, a rectangle whose width is bound to "panel-width" stays at 240 and only jumps to 480 after manually switching the collection's "Active mode" dropdown. The default-mode change (and the active-mode selection) also silently reverts to Mode 1 on every page reload, while renames, values, mode add/delete, and the binding itself persist fine. Secondary bugs: the dialog/canvas frequently render stale (the mode "+" button appeared to do nothing and produced a duplicate Mode 3), and clicking the W input before using the "Apply variable" diamond makes the committed numeric value override the binding.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Local variables dialog from the left panel Variables tab.
3. Create a collection ("New collection").
4. Add a FLOAT variable "panel-width" with value 240 in the default mode (Mode 1).
5. Add a second mode via the mode header "+" and set "panel-width" to 480 in the new column.
6. Close the dialog, draw a rectangle, and bind its width to "panel-width" via the Apply-variable diamond (without focusing the W input first) — it should snap to 240.
7. Reopen the dialog, open the second mode's context menu, rename it to "High contrast", then click "Set as default".
8. Observe the bound rectangle; then reload the page and check whether the default mode persisted.

Actual Result:

- Core failure: after "Set as default" was applied to "High contrast" (verified: the menu item disappeared from its context menu), the bound rectangle never re-resolved — it stayed at 240. Width only became 480 after manually switching the collection's "Active mode" dropdown to High contrast, an extra step the flow shouldn't require.
- Persistence bug: the "Set as default" change (and the active-mode selection) silently reverts to Mode 1 on every page reload, despite retries and waits; renames, values, mode add/delete, and the binding all persist fine.
- Stale-render bug: the dialog/canvas frequently didn't refresh after changes — the mode "+" button appeared to do nothing and created a duplicate mode (Mode 3) that had to be deleted; reloads were needed to see true state.
- Binding quirk: clicking the W input before using the "Apply variable" button caused the committed numeric value to override the binding; binding only worked via the Apply-variable diamond without focusing the input first.

Expected Result:
Setting a mode as default should by itself cause bound properties on the canvas to re-resolve (the rectangle width jumps to 480), and the default-mode choice should persist across page reloads.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 3 of 3 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_41e5b613-f8ce-4fd7-9a82-1fe8748e0864.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_42755dd4-e595-4e17-a3c2-f83e0f4bd9eb.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_48ab573d-c9be-4686-9082-3e9b1603c04b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4dca45ee-18a4-483d-a2a7-369b3d0121e2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ac3bde9a-eb71-4994-9733-53b049c45a64.txt`

Agent report (verbatim tail of failing run):

```
All task steps are complete and the final live state shows the rectangle at 480 × 130 with the variable binding intact, "High contrast" renamed and set as default. Here's my summary:

**What was accomplished:**
1. ✅ Opened Local variables dialog from the left panel Variables tab
2. ✅ Created a collection ("New collection")
3. ✅ Added FLOAT variable "panel-width" = 240 in the default mode (Mode 1)
4. ✅ Added a second mode via the header "+" and set its value to 480
5. ✅ Drew a rectangle and bound its width to "panel-width" — it snapped to 240
6. ✅ Renamed the second mode to "High contrast" via its context menu
7. ⚠️ Clicked "Set as default" on "High contrast" — but the rectangle did **not** jump to 480 on its own

**Problems/bugs encountered:**
- **Core failure:** Setting "High contrast" as default (verified applied: the "Set as default" item disappeared from its context menu) never caused the bound rectangle to re-resolve — it stayed at 240. The width only became 480 after I manually switched the collection's "Active mode" dropdown to High contrast, an extra step the task flow shouldn't require.
- **Persistence bug:** The "Set as default" change (and the active-mode selection) silently reverts to Mode 1 on every page reload, despite retries and waits; meanwhile renames, values, mode add/delete, and the binding all persist fine.
- **Stale-render bug:** The dialog/canvas frequently didn't refresh after changes — the mode "+" button appeared to do nothing and created a duplicate mode (Mode 3) that I had to delete; reloads were needed to see true state.
- **Binding quirk:** Clicking the W input before using the "Apply variable" button caused the committed numeric value to override the binding; binding only worked via the Apply-variable diamond button without focusing the input first.

The end state was ultimately reached in the live session, but only by working around several bugs, and the key expected behavior ("set as default → bound width jumps to 480") does not work by itself, nor does the default-mode change persist.

verdict: not-approve
```
