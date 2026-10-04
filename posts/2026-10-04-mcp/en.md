An AI app wants to read your files, query a database, open a Sentry issue. MCP is the one plug for all of them, so each tool doesn't need its own integration.

1. **Host**: the AI app, like Claude Code or VS Code. It makes one MCP client per server, and each client keeps its own connection. The host merges every server's tools into one list for the model and routes each call to the right client.
2. **Transport**: a local server runs on the same machine over stdio, and usually serves one client. A remote server uses Streamable HTTP (POST, with optional SSE for streaming) and serves many; OAuth is the recommended way to get tokens. Both carry the same JSON-RPC 2.0 messages, both ways: requests and notifications go out, results and notifications come back.
3. **Server**: offers three things. Tools the model can call, resources the app can read, prompts the user can reuse. The client lists them first (`tools/list`), then calls `tools/call`, `resources/read` or `prompts/get`.
4. **Data layer**: in version `2026-07-28` every request stands alone. It carries the protocol version and the client's capabilities in `_meta`, so the server keeps no session. `server/discover` returns what the server supports. A server that needs the user's input asks through `elicitation/create`. To hear about changes, the client opens `subscriptions/listen` and gets `list_changed` notices.

MCP only moves context. How the app uses the model and that context is up to the app.
