# DesignPen [MCP tools]: 'fetch icons' fails QA — 5/5 runs report broken workflow (10060-fetch-icons-mcp)

Description:
Icon fetching in the DesignPen/OpenPencil design app is completely non-functional in the QA environment: every call to the `fetch_icons` MCP tool (names `['mdi:home']`, size 48) and every call to `insert_icon` (both the single-`name` shorthand and the `names` array form) returns the network error `"Failed to fetch"`. Both tools depend on reaching the external Iconify API, which is unreachable from the sandboxed environment, so the cache is never warmed and no icon node is ever created — the document stays empty (`find_nodes` returns 0 results). Node inspection and viewport tools work fine; the blocker is specifically the external icon fetch.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Call the `fetch_icons` MCP tool with `names: ["mdi:home"]` and `size: 48` to warm the cache.
3. Call `insert_icon` with `mdi:home` at 48px (try both the single-`name` shorthand and the `names` array form).
4. Call `viewport_zoom_to_fit`.
5. Verify with `find_nodes` (by name "home", unfiltered, and filtered by type VECTOR) and `get_node` on the document root.

Actual Result:

- `fetch_icons` fails with `"Failed to fetch"` on every attempt, including retries.
- `insert_icon` fails with the same `"Failed to fetch"` error in both call forms; with the cache never warmed, it attempts its own request to the Iconify API, which also cannot complete.
- `viewport_zoom_to_fit` on the page canvas succeeds but returns zero-size bounds centered at (0, 0), consistent with an empty page.
- `find_nodes` returns 0 results in all queries; `get_node` on the document root shows only an empty "Page 1" canvas with no children — the icon was never inserted.

Expected Result:
`fetch_icons` should successfully warm the icon cache for `mdi:home` at size 48 (the icon source must be reachable from the environment, or served locally), and `insert_icon` should then create a visible icon node on the canvas that verification tools can find.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_290aebfa-553d-4cf9-a6b0-f3e35bf5e7b3.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2e189bd3-613a-4916-ab0d-210018eb9180.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5da9e1ed-0546-41c2-91e7-c29722c01699.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9cf0397f-c8a5-4302-9ed4-686a00cdec43.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ec9a8205-d4ad-4aeb-9be1-dc6443965ed7.txt`

Agent report (verbatim tail of failing run):

```
## Report

Here's what happened during the task:

**1. fetch_icons (warm cache):** Called with `names: ["mdi:home"]` and `size: 48` — **failed** with `"Failed to fetch"`. Retried multiple times (including one final retry at the end); every attempt returned the same network error.

**2. insert_icon:** Called with `mdi:home` at 48px, using both the single-`name` shorthand and the `names` array form — **failed** with the same `"Failed to fetch"` error. Since the cache was never warmed, insert_icon attempted its own network request to the Iconify API, which also could not complete.

**3. viewport_zoom_to_fit:** Since no icon node existed, I targeted the page canvas (`0:2`). The call **succeeded** but returned zero-size bounds centered at (0, 0), consistent with an empty page.

**4. Verification findings:**
- `find_nodes` with name "home" → 0 results
- `find_nodes` with no filter (all nodes) → 0 results
- `find_nodes` filtered by type VECTOR → 0 results
- `get_node` on the document root (`0:1`) shows only an empty "Page 1" canvas (`0:2`) with no children

**Conclusion:** The document is confirmed empty — the `mdi:home` icon was never inserted. The root cause appears to be that the sandboxed environment cannot reach the Iconify API (every icon-fetching call, whether via `fetch_icons` or `insert_icon`, returned `"Failed to fetch"`). The MCP tools for node inspection and viewport control worked fine, but the core objective of the task (inserting the icon) was blocked by the network failure.

The task did not go smoothly: both `fetch_icons` and `insert_icon` consistently failed with `"Failed to fetch"`, so the icon could not be inserted and the canvas remains empty.

verdict: not-approve
```
