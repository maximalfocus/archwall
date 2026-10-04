Pi is a small coding agent for the terminal. It ships with four tools; you add the rest with extensions.

1. **Interfaces**: terminal UI, print or JSON mode, RPC over JSONL, and a TypeScript SDK. All share one agent and session.
2. **Build the request**: the system prompt plus context files, the active session branch, the tools (`read`, `bash`, `edit`, `write` by default) and short skill descriptions. A skill's full text loads only when needed. Extensions are TypeScript modules in the same process. They add tools, commands, providers and UI, and can change the context.
3. **Loop** (`pi-agent-core`): call the model, get back text and tool calls, run the tools (in parallel by default), record the results, go again. No tool calls: the run ends. A steering message goes in after this turn, a follow-up after the whole run.
4. **pi-ai**: one API over many providers: Anthropic, OpenAI, Google, Bedrock, OpenRouter or any OpenAI-compatible server. `/login` takes a key or a subscription.

![](session.svg)

A session is one JSONL file. Each entry stores its parent's id, so it is a tree. Only the active branch, root to current entry, goes to the model. `/tree` jumps back and starts a new branch; the old one stays. When the context fills up, compaction writes a summary that replaces older messages. The originals stay in the file. `/fork` and `/clone` start a new file.

Pi has no permission system. Tools run with your account's rights, so use a container if you want isolation.
