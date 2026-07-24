# DesignPen [UI]: 00157-rulers-toggle premise mismatch — NOT an app bug (prompt fix)

No Linear issue — the Rulers feature works; this is task/seed design.

Description:
Rulers are enabled by default in the seed. The prompt asked to "turn ON" rulers; the agent found them already on, refused to click (which would turn them OFF), flagged the premise mismatch, and voted not-approve (5/5).

Fix applied (definition.yaml):
- Reword to a state-agnostic toggle: "click the Rulers checkbox to toggle … whatever state they are in, clicking flips it; confirm the rulers appear/disappear accordingly." Works from either starting state.

Evidence: classification.json category `agent-flaky`; 5/5 failing on premise mismatch.
