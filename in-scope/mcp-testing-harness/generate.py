#!/usr/bin/env python3
"""Generate the MCP testing-harness task set (40001-40024) for cua_designpen.

Chained end-to-end MCP workflows: output of one call feeds the next, expected-vs-actual
checked at every step. Scope: in-scope features only (no variables engine, no AI/collab).
"""
import json
import os

import yaml

BROWSER_TOOLS = [
    "browser_navigate", "browser_screenshot", "browser_click", "browser_right_click",
    "browser_double_click", "browser_mouse_move", "browser_drag", "browser_scroll",
    "browser_scroll_to", "browser_press_key", "browser_type", "browser_wait",
    "browser_get_page_text", "browser_evaluate", "browser_upload_file",
    "browser_create_tab", "browser_close_tab", "browser_switch_tab", "browser_list_tabs",
]

PREFIX = ("Using only MCP tools (the browser is allowed only for screenshots and visual "
          "verification): ")

DISCIPLINE = ("\n\nHarness discipline: before EVERY tool call, state the output you expect; "
              "after the call, compare actual vs expected and flag any mismatch. Pay special "
              "attention to data-modeling issues: fields that do not round-trip, list vs detail "
              "disagreements, IDs that change format between tools, broken references between "
              "nodes, stale reads after writes, and silently truncated results. When you are "
              "done, zoom the canvas to fit (press Shift+1 in the browser) and take a browser "
              "screenshot so the final state can be visually verified.")

REPORT = ('\n\nLog every mismatch or defect you find using exactly this format, one block per '
          'finding:\n\nMISMATCH #<n>\nStep: <the exact tool call with its arguments>\n'
          'Expected: <what you expected and why>\nActual: <what the tool returned / what the '
          'app did>\nSeverity: <critical | major | minor | cosmetic>\n\nFields that do not '
          'round-trip, list vs detail disagreements, broken references, stale reads after '
          'writes, silent truncation, free-form or unstructured error payloads, misleading '
          'success responses, and any single response over ~50K characters all count as '
          'findings. If you found no mismatches, state exactly "NO MISMATCHES FOUND". At the '
          'very end of your final message, end with exactly "mcp-harness-report: complete".')

