# DesignPen [AI panel]: 'ai acp agent' fails QA — 5/5 runs report broken workflow (00456-ai-acp-agent-ui)

Description:
In the DesignPen/OpenPencil design app, the AI chat panel's provider selector has no "acp:" provider entry, so connecting the assistant to a locally running coding agent is impossible in this build. Opening the AI panel works (right-panel AI tab or Ctrl/Cmd+J shows "Connect an AI provider to start chatting"), but the selector contains exactly 9 options — OpenRouter, Anthropic, OpenAI, Google AI, DeepSeek, Z.ai, MiniMax, OpenAI-compatible, Anthropic-compatible — none prefixed with "acp:", verified via full accessibility-tree reads, dropdown scrolling, keyboard typeahead, and page reloads. The "-compatible" options only offer HTTP API config fields (Base URL / Model ID / API key), not ACP; the Code tab's MCP "Connect to AI agent" button is grayed out and unresponsive; and no ACP/local-agent options exist in the menus or Preferences. Because no acp: provider can be selected, the downstream permission dialog is never reached.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the AI chat panel via the right panel's AI tab (Design / Code / AI tablist) or press Ctrl/Cmd+J.
3. Open the provider selector in the "Connect an AI provider to start chatting" view.
4. Look for an "acp:" provider entry to connect a locally running coding agent (scroll the dropdown, use keyboard typeahead, reload the page and re-check).
5. Attempt to select the acp: provider and approve the agent's permission dialog.

Actual Result:
- The provider selector contains only 9 options: OpenRouter, Anthropic, OpenAI, Google AI, DeepSeek, Z.ai, MiniMax, OpenAI-compatible, and Anthropic-compatible — there is no "acp:" provider entry (confirmed via full accessibility-tree reads including off-screen items, scrolling, typeahead, and page reload with wait for async discovery).
- The "-compatible" options only offer Base URL / Model ID / API key fields (HTTP API config, not ACP).
- The Code tab's MCP section has a "Connect to AI agent" button, but it is grayed out/disabled and clicking it does nothing (and it is MCP, not the acp provider flow); the main menu/Preferences contain no ACP or local-agent options.
- Since no acp: provider can be selected, no connection to a local coding agent is attempted and no permission dialog ever appears.

Expected Result:
The AI chat panel's provider selector should include an "acp:" provider entry for connecting the assistant to a locally running coding agent; selecting it should trigger the agent connection and show a permission dialog the user can approve so the agent can work on the file.

Estimate: M (3 points) — scoped feature fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2444214c-d1bd-4e54-a326-8d16c92eca2d.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_398d6ca7-bcc8-4115-b90d-729537e0f988.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_5b4c696b-8904-4e7c-997b-47c528ca64af.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_a8f2354d-10be-4027-a720-b29b85e30336.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_f2331a54-c4b4-41d9-9dc7-c3e7c5c56d21.txt`

Agent report (verbatim tail of failing run):

```
The provider selector is restored to its default "OpenRouter" state. My testing is complete.

**Summary of what I did and found:**

1. **Opening the AI chat panel — worked.** Pressing Ctrl+J (the Cmd+J equivalent) opened the AI tab in the right panel, showing the "Connect an AI provider to start chatting" view. The AI tab is also reachable from the right-panel tablist (Design / Code / AI).

2. **Choosing an acp: provider — blocked.** The provider selector contains only these 9 options: OpenRouter, Anthropic, OpenAI, Google AI, DeepSeek, Z.ai, MiniMax, OpenAI-compatible, and Anthropic-compatible. There is **no "acp:" provider entry** for connecting to a locally running coding agent. I verified this thoroughly:
   - Read the full accessibility tree of the dropdown (including off-screen items) — exactly 9 options, none prefixed with "acp:".
   - Scrolled within the dropdown, used keyboard typeahead ("a" only matched "Anthropic").
   - Reloaded the page and waited (in case local agent discovery is asynchronous) — the list never changed.
   - Checked the "-compatible" options — they only offer Base URL / Model ID / API key fields (HTTP API config, not ACP).
   - Checked other surfaces: the Code tab's MCP section has a "Connect to AI agent" button, but it's grayed out/disabled and clicking it does nothing (and it's MCP, not the acp provider flow). The main menu/Preferences contain no ACP or local-agent options.

3. **Approving the permission dialog — never reached.** Since no acp: provider could be selected, no connection to a local coding agent was attempted and no permission dialog ever appeared.

The core flow described in the task (select an acp: provider → approve the agent's permission request) cannot be completed in this build: the acp: provider option is missing from the AI chat panel's provider selector, so connecting the assistant to a locally running coding agent is impossible.

verdict: not-approve
```
