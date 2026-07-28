# mixed/ — MCP + UI tasks

Tasks that deliberately span both surfaces: part of the work is done with the app's MCP tools, part
by driving the UI in the browser, and the agent has to check that the two agree about **one**
document.

Why this bucket exists: the `ui/` tasks exercise the app through the canvas, the
`mcp-testing-harness/` tasks exercise the tool layer, and neither notices when the two drift apart —
a write on one surface the other never sees, a value that reads back differently, a node visible in
only one of them. That gap is what these tasks cover.

## Shape of a task

Each task alternates surfaces at least twice (MCP → UI → MCP), so a one-way sync passes the first
crossing and fails the second. Every step names which surface it belongs to.

- `available_tools` carries the browser tools **and** the MCP tools the task needs, so the metadata
  generator derives `required_tools: [browser]` and the container still serves the MCP tools,
  filtered to the listed ones.
- Findings are reported as `DESYNC #<n>` blocks (step / MCP says / UI says / severity), closing with
  the marker `mixed-report: complete`, which is the single reward.
- Numbers rounded identically on both surfaces are explicitly *not* a finding — that keeps the noise
  from earlier QA rounds (readout rounding, sub-pixel drag landings) out of the reports.

## Grounding rules honoured by the prompts

- Modifier is Ctrl (the container runs Linux), never Cmd.
- Exact-pixel gestures are avoided: vertices are selected then moved with arrow keys, sizes/radii are
  set in the properties panel — the CUA driver's sparse pointer moves make precise drags flaky.
- The pen tool is never left armed while marquee-selecting; vector edits enter through the move tool.
- Letter spacing is a percent-native numeric field: `10` means 10% and the bare readout is correct.
- No verdict depends on the clipboard.

## Contents

| Task | Crossing | MCP side |
|---|---|---|
| `50001-create-mcp-verify-ui-mixed` | create over MCP → verify + rename in UI → read back | `create_shape`, `find_nodes`, `get_node`, `rename_node`, `delete_node` |
| `50002-draw-ui-inspect-mcp-mixed` | draw in UI → inspect over MCP → resize over MCP → UI follows | `find_nodes`, `get_node`, `node_bounds`, `node_resize`, `get_page_tree` |
| `50003-fill-roundtrip-mixed` | fill over MCP → recolour in UI → read back over MCP | `create_shape`, `set_fill`, `get_node`, `select_nodes` |
| `50004-text-typography-mixed` | text + font over MCP → size/spacing/copy in UI → read back | `create_shape`, `set_text`, `set_font`, `set_text_properties`, `get_node` |
| `50005-autolayout-mixed` | auto layout over MCP → gap/direction in UI → read back | `set_layout`, `set_layout_child`, `reparent_node`, `create_shape`, `get_node` |
| `50006-component-instance-mixed` | component + instance over MCP → override in UI → read back | `create_component`, `create_instance`, `node_children`, `set_text`, `get_node` |
| `50007-vector-path-mixed` | vector over MCP → vertex moved in UI → `path_get` | `create_vector`, `path_get`, `get_node`, `node_bounds` |
| `50008-pages-mixed` | page created/switched over MCP → renamed in UI → listed over MCP | `create_page`, `switch_page`, `list_pages`, `get_current_page`, `create_shape` |
| `50009-paint-style-mixed` | style applied over MCP → detached in UI → binding read over MCP | `create_paint_style`, `apply_paint_style`, `list_paint_styles`, `node_bindings`, `get_node` |
| `50010-export-parity-mixed` | edits in UI → `get_page_tree` + `export_svg` parity | `get_page_tree`, `export_svg`, `set_fill`, `create_shape`, `viewport_zoom_to_fit` |

## Promoting into a run

These live outside `tasks/`, so they are not in `tasks.jsonl` yet. To include them:

```bash
cp -R mixed/5000*-mixed tasks/
# then regenerate the flat index the image bakes in, and rebuild/push the env image
```

Every definition validates against the gym's `Task` model and renders through `PromptBuilder`, and
every MCP tool named in `available_tools` exists in the app's tool registry.