TASKS = [
    ("40001-shape-crud-chain-mcp",
     "Run a full CRUD chain on one shape: (1) create_shape a RECTANGLE named \"CRUD Card\", "
     "120x80 at (40,40); (2) find_nodes with name \"CRUD Card\" — expect exactly one hit and "
     "keep its id; (3) get_node on that id — name, type, x, y, width and height must round-trip "
     "exactly as created; (4) update_node setting width=200, opacity=0.5 and corner_radius=8; "
     "(5) get_node again — the three changed fields must read back exactly, and the untouched "
     "fields (x, y, height, name) must be unchanged; (6) rename_node to \"CRUD Card v2\", then "
     "find_nodes for the old and the new name — the old name must return no results and the new "
     "exactly one; (7) delete_node, then find_nodes \"CRUD Card v2\" — expect an empty result; "
     "(8) get_node on the deleted id — expect a structured not-found error that is clearly "
     "distinguishable from an empty result.",
     ["create_shape", "find_nodes", "get_node", "update_node", "rename_node", "delete_node"]),

    ("40002-structure-group-chain-mcp",
     "Exercise the node-structure tools as one chain: (1) create_shape three 60x60 RECTANGLEs "
     "named A1, A2, A3 at x=0, 80, 160 (y=0); (2) group_nodes the three and keep the group id; "
     "(3) node_children on the group — expect exactly the three ids; (4) node_tree on the group "
     "and node_ancestors on A1 — the parent/child edges must agree in both directions; "
     "(5) clone_node the group — the clone and every descendant must get fresh ids distinct from "
     "the originals; (6) create_shape a FRAME \"Holder\" 400x300 at (0,200), then reparent_node "
     "A1 into Holder with insert_index 0 — node_children on both the group and Holder must "
     "reflect the move, and node_ancestors on A1 must now include Holder; (7) ungroup_node the "
     "original group — its remaining children must survive as siblings and get_node on the old "
     "group id must return a structured not-found error.",
     ["create_shape", "group_nodes", "node_children", "node_tree", "node_ancestors",
      "clone_node", "reparent_node", "ungroup_node", "get_node"]),

    ("40003-page-lifecycle-chain-mcp",
     "Run a page lifecycle chain: (1) list_pages and get_current_page — note the current page "
     "and the id/name format used; (2) create_page \"QA Page\" — list_pages must now include it "
     "using the same entry shape as the existing pages; (3) switch_page to \"QA Page\" — "
     "get_current_page must agree; (4) create_shape a 100x100 RECTANGLE \"Marker\" on it, then "
     "page_bounds — the reported bounds must contain the rectangle; (5) reorder_page \"QA Page\" "
     "to index 0 — list_pages order must reflect the move; (6) switch_page back to the original "
     "page — find_nodes \"Marker\" there must return nothing (page scoping); (7) delete_page "
     "\"QA Page\" — list_pages must drop it and get_current_page must still return a valid "
     "page; (8) attempt delete_page on the now-current page only if more than one page remains, "
     "otherwise call delete_page with a nonexistent page name — either way the response must be "
     "a structured, informative error or a clean success, never a wedged document.",
     ["list_pages", "get_current_page", "create_page", "switch_page", "create_shape",
      "page_bounds", "reorder_page", "find_nodes", "delete_page"]),

    ("40004-component-instance-chain-mcp",
     "Chain the component tools end to end: (1) create_shape a FRAME \"Button\" 120x40 at (0,0), "
     "create_shape a TEXT child inside it (parent_id = Button) and set_text it to \"Buy\"; "
     "(2) create_component on the Button frame — keep the component id; get_components must list "
     "it under the same id; (3) create_instance of the component at (0,100) — get_node on the "
     "instance must report type INSTANCE and reference the component; (4) inspect the instance "
     "with get_node/describe to discover its exposed properties, then set_instance_property to "
     "override the text to \"Sell\" — verify via get_node that the instance shows \"Sell\" while "
     "the master still shows \"Buy\"; (5) create_shape a 80x80 RECTANGLE \"Chip\" and "
     "node_to_component it — get_components must now list two components; (6) delete_node the "
     "Button master component, then get_node on the instance — record exactly what happens to "
     "the orphaned instance; a dangling reference that later tool calls crash on is a finding.",
     ["create_shape", "set_text", "create_component", "get_components", "create_instance",
      "set_instance_property", "node_to_component", "describe", "get_node", "delete_node"]),

    ("40005-paint-style-chain-mcp",
     "Chain the paint-style tools: (1) create_shape a 100x100 RECTANGLE \"Styled\" and set_fill "
     "#3366FF; (2) create_paint_style \"Brand Blue\" from that node (node_id) — "
     "list_paint_styles must include it with an id; (3) create_shape a second RECTANGLE "
     "\"Styled 2\" and apply_paint_style with the style id — get_node must show the #3366FF "
     "fill; (4) update_paint_style the style color to #FF6600 — get_node on BOTH rectangles "
     "must show the new color (style propagation); (5) detach_paint_style on \"Styled 2\", then "
     "update_paint_style to #00AA00 — \"Styled\" must change but \"Styled 2\" must stay "
     "#FF6600; (6) apply_paint_style with a nonexistent style_id — expect a structured error, "
     "not a silent no-op.",
     ["create_shape", "set_fill", "create_paint_style", "list_paint_styles",
      "apply_paint_style", "update_paint_style", "detach_paint_style", "get_node"]),

    ("40006-text-font-chain-mcp",
     "Chain the text and font tools: (1) create_shape a TEXT node \"Headline\" 300x60 at (0,0) "
     "and set_text \"The quick brown fox\"; (2) list_fonts and list_available_fonts — compare "
     "the two responses (entry shape, overlap, filtering by family) and flag inconsistencies "
     "between them; pick a family both report (e.g. Roboto); (3) set_font with that family, "
     "size 24 and a bold style — get_node must round-trip family, size and style exactly; "
     "(4) set_font_range start 4 end 9 with size 40 and color #FF0000 — get_node/describe must "
     "show the mixed styling on exactly that range; (5) set_text to replace the full text — "
     "record what happens to the range styling (silent corruption is a finding); "
     "(6) set_text_properties align_horizontal CENTER and set_text_resize TRUNCATE — read both "
     "back via get_node.",
     ["create_shape", "set_text", "list_fonts", "list_available_fonts", "set_font",
      "set_font_range", "set_text_properties", "set_text_resize", "describe", "get_node"]),

    ("40007-vector-path-chain-mcp",
     "Chain the vector path tools, verifying geometry math at each step: (1) create_vector at "
     "(0,0) named \"Path\" with path \"M 0 0 L 100 0 L 100 100 Z\"; (2) path_get — the returned "
     "path must be equivalent to what was set (round-trip); (3) path_set to "
     "\"M 0 0 L 100 0 L 100 100 L 0 100 Z\" and path_get again; (4) path_move dx=50 dy=25, then "
     "node_bounds — the bounds must shift by exactly (50,25); (5) path_scale factor 2 — the "
     "bounds must double; (6) path_flip horizontal — bounds must stay the same while path_get "
     "shows mirrored geometry; (7) set_stroke #000000 weight 2, then set_stroke_width_profile "
     "with a points string defining a variable-width profile (inspect the tool description for "
     "the exact format) — read back via get_node/path_get; a profile that is accepted but "
     "silently ignored is a finding.",
     ["create_vector", "path_get", "path_set", "path_move", "path_scale", "path_flip",
      "node_bounds", "set_stroke", "set_stroke_width_profile", "get_node"]),

    ("40008-boolean-flatten-chain-mcp",
     "Verify all four boolean operations and flattening: (1) create_shape two overlapping "
     "100x100 RECTANGLEs U1 at (0,0) and U2 at (50,50), then boolean_union — expect a single "
     "result node; the originals must be consumed (find_nodes on their names empty) and "
     "node_bounds of the result must be 150x150; (2) repeat with fresh overlapping pairs for "
     "boolean_subtract, boolean_intersect (bounds must be the 50x50 overlap) and "
     "boolean_exclude, checking bounds sanity each time; (3) flatten_nodes on the union result — "
     "it must become plain vector geometry and path_get must return a real path; "
     "(4) boolean_union with only one id, and with one valid plus one nonexistent id — both "
     "must produce structured errors or clearly documented behavior, never a half-applied "
     "operation.",
     ["create_shape", "boolean_union", "boolean_subtract", "boolean_intersect",
      "boolean_exclude", "flatten_nodes", "node_children", "node_bounds", "find_nodes",
      "path_get", "get_node"]),

    ("40009-geometry-transform-chain-mcp",
     "Verify geometry reads and writes agree: (1) create_shape a RECTANGLE \"Geo\" 100x50 at "
     "(10,10); node_bounds must report exactly x=10 y=10 width=100 height=50 and get_node must "
     "agree field-for-field; (2) node_move to (200,300) — both readers must match exactly; "
     "(3) node_resize to 250x125 — both readers must match; (4) set_rotation 45 — record what "
     "node_bounds reports (rotated AABB ≈ 265x265 for this size) vs what get_node width/height "
     "mean, and flag if the two readers silently disagree about rotated geometry; "
     "(5) set_constraints horizontal STRETCH vertical CENTER and set_minmax min_width 50 "
     "max_width 400 — get_node must round-trip all four; (6) node_resize to 500x50 — check "
     "whether max_width=400 actually clamps the resize; a constraint that is stored but never "
     "enforced (or silently dropped) is a finding.",
     ["create_shape", "node_bounds", "node_move", "node_resize", "set_rotation",
      "set_constraints", "set_minmax", "get_node"]),

    ("40010-appearance-roundtrip-chain-mcp",
     "Round-trip every appearance property on one node, reading back with get_node after EVERY "
     "write: (1) create_shape a 150x150 RECTANGLE \"Look\"; (2) set_fill #FF0000; (3) set_fill "
     "with color #FF0000, color_end #0000FF and gradient left-right; (4) set_stroke #000000 "
     "weight 4 align OUTSIDE; (5) set_stroke_align CENTER; (6) set_opacity 0.35; (7) set_blend "
     "MULTIPLY; (8) set_radius with top_left 4, top_right 8, bottom_right 12, bottom_left 16; "
     "(9) set_effects type DROP_SHADOW color #000000 offset_x 0 offset_y 4 radius 10. Each "
     "read-back must return exactly what was written — flag any value that comes back mutated "
     "(0.35 → 0.3499…), any per-corner radius flattened to a uniform one, any gradient or "
     "stroke-align detail lost, and any effect field missing from the read.",
     ["create_shape", "set_fill", "set_stroke", "set_stroke_align", "set_opacity", "set_blend",
      "set_radius", "set_effects", "get_node"]),

    ("40011-autolayout-arrange-chain-mcp",
     "Verify layout math end to end: (1) create_shape a FRAME \"Row\" 400x120 at (0,0) and "
     "three 60x60 RECTANGLE children inside it; (2) set_layout on Row with direction HORIZONTAL, "
     "spacing 20, padding 10 — node_bounds of the children must show x offsets 10, 90 and 170 "
     "inside the frame (padding + spacing math); (3) set_layout_child on the middle child with "
     "sizing_horizontal FILL and grow 1 — verify via node_bounds that it actually expands and "
     "via get_node that the setting round-trips; (4) create_shape three loose 40x40 rectangles, "
     "then arrange them with mode row and gap 30 — verify the resulting positions; "
     "(5) distribute the same three with axis horizontal gap 15 — verify; (6) tidy them — "
     "verify spacing is normalized. State the exact expected coordinates before each step and "
     "compare against node_bounds after.",
     ["create_shape", "set_layout", "set_layout_child", "node_bounds", "arrange", "distribute",
      "tidy", "get_node"]),

    ("40012-image-fill-chain-mcp",
     "Chain the image tools: (1) stock_photo requesting one photo (inspect the tool description "
     "for the requests format); (2) create_shape a 200x150 RECTANGLE \"Photo\" and "
     "set_image_fill with the returned image data — get_node must show an image fill with "
     "scale_mode FILL; (3) update_image_fill with scale_mode TILE, tile_scale 0.5, rotation 90 "
     "and exposure 0.2 — read back every changed field via get_node; adjustments that are "
     "accepted but not persisted are findings; (4) export_image on the rectangle with format "
     "PNG and scale 2 — expect image data back; create_shape a second RECTANGLE \"Copy\" and "
     "set_image_fill it with the exported data (the export→import round-trip); (5) export_image "
     "with a nonexistent id and with scale 0 — both must produce structured errors.",
     ["stock_photo", "create_shape", "set_image_fill", "update_image_fill", "export_image",
      "get_node"]),

    ("40013-icon-pipeline-chain-mcp",
     "Chain the icon tools: (1) search_icons with queries [\"arrow\", \"home\"] and limit 5 — "
     "expect named results for both queries; (2) fetch_icons for two of the returned names at "
     "size 32 — expect icon data whose names match what search returned (search→fetch "
     "consistency); (3) insert_icon one of those names at size 48 with color #333333 — "
     "find_nodes must show the inserted node and node_bounds must be about 48x48; "
     "(4) search_icons with an empty queries list, and insert_icon with a nonexistent icon "
     "name — both must return structured errors, and a legitimate zero-hit search must be "
     "clearly distinguishable from those errors.",
     ["search_icons", "fetch_icons", "insert_icon", "find_nodes", "node_bounds", "get_node"]),

    ("40014-export-import-roundtrip-mcp",
     "Test the export surface as a round-trip: (1) create_shape a FRAME \"Scene\" 300x200 with "
     "a RECTANGLE child and a TEXT child (set_text \"Export me\"); (2) export_svg on the frame — "
     "the SVG must contain both children; (3) import_svg the exact returned SVG string as "
     "\"Reimport\" — node_tree of Reimport vs node_tree of Scene: compare structure and "
     "geometry and flag any drift (that is the round-trip test); (4) export_fig — expect a "
     "structured response, record its size; (5) export_pdf on the frame — record exactly what "
     "comes back; any crash, empty payload or unstructured error is a finding; (6) export_svg "
     "with a nonexistent id — structured error required.",
     ["create_shape", "set_text", "export_svg", "import_svg", "node_tree", "export_fig",
      "export_pdf", "get_node"]),

    ("40015-selection-viewport-chain-mcp",
     "Verify selection and viewport round-trips: (1) create_shape three 80x80 RECTANGLEs S1, "
     "S2, S3; select_nodes S1 and S2 — get_selection must return exactly those two ids in the "
     "same id format find_nodes uses; (2) select_nodes [] — the selection must read back empty, "
     "clearly distinguishable from an error; (3) viewport_set x 100 y 200 zoom 2 — viewport_get "
     "must round-trip all three values exactly; (4) viewport_zoom_to_fit on S3 — viewport_get "
     "must change, and from node_bounds you must be able to confirm S3 is inside the visible "
     "area; (5) delete_node S1, then select_nodes [S1's old id] — expect a structured error or "
     "clean rejection, and get_selection must never contain dead ids afterwards.",
     ["create_shape", "select_nodes", "get_selection", "viewport_set", "viewport_get",
      "viewport_zoom_to_fit", "delete_node", "find_nodes", "node_bounds"]),

    ("40016-analyze-ground-truth-mcp",
     "Test the analyze tools against a scene you control: (1) build ground truth — four 50x50 "
     "RECTANGLEs in a row at x = 0, 70, 140, 210 (a constant 20px gap), set_fill two of them "
     "#FF0000 and two #0000FF; add one TEXT \"Sample\" with set_font size 16 and one TEXT "
     "\"Big\" with size 32; (2) analyze_spacing — it must report the 20px gap; (3) "
     "analyze_colors with limit 10 — it must report exactly the two fill colors with two uses "
     "each; (4) analyze_typography with group_by size — it must report sizes 16 and 32; (5) "
     "analyze_clusters with min_count 2 — it should detect the row of rectangles. Compare every "
     "response against the known scene: colors or sizes that exist but are not reported, and "
     "anything reported that does not exist, are findings.",
     ["create_shape", "set_fill", "set_text", "set_font", "analyze_spacing", "analyze_colors",
      "analyze_typography", "analyze_clusters", "get_node"]),

    ("40017-read-shape-consistency-mcp",
     "Response-shape consistency audit: (1) create_shape a FRAME \"Probe\" 200x100 at (0,0) "
     "with one RECTANGLE child; (2) read the SAME frame through every read tool: get_node, "
     "find_nodes, node_tree, get_page_tree, query_nodes (inspect the tool description for the "
     "selector syntax and select it by name) and describe; (3) build a field-by-field "
     "comparison: id format (string vs number, same value everywhere?), type naming (FRAME vs "
     "frame vs Frame), geometry fields (x/y/width/height vs bounds objects), how children are "
     "represented, and whether optional fields are consistently present-and-null vs sometimes "
     "missing. ANY disagreement between two tools describing the same entity is a finding — "
     "shape drift is the thing this task hunts; (4) query_nodes with a selector that matches "
     "nothing — the empty result must be clearly distinguishable from an invalid-selector "
     "error.",
     ["create_shape", "get_node", "find_nodes", "node_tree", "get_page_tree", "query_nodes",
      "describe"]),

    ("40018-codegen-diff-chain-mcp",
     "Chain the codegen and diff tools: (1) create_shape a FRAME \"Widget\" 200x120 with a "
     "RECTANGLE child and a TEXT child (set_text \"Hi\"); get_jsx on Widget — the JSX must "
     "reference both children; (2) using the JSX dialect you just observed, call render to "
     "create a new small frame at (0,400) — find_nodes must show it and get_jsx on it must "
     "round-trip semantically; (3) node_replace_with on the rendered frame's rectangle, "
     "swapping it for a modified element — verify via get_node/node_tree; (4) diff_jsx from "
     "Widget to the rendered frame, diff_create between the same two, and diff_show on Widget "
     "with a props argument — each must return a structured, non-empty response that actually "
     "reflects the differences; (5) design_to_component_map — Widget must appear in the map; "
     "(6) get_codegen_prompt — expect a non-empty prompt; (7) done_with_changes on Widget with "
     "reason \"qa pass\" — record the response shape.",
     ["create_shape", "set_text", "get_jsx", "render", "node_replace_with", "diff_jsx",
      "diff_create", "diff_show", "design_to_component_map", "get_codegen_prompt",
      "done_with_changes", "find_nodes", "node_tree", "get_node"]),

    ("40019-batch-mixed-readwrite-mcp",
     "Test batching, atomicity and read-after-write freshness: (1) calc with expression "
     "\"17 * 3 + 9\" — expect exactly 60; (2) create_shape two 100x100 RECTANGLEs B1 and B2; "
     "(3) batch_update with a single operations JSON setting width=200 and opacity=0.4 on both — "
     "IMMEDIATELY get_node both: every change must be visible in the very next read (a stale "
     "read is a critical finding); (4) get_node B1, take the width it returns, and batch_update "
     "B1's width to that value plus 10 — verify the write-from-read lands at 210; (5) "
     "batch_update mixing one valid operation (B1 width 300) with one operation on a "
     "nonexistent id — record whether the batch is atomic (nothing applied) or partial (B1 "
     "changed), and whether the response identifies which operation failed; EITHER behavior is "
     "acceptable only if the response states it explicitly — silent partial application is a "
     "finding; (6) call update_node on B2's opacity five times in rapid succession (0.1 … 0.5) "
     "then get_node — the final value must be the last write.",
     ["calc", "create_shape", "batch_update", "update_node", "get_node"]),

    ("40020-error-surface-audit-mcp",
     "Audit the error surface for consistency (create one RECTANGLE \"Baseline\" first so you "
     "have a valid id to contrast against): (1) call get_node, delete_node, rename_node, "
     "node_move and node_bounds each with the nonexistent id \"zzz-does-not-exist\" — all five "
     "must return a structured not-found error; compare the five error payloads with each "
     "other: do they share the same shape (status/code/message)? Divergent error shapes across "
     "tools are a finding; (2) wrong types: create_shape with width \"wide\", set_opacity with "
     "value \"half\", node_move with x null — graceful, informative errors required; "
     "(3) missing required params: create_shape without type, rename_node without name; "
     "(4) find_nodes with name \"NoSuchNodeName\" — this must return an EMPTY RESULT, not an "
     "error, and its shape must be clearly different from the errors above (no-results vs "
     "error distinguishability); (5) inspect every error you collected: any stack trace, file "
     "path, or internal implementation detail leaking through is a finding.",
     ["create_shape", "get_node", "delete_node", "rename_node", "node_move", "node_bounds",
      "set_opacity", "find_nodes"]),

    ("40021-large-response-truncation-mcp",
     "Test large result sets and truncation honesty: (1) create 60 RECTANGLEs named "
     "\"Bulk 001\" through \"Bulk 060\" (40x40, laid out in a grid) — use batch_update with "
     "chunked operations JSON, or eval if it is enabled (eval requires OPENPENCIL_MCP_EVAL=1; "
     "if it is rejected as disabled, record the error shape and fall back to batch_update); "
     "(2) find_nodes with type RECTANGLE — count the results: all 60 must be returned, or the "
     "response must EXPLICITLY say it was cut (silent truncation is a critical finding); "
     "confirm you can locate \"Bulk 042\" specifically; (3) get_page_tree at full depth — "
     "measure the response size and flag it if it exceeds ~50K characters or is truncated "
     "without saying so; (4) query_nodes with limit 10 — expect exactly 10 plus some indication "
     "that more exist; (5) describe on the page — response size must stay sane. Any oversized "
     "or silently-cut response is a finding.",
     ["create_shape", "batch_update", "eval", "find_nodes", "get_page_tree", "query_nodes",
      "describe", "get_node"]),

    ("40022-server-file-roundtrip-mcp",
     "Test the server file tools (they require OPENPENCIL_MCP_ROOT; if a call is rejected as "
     "disabled, record the exact error — it must be structured and self-explanatory, that IS "
     "part of the test — then continue with whatever remains possible): (1) create_shape a "
     "RECTANGLE \"Original\" so the document is non-empty, then save_file as "
     "\"qa-harness-a.pencil\" — expect a saved path back; (2) new_document — the document must "
     "reset: find_nodes returns nothing and list_pages shows a fresh document; (3) create_shape "
     "a RECTANGLE \"Marker\", save_file as \"qa-harness-b.pencil\"; (4) open_file the FIRST "
     "saved path — \"Marker\" must be gone and \"Original\" must be back (the persistence "
     "round-trip); (5) open_file \"no/such/file.pencil\" — structured not-found error; "
     "(6) open_file \"../outside-root.pencil\" — the path traversal must be refused with a "
     "structured error, never read from outside the sandbox root.",
     ["create_shape", "save_file", "new_document", "open_file", "find_nodes", "list_pages",
      "get_node"]),

    ("40023-text-on-path-chain-mcp",
     "Chain text-on-path: (1) create_vector \"Arc\" at (0,0) with the curved path "
     "\"M 0 100 Q 100 0 200 100\"; create_shape a TEXT node \"Rider\" and set_text "
     "\"Follow the curve\"; (2) attach_text_to_path with the text id and the vector id — "
     "get_node on the text must reflect the attachment; (3) set_text_path_options with offset "
     "20, side RIGHT, reversed true and align CENTER — read every option back; options that "
     "are accepted but not persisted are findings; (4) set_text_path_options with detach true — "
     "the text must be a free node again; (5) attach_text_to_path using a RECTANGLE id as the "
     "pathId (not a vector), and then with a nonexistent pathId — both must return structured "
     "errors.",
     ["create_vector", "create_shape", "set_text", "attach_text_to_path",
      "set_text_path_options", "get_node"]),

    ("40024-visibility-lock-slice-mcp",
     "Test visibility, locking, slices and section status: (1) create_shape a RECTANGLE "
     "\"Guard\" 100x100; set_visible false — get_node must report visible false; check whether "
     "find_nodes still returns the hidden node and record the behavior; set_visible true; "
     "(2) set_locked true, then attempt node_move and set_fill on the locked node — record "
     "whether mutations are refused with a structured error or silently applied; silently "
     "mutating a locked node is a finding; set_locked false; (3) create_slice at (0,0) 200x200 "
     "named \"Cut\" — get_node must report a slice-typed node with those bounds; (4) "
     "create_shape a SECTION \"Zone\" 300x200, then set_section_status to BUILD and afterwards "
     "to COMPLETED with a reason — read the status back after each change; (5) "
     "set_section_status with the invalid status \"DONE\" — structured error required.",
     ["create_shape", "set_visible", "set_locked", "node_move", "set_fill", "create_slice",
      "set_section_status", "find_nodes", "get_node"]),
]

