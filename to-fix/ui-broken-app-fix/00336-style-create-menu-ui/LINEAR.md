# DesignPen [styles panel]: 'create shared text style via Styles "+" dialog' fails QA — 5/5 runs report broken workflow (00336-style-create-menu-ui)

Description:
The "Create new text style" dialog opened from the Styles section's "+" add-style menu cannot set an arbitrary font size. Its font-size control is a preset-only, button-type combobox offering exactly 8, 10, 12, 14, 16, 20, 24, 32, 48 — there is no 40, and the control rejects typed input (agents verified: typing fails with "no editable element is focused (active element: BUTTON)", triple-clicking just reopens the preset list, and type-ahead "4" snaps to 48). This makes it impossible to create a shared text style at size 40 through the dialog; styles created there default to a preset size (12). Compounding the problem, existing text styles can neither be edited (the pencil icon only renames — no size field) nor deleted (no context menu, trash icon, or Assets entry), so a wrongly-sized style becomes permanent cruft. The equivalent size IS settable elsewhere: the Typography panel's font-size field for a selected text layer is a normal editable input, and TextStylesMenu > "Create style" correctly captures a layer's real size — so the dialog's size picker is uniquely broken, not the styles engine.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Deselect everything (press Escape or click empty canvas).
3. In the Styles section of the properties panel, click the "+" and choose "Text" to open the "Create new text style" dialog.
4. Name the style "Heading".
5. Try to set the font size to 40 — open the size dropdown, then try typing "40" into the control.

Actual Result:

- The font-size dropdown offers only fixed presets (8, 10, 12, 14, 16, 20, 24, 32, 48); 40 is absent.
- The control is a non-editable button-type combobox: typed input is rejected ("no editable element is focused"), triple-click reopens the preset list, and type-ahead snaps "4" to 48.
- The style can only be created at a preset size (defaults to 12), and afterwards it cannot be corrected: the edit pencil only renames, and there is no way to delete a text style anywhere in the UI (Styles section, right-click, or Assets panel).
- Workaround: set a text layer to 40 in the (editable) Typography font-size field, then use TextStylesMenu > "Create style" to capture size 40 — proving the limitation is specific to the "+" dialog.

Expected Result:
The "Create new text style" dialog's font-size control should accept a custom typed value (like the Typography panel's size field does) or at minimum include the full range of sizes, so a shared style such as "Heading" at 40 can be created directly. Text styles should also be editable and deletable after creation.

Estimate: M (3 points) — swap the preset-only combobox for the editable size input used in the Typography panel; style edit/delete gaps are related but may split into a follow-up.

Evidence:

- QA job `db76a8af-97c9-41fb-bbba-42d2d887d5b8`, model `claude-opus-4-8` — 5 of 5 runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_35c8d690-0bc2-4a87-b0a5-8c2b46c5bc52.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_12c367e7-a6bf-422f-8379-542ca6628877.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2fba75ed-fa83-414c-90ff-cc451712441b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_218db66a-fcc3-498f-a8f3-2de871aed3f2.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_02cf372e-d581-4794-b850-6d8ce720b9d5.txt`

Agent report (verbatim tail of failing run):

```
The task is now complete to the fullest extent the app allows, and the final state is verified. Here is my summary.

**What I did:**
1. **Deselected everything** on the canvas (Escape / clicked empty canvas).
2. **Attempted to create the "Heading" text style (font size 40) via the Styles "+" menu** → Styles "+" → Text → "Create new text style" dialog.
3. **Created the text layer** "Quarterly report".
4. **Applied the "Heading" style via the TextStylesMenu** in the Typography section — the layer now shows the chip "Ag Heading · 40/48", and the TextStylesMenu shows "Heading" checkmarked.

Final state (verified): the document Styles section has one text style named **"Heading · 40/Auto"**, which is applied to the "Quarterly report" layer.

**Problems / bugs / blockers I hit:**
- **The Styles "+" "Create new text style" dialog cannot set font size 40.** Its font-size control is a *preset-only dropdown* (8, 10, 12, 14, 16, 20, 24, 32, 48) — there is no 40 option, and it's a button-type combobox that rejects typed input (typing fails because the focused element is a non-editable DIV; the font family and line-height fields next to it *are* editable, but font size is not). So the task's core instruction — create the style at font size 40 through that dialog — is not achievable as written. I worked around it by setting a text layer to 40px in the editable Typography panel and then using the TextStylesMenu's "Create style" (which captures the real 40px size) to produce the correct "Heading · 40" style.
- **There is no way to delete a text style in this app** (no right-click context menu, no hover trash icon, and the Assets panel only manages components). My first attempt via the "+" dialog left a stuck-at-12px "Heading" style that I could not remove, so to avoid a duplicate-name collision I could only *rename* it to "Unused 12px" (still visible in the Styles list as leftover cruft).

Because the primary instruction could not be completed through the specified UI path (the Styles "+" dialog's font size has no 40 and no custom entry), and style deletion is unsupported, this required workarounds rather than working cleanly as described.

verdict: not-approve
```
