# DesignPen [MCP tools]: 'stock photo' fails QA — 5/5 runs report broken workflow (10020-stock-photo-mcp)

Description:
The `stock_photo` MCP tool in DesignPen/OpenPencil always fails in the QA environment because no stock photo provider is configured. Every call (with or without the orientation parameter) returns the error "No stock photo provider configured. Ask the user to add an API key in AI chat settings. Available providers: Pexels, Unsplash." The rest of the workflow is fine — the 400x300 "Photo" rectangle is created, viewport_zoom_to_fit works, and get_node/find_nodes verify it — but the mountain image fill can never be applied, so the rectangle stays plain. Fix requires provisioning a Pexels or Unsplash API key (in AI chat settings) or a mock provider in the environment.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Using MCP tools only, call create_shape to create a 400x300 rectangle named Photo (e.g. at (100,100)).
3. Call stock_photo to search for a photo of mountains and apply it to the Photo rectangle as an image fill (retry with and without the orientation parameter).
4. Call viewport_zoom_to_fit.
5. Verify with get_node on the rectangle and find_nodes.

Actual Result:

- `stock_photo` returns the error "No stock photo provider configured. Ask the user to add an API key in AI chat settings. Available providers: Pexels, Unsplash." — same error on retry, with and without the orientation parameter.
- The rectangle has no mountain image fill; verification shows the plain 400x300 RECTANGLE "Photo" (id 0:3) with no image applied.
- Rectangle creation, viewport_zoom_to_fit (bounds 100, 100, 400x300), and get_node/find_nodes verification all work correctly.

Expected Result:
`stock_photo` should return mountain photo results and apply the selected photo to the Photo rectangle as an image fill; the environment should have a stock photo provider (Pexels or Unsplash API key) configured so the tool is usable.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2867ad76-c706-4a21-a636-7a4ba65a7f9c.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_4f715a29-435b-4386-b178-a2d8ef782f1d.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_9890c74c-f9ef-4f23-a5dd-37f7be0e4837.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_c913b7ec-6a6b-4f06-8680-684c1ba67925.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_e8abab58-4ec2-447f-90b4-bb0106f9dd9d.txt`

Agent report (verbatim tail of failing run):

```
## Report

Here's what I did and what I found during verification:

**Completed successfully:**
1. ✅ **Rectangle created** — A 400×300 RECTANGLE named "Photo" was created at (100, 100) and assigned ID `0:3`.
2. ✅ **Viewport zoomed** — `viewport_zoom_to_fit` centered the view on the rectangle (center at 300, 250; bounds 100, 100, 400×300).
3. ✅ **Verification** — `get_node("0:3")` confirms the node exists as a RECTANGLE named "Photo" with exactly 400×300 dimensions, and `find_nodes` confirms it is the single matching "Photo" rectangle on the canvas.

**Failed:**
- ❌ **Stock photo application** — The `stock_photo` tool returned the error: *"No stock photo provider configured. Ask the user to add an API key in AI chat settings. Available providers: Pexels, Unsplash."* I retried (with and without the orientation parameter) and got the same error both times. As a result, the rectangle has **no mountain image fill** — the verification output shows the plain rectangle with no image applied. To fix this, an API key for Pexels or Unsplash needs to be added in the AI chat settings.

**What went wrong:** The environment has no stock photo provider configured (missing Pexels/Unsplash API key), so the required image fill step could not be completed despite the rectangle, zoom, and verification steps all working correctly.

verdict: not-approve
```