OUT = os.path.dirname(os.path.abspath(__file__))


def main():
    jsonl = []
    for task_id, body, tools in TASKS:
        prompt = PREFIX + body + DISCIPLINE + REPORT
        definition = {
            "id": task_id,
            "start_url": "http://cua_designpen.web",
            "prompt": prompt,
            "available_tools": BROWSER_TOOLS + tools,
            "required_tools": tools,
            "rewards": [{
                "name": "MCP harness report delivered",
                "kind": "answer",
                "comparator": "STRING_CONTAINS",
                "expected": "mcp-harness-report: complete",
            }],
        }
        d = os.path.join(OUT, task_id)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "definition.yaml"), "w") as f:
            yaml.dump(definition, f, sort_keys=False, allow_unicode=True, width=110)
        jsonl.append({
            "id": task_id,
            "prompt": prompt,
            "available_tools": definition["available_tools"],
            "rewards": definition["rewards"],
            "start_url": definition["start_url"],
            "hint": None,
            "bootstrap_data": None,
        })
    with open(os.path.join(OUT, "tasks.jsonl"), "w") as f:
        for o in jsonl:
            f.write(json.dumps(o) + "\n")
    used = set()
    for _, _, tools in TASKS:
        used.update(tools)
    print(f"wrote {len(TASKS)} tasks, {len(used)} distinct app tools covered")


if __name__ == "__main__":
    main()
