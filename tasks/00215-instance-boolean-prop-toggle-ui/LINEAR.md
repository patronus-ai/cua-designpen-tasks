# DesignPen [boolean operations]: 'instance boolean prop toggle' fails QA — 5/5 runs report broken workflow (00215-instance-boolean-prop-toggle-ui)

Description:
The workflow requires exposing a component child's visibility as a BOOLEAN component property and toggling it via a checkbox in a Design panel "Properties" section — but this OpenPencil build has no Properties section and no Figma-style component-property feature at all. An exhaustive search (Design panel sections, all "..." and right-click context menus, the main menu, the visibility-eye popup, the Variables modal, Assets, Tools, Plugins, the Code/Inspect tab, and even the app's build files) found no property-creation UI. The closest available mechanism is a boolean variable bound to the child's visibility eye (right-click the eye in the Appearance section), plus an instance-level visibility override to hide the dot. The documented Properties-checkbox path is unreachable because the feature does not exist.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Build a card: draw a ~240x160 rectangle and a small ~24x24 circle "notification dot" in its top-right corner.
3. Select both layers, right-click, and choose "Create component".
4. Attempt to expose the dot's visibility as a BOOLEAN component property — search the Design panel for a "Properties" section or "Add property" control.
5. Place an instance of the card via the component's "..." menu > "Create instance".
6. Select the instance and attempt to switch the dot off via a property checkbox in a Design panel Properties section.

Actual Result:

- There is no Properties section and no component-property feature anywhere in the app. Exhaustively searched: the Design panel for main component/instance/nested layers (sections are only Position/Layout/Appearance/Fill/Stroke/Effects/Export etc.), every "..." and right-click context menu, the main menu (File/Edit/View/Object/Text/Arrange/Preferences), the visibility-eye popup (variables only), the Variables modal (collections/modes only), Assets, Tools (empty), Plugins ("No plugins installed"), and the Code/Inspect tab ("Layer properties" is just a CSS box model). Probing the app's build files also found no property-creation UI.
- The closest workaround: right-clicking the visibility eye in the dot's Appearance section (inside the main component) creates a boolean variable ("Show dot" = true) bound to the dot's visibility; the dot was switched off on the instance via an instance-level visibility override in Appearance.
- The literal requirement — a boolean component property toggled from a Properties-section checkbox — could not be fulfilled.
- Side issue: the z-order flipped during component creation and had to be fixed with "Bring to front" on the dot.

Expected Result:
The Design panel should offer a Properties section for components where a child's visibility can be exposed as a BOOLEAN component property, and instances should show that property as a checkbox that toggles the dot's visibility.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 completed runs failed
- Attempt transcripts:
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2cebb39c-b7d9-4d55-88c5-0fd6de985a8b.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_73ddc606-20b6-4947-b112-a201c13188cb.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8a600ade-83e3-4b87-aa2b-afc4f04c0fce.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_8fc608f1-609d-4a6c-8ba6-41fd4b0652a6.txt`
  - `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_af6bf48a-28dd-4f95-bb07-a278e2336311.txt`

Agent report (verbatim tail of failing run):

```
I've taken this as far as the application allows. Here's a summary of what happened:

**Completed successfully:**
1. **Card built** — a 240×160 gray rectangle ("Rectangle 1") with a 24×24 red circle ("Ellipse 1", #FF3B30) as a notification dot in its top-right corner.
2. **Component created** — both layers selected → right-click → "Create component" (the z-order flipped during creation, which I fixed with "Bring to front" on the dot).
3. **Boolean exposure (closest available mechanism)** — OpenPencil turned out to have no Figma-style component properties. The only boolean-visibility mechanism the app offers is a **boolean variable**: I right-clicked the visibility eye in the Appearance section of the dot inside the main component and created the boolean variable **"Show dot" = true**, bound to the dot's visibility (eye shows purple/bound; variable visible in the Variables modal).
4. **Instance placed** — via the component's "…" menu → "Create instance" (placed at X:434, Y:150 next to the main component).
5. **Dot switched off on the instance** — with the instance selected, I hid its dot (instance-level override): the instance now renders without the dot while the main component keeps it.

**The blocker:** the task required switching the dot off "via the property checkbox in the Design panel Properties section." **This app has no Properties section and no component-property feature at all.** I searched exhaustively: the Design panel for main component/instance/nested layers (full DOM reads — sections are only Position/Layout/Appearance/Fill/Stroke/Effects/Export etc.), every "…" and right-click context menu, the main menu (File/Edit/View/Object/Text/Arrange/Preferences), the visibility-eye popup (variables only), the Variables modal (collections/modes only), Assets, Tools (empty), Plugins ("No plugins installed"), and the Code/Inspect tab ("Layer properties" is just a CSS box model). I even probed the app's build files — there's no property-creation UI. So the boolean had to be exposed as a bound variable and the dot toggled via the Appearance visibility control instead of a non-existent Properties checkbox.

Everything else (component, instance, dot off on the selected instance, boolean variable driving the dot's visibility) is in place, but the literal requirement — a boolean **component property** toggled from a **Properties section checkbox** — could not be fulfilled because the feature does not exist in this OpenPencil build.

verdict: not-approve
```
