# Adversarial QA task set — cua_designpen (in scope only)

**60 tasks**: 37 UI (`20001`–`20040`) + 23 MCP (`30001`–`30025`), copied from
`patronus-gyms/cua_designpen/in-app/adversarial-tasks/` (65 tasks) and filtered to the scope
defined by `Patronus_QA_Report_EXTERNAL_updated - Figma.csv`.

## Dropped as out of scope (5)

- `20023-variable-delete-rebind-ui`, `20024-variable-malformed-values-ui`,
  `30011-bind-variable-mcp` — dedicated Variables engine is an intentional stub
  (tokens go through Styles).
- `20029-export-empty-cancel-ui`, `20030-export-giant-frame-pdf-ui` — export panel
  intentionally inert (grading reads the live canvas, not exported artifacts).

## Edited

- `20038-menu-empty-selection-ui` — the shortcut-leak probe now targets the color-style
  creation dialog (Styles, in scope) instead of the Local variables dialog (out of scope).

Everything else (format, reporting contract, `adversarial-report: complete` sentinel, single
`answer` reward) is unchanged from the source set — see its README at
`cua_designpen/in-app/adversarial-tasks/README.md`.
