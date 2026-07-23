# DesignPen [MCP tools]: 'search icons' fails QA — 5/5 runs report broken workflow (10094-search-icons-mcp)

Description:
Icon search and insertion is completely broken in the DesignPen/OpenPencil design app because the network path to the Iconify API is unreachable from the environment. Every call to the `search_icons` MCP tool (queries "home", "house", with and without `prefix: "lucide"` and `limit`) returns `{"error": "Failed to fetch"}`, and `insert_icon` fails the same way for `lucide:home`, `mdi:home`, `material-symbols:home`, and `tabler:home` because icon data must be fetched over the network and nothing is cached. As a result no icon can ever be placed on the canvas; local document tools (`find_nodes`, `get_node`, `viewport_zoom_to_fit`) work fine and confirm the document stays empty.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Call the `search_icons` MCP tool with query 'home'.
3. Retry `search_icons` with a `limit` parameter, and again with `prefix: "lucide"` and query 'house' — all attempts fail the same way.
4. Call `insert_icon` directly with a known icon name such as `lucide:home` (or `mdi:home`, `material-symbols:home`, `tabler:home`) at 64px.
5. Call `viewport_zoom_to_fit`.
6. Verify document contents with `find_nodes` (name "home" and unfiltered) and `get_node` on root `0:0`.

Actual Result:

- `search_icons` returns `{"error": "Failed to fetch"}` on every attempt (3 tries with different parameters).
- `insert_icon` returns `{"error": "Failed to fetch"}` for every icon set tried, so no icon is ever placed.
- `viewport_zoom_to_fit` returns `{"error": "No valid nodes found"}` because the canvas is empty.
- `find_nodes` returns 0 nodes and `get_node("0:0")` returns "Node not found" — the document is completely empty.

Expected Result:
`search_icons` with query 'home' should return icon results, and `insert_icon` should place the top result onto the canvas as a 64px node that is visible via `find_nodes`/`get_node` and can be targeted by `viewport_zoom_to_fit`. The Iconify API (or a local mirror/cache) must be reachable from the app environment.

Estimate: M (3 points) — missing/unwired handler or component, scoped to one feature area

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5919f774-6713-4bca-8fc9-979b74fb45e5.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9bf79454-93ee-4d52-b290-82e918c90536.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b0cbfb5f-caec-4822-960e-ad6b2e4d9266.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_bdb3543f-11ed-40ec-93be-e93556c2fef1.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_ecc0aace-bb40-4ebf-9081-377c4ba8fc8e.txt`

Agent report (verbatim tail of failing run):

```
## Report

Here's what happened, step by step:

**1. `search_icons` with query "home" — FAILED**
- Attempt 1: `{"error": "Failed to fetch"}`
- Attempt 2 (retry with limit): `{"error": "Failed to fetch"}`
- Attempt 3 (with `prefix: "lucide"` and extra query "house"): `{"error": "Failed to fetch"}`

The Iconify search API appears unreachable from this environment, so no "top result" was ever obtained.

**2. `insert_icon` fallback attempts at 64px — FAILED**
- `lucide:home` → `{"error": "Failed to fetch"}`
- Batch of `mdi:home`, `material-symbols:home`, `tabler:home` → `{"error": "Failed to fetch"}`

Icon insertion also depends on fetching icon data over the network, and nothing was cached, so no icon could be placed.

**3. `viewport_zoom_to_fit` — FAILED (nothing to fit)**
- Returned `{"error": "No valid nodes found"}` — expected, since nothing was inserted.

**4. Verification with MCP tools — canvas confirmed empty**
- `find_nodes` (name "home"): 0 nodes
- `find_nodes` (no filter, entire document): 0 nodes
- `get_node` on root `0:0`: "Node not found"

**Conclusion:** The document is completely empty. No home icon exists on the canvas because every network-dependent tool call (`search_icons`, `insert_icon`) consistently returned "Failed to fetch". The local document tools (`find_nodes`, `get_node`, `viewport_zoom_to_fit`) responded correctly and confirm that nothing was inserted. The task could not be completed due to what looks like a blocked or broken network path to the Iconify API.

The search endpoint was unreachable ("Failed to fetch" on every attempt), icon insertion failed for the same reason, and as a result no icon was placed and zoom-to-fit had nothing to target.

verdict: not-approve
```
