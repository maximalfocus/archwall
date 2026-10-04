Pi is a small coding agent for the terminal. It ships with four tools; extensions add the rest.

1. **Interfaces**: terminal UI, print or JSON mode, RPC over JSONL, and a TypeScript SDK. All share one agent and session.
2. **Build the request**: the system prompt plus context files, the active session branch, the tools (`read`, `bash`, `edit`, `write` by default) and short skill descriptions. Extensions are TypeScript modules in the same process. They add tools, commands and UI, and can change the context.
3. **Loop** (`pi-agent-core`): call the model, get back text and tool calls, run the tools (in parallel by default), record the results, go again. No tool calls: the run ends.
4. **pi-ai**: one API over many providers: Anthropic, OpenAI, Google, Bedrock, OpenRouter or any OpenAI-compatible server.

![](session.svg)

A session is one JSONL file. Each entry stores its parent's id, so it is a tree. Only the active branch goes to the model. `/tree` jumps back and starts a new branch; the old one stays. When the context fills up, compaction writes a summary that replaces older messages. `/fork` and `/clone` start a new file.

![](mcp.svg)

MCP servers go in `mcp.json`. Pi talks to them with its own client, over stdio or Streamable HTTP. By default the model doesn't see MCP tools; it writes a sandboxed script that calls them and gets back only the output. `tool_search` or `direct` exposure are the other ways in. Calls go through the built-in tools' pipeline.

Pi has no permission system. Tools run with your account's rights, so use a container if you want isolation.
