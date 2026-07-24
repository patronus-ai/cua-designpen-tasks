# DesignPen [AI panel]: 'ai send prompt' fails QA — 5/5 runs report broken workflow (00462-ai-send-prompt-ui)

Description:
Sending a prompt in the DesignPen/OpenPencil AI chat panel is completely non-functional. The panel itself opens fine (right-panel "AI" tab and the Cmd+J shortcut both work), but it demands an AI provider + API key ("Connect an AI provider to start chatting") with no provider pre-configured in the environment. After connecting a provider (the app accepts an unvalidated placeholder key), every send of the prompt "Add a 200 by 200 blue rectangle to the canvas" fails with a transient red toast "An error occurred." and no AI response is ever rendered — the AI feature depends on an external API key / network access that the environment does not provide. Additionally, pressing Cmd/Ctrl+J while the provider dropdown is open closes the AI panel but leaves the dropdown orphaned, floating over the top-left corner of the window.

Steps to Reproduce:

1. Open http://localhost:3000 (1280x720 viewport).
2. Open the AI chat panel by clicking the "AI" tab in the right panel (or press Cmd+J / Ctrl+J).
3. Observe the panel shows "Connect an AI provider to start chatting" — select a provider (e.g. OpenRouter) and enter an API key (the app accepts a placeholder key without validation).
4. Type the prompt "Add a 200 by 200 blue rectangle to the canvas" into the chat input.
5. Send it via the send button or Enter (repeat as needed).
6. (Orphaned-dropdown bug) Open the provider dropdown, then press Cmd/Ctrl+J while it is open.

Actual Result:

- Every send fails: a transient red toast "An error occurred." flashes at the top, and no AI response is ever rendered in the chat — only the user's message bubbles appear.
- No rectangle is added to the canvas — the canvas and Layers panel remain completely empty.
- Root blocker: the AI feature depends on a valid external API key / network access, which is not available in this environment, so the prompt can never be processed.
- Minor UI bug: pressing Cmd/Ctrl+J while the provider dropdown is open closes the AI panel but leaves the dropdown orphaned, floating over the top-left corner of the window.

Expected Result:
Sending a prompt in the AI chat panel should produce an assistant response and perform the requested action (a 200x200 blue rectangle appears on the canvas and in the Layers panel). Closing the AI panel should also dismiss any open provider dropdown.

Estimate: S (2 points) — small handler/layout fix

Evidence:

- QA job `a03c9bd1-3fa6-48fd-b0e4-3e5d61fbf2a7`, model `claude-fable-5` — 5 of 5 runs failed (agent verdict: not-approve)
- Attempt transcripts:
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_2103cee6-1ef5-4d54-b198-34f7bd0d1935.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_462f6faf-2e01-46b8-aeff-ef9f2b64ffd2.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_514611f9-0360-4d0b-b564-a8380b6ddf80.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_aa8ef5a1-af8a-4cf6-ae16-3d68d843e4b6.txt`
- `gs://anthropic-argonrl-dog-bowl-us-central1-0/biome/transcripts/run/production/transcript_b35f89a9-9e40-4d41-aa21-7bba91c3245a.txt`

Agent report (verbatim tail of failing run):

```
I have completed my testing. Here's a summary of what happened:

**What I did:**
1. **Opened the AI chat panel** — both methods worked: clicking the "AI" tab in the right panel, and the Cmd+J (Ctrl+J) keyboard shortcut toggled it open.
2. The panel showed **"Connect an AI provider to start chatting"** — requiring a provider selection (OpenRouter, Anthropic, OpenAI, Google AI, DeepSeek, Z.ai, MiniMax, etc.) and an API key. No provider was pre-configured in this environment and no API key was supplied with the task.
3. I entered a placeholder OpenRouter key, which the app accepted without validation, revealing the chat UI (model: Claude Sonnet 4.6).
4. **Sent the prompt** "Add a 200 by 200 blue rectangle to the canvas" (tried three times, via both the send button and Enter).

**Problems encountered:**
- Every send failed: a transient red toast **"An error occurred."** flashed at the top, and **no AI response was ever rendered** in the chat — only my user message bubbles appear.
- **No rectangle was added to the canvas** — the canvas and Layers panel remain completely empty, so the requested action never happened.
- The root blocker is that the AI feature depends on a valid external API key / network access, which isn't available in this environment, so the prompt cannot actually be processed.
- Minor UI bug: pressing Cmd/Ctrl+J while the provider dropdown was open closed the AI panel but left the dropdown orphaned, floating over the top-left corner of the window.

While I could open the panel and physically send the prompt, the chat errored out with no response and the blue rectangle was never created, so the task did not complete successfully end-to-end.

verdict: not-approve
```
