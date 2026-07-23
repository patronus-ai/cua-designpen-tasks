# DesignPen [fills & color]: 'variable create color' fails QA — 5/5 runs report broken workflow (00347-variable-create-color-ui)

Description:
In the Local variables dialog (opened from the left panel Variables tab), the hex input inside a COLOR variable's color-picker popover cannot be given keyboard focus by clicking. Single, double, and triple clicks (by coordinates and by element reference) all fail — focus immediately snaps back to a button in the dialog, apparently because the dialog's focus trap fights the picker popover, which renders in a portal. Pressing Tab dismisses the picker. A real user therefore cannot type an exact hex value (e.g. #FFFF00) for a color variable; the agent could only set the value by programmatically writing to the input via a native setter. The rest of the flow (collection creation, Add menu, renaming, drawing, fill binding) works.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the Local variables dialog from the left panel Variables tab.
3. Create a collection via the folder-plus button ("New collection").
4. Use the "+ Add" menu > Color to create a COLOR variable and rename it to "accent".
5. Click the variable's color swatch/value cell to open the color-picker popover.
6. Click the hex input inside the picker and attempt to type "FFFF00".

Actual Result:

- The hex input never receives keyboard focus when clicked (single/double/triple clicks, by coordinates and by element reference, across separate attempts); focus immediately snaps back to a button in the dialog.
- Pressing Tab dismisses the picker instead of moving focus into it.
- The value could only be set programmatically via a native setter on the input — a workaround unavailable to a real user.
- All other steps worked: collection creation, Add menu, renaming, drawing a 200x200 rectangle, and binding its fill to the "accent" token (Code panel confirmed `background: var(--accent, #FFFF00)`).

Expected Result:
Clicking the hex input in the variable color-picker popover should focus it and allow typing an exact hex value, which commits to the variable's mode value.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed (`verdict: not-approve`)
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_25f93d78-f1d2-46d1-af70-6b7fbdbbeaaa.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_6aa398d4-27b0-429c-9595-9692147e9d60.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_856035fc-be4f-4d1c-8247-67928f1ca98a.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c2201703-b7e2-42fe-8d92-ec6f8c369768.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c7a62523-4dd2-4bd0-a66a-71ec90bb888f.txt`

Agent report (verbatim tail of failing run):

```
All steps are complete and verified. Final state summary:

1. **Local variables dialog** – Opened from the left panel's Variables tab ✓
2. **Collection created** – "New collection" via the folder-plus button ✓
3. **COLOR variable** – Created via the "+ Add" menu → Color, renamed to "accent", value set to pure yellow **#FFFF00** (confirmed in the dialog: yellow swatch + "FFFF00" in Mode 1) ✓
4. **Square rectangle** – Drew a 200 × 200 rectangle on canvas ✓
5. **Fill bound to token** – Opened the fill picker, switched to the Libraries/Variables tab, clicked "accent" (checkmark appeared, fill swatch shows purple variable-binding diamond). The Code/Inspect panel confirms `background: var(--accent, #FFFF00)` with "Background colors: accent" ✓

**Problem encountered:** The hex input inside the variables dialog's color picker is effectively un-typeable through normal interaction — clicking it (tried single/double/triple clicks, both by coordinates and by element reference, across two separate attempts) never gives it keyboard focus; focus immediately snaps back to a button in the dialog (looks like the dialog's focus trap fights the picker popover, which renders in a portal). Pressing Tab just dismissed the picker. I could only set the value by programmatically writing to the input via a native setter — a workaround not available to a real user, who would be unable to type an exact hex value for a variable. The rest of the flow (collection creation, Add menu, renaming, drawing, fill binding) worked fine, and the end state is fully correct, but this focus bug blocked the normal hex-entry path.

verdict: not-approve
```
