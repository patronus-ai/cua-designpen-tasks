# DesignPen [MCP tools]: 'insert icon' fails QA — 5/5 runs report broken workflow (10070-insert-icon-mcp)

Description:
The `insert_icon` MCP tool in the DesignPen/OpenPencil design app fails on every call with `{"error": "Failed to fetch"}` — it needs to fetch icon data from an external source (the Iconify API), which is unreachable from the sandboxed QA environment. The failure is not icon-specific: `mdi:home` and `lucide:home` fail identically, in both the `name` shorthand and `names` array forms and with an explicit `color` parameter. The tool's docs mention icons being "cached by fetch_icons", but no `fetch_icons` tool was available in the run's toolset to pre-cache and work around the network block, so no icon node is ever created and the canvas stays empty.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Call the `insert_icon` MCP tool with `name: 'mdi:home'`, `size: 48`.
3. Retry with the `names` array form and with an explicit `color` parameter; also try a different icon set (e.g. `lucide:home`).
4. Call `viewport_zoom_to_fit`.
5. Verify with `find_nodes` (unfiltered and searching for "home").

Actual Result:

- Every `insert_icon` attempt returns `{"error": "Failed to fetch"}`, regardless of icon name, call form, or `color` parameter.
- `viewport_zoom_to_fit` returns `{"error": "No valid nodes found"}` since no node was created.
- `find_nodes` returns `count: 0` in all queries — the document is completely empty; no icon node (full or partial) exists on the canvas.
- No `fetch_icons` tool is available in the toolset to pre-cache the icon as the docs suggest.

Expected Result:
`insert_icon` with `mdi:home` at size 48 should create an icon node on the canvas (icon data must be reachable or served locally, or a working pre-caching path must be exposed), and verification tools should find the inserted node.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_0db7eec4-07cc-4c7d-adc1-61e21ada93f7.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_85f352a4-a16e-40a4-8e59-20c9126cc7c0.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b11600b0-9500-4c68-be29-781c51ac1a16.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e8b53886-0bfa-44e0-8a21-207282afd72a.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_fb3e5b21-fa7d-4426-99c1-fd4a4c5de8e8.txt`

Agent report (verbatim tail of failing run):

```
## Report

**Task outcome: Failed — the icon could not be inserted.**

Here's what I did and found:

1. **insert_icon attempts (all failed):** I called `insert_icon` with `name: 'mdi:home'`, `size: 48` — it returned `{"error": "Failed to fetch"}`. I retried multiple times using both the `name` shorthand and the `names` array form, and with an explicit `color` parameter. Every attempt returned the same `Failed to fetch` error.

2. **Diagnosis:** I tested a different icon set (`lucide:home`) to rule out a problem with the specific icon name — it failed with the identical error. This indicates a general network failure: the `insert_icon` tool needs to fetch icon data from an external source (e.g., the Iconify API), which is unreachable from this sandboxed environment. The tool's docs mention icons being "cached by fetch_icons," but no `fetch_icons` tool is available in my toolset to pre-cache the icon and work around the network block.

3. **viewport_zoom_to_fit:** Called as instructed, but it returned `{"error": "No valid nodes found"}` — expected, since no node was ever created.

4. **Verification:** `find_nodes` (both unfiltered and searching for "home") returned `count: 0` — the document is completely empty. `get_node` on root-style IDs also found nothing. This confirms that no icon node (full or partial) exists on the canvas.

**Conclusion:** The requested `mdi:home` icon at size 48 was never inserted. The blocker is an external network fetch failure in the `insert_icon` tool ("Failed to fetch" on every attempt), with no available caching tool to bypass it, leaving the canvas empty and nothing for `viewport_zoom_to_fit` to target.

verdict: not-approve
```
