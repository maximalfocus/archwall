An AI app wants to read your files, query a database, open a Sentry issue. MCP is the one plug for all of them, so each tool doesn't need its own integration.

1. **Host**: the AI app, like Claude Code or VS Code. It holds the model and makes one MCP client per server. It merges every server's tools into one list for the model and routes each call to the right client. MCP itself runs between each client and its server.
2. **Connection**: one per client, with two layers.
   - Outside, the **transport layer** is the pipe. A local server runs over stdio: the client starts it, and it usually serves one client. A remote server uses Streamable HTTP (POST, replies as JSON or SSE) and serves many; OAuth is recommended for tokens.
   - Inside, the **data layer** is the messages: JSON-RPC 2.0, the same on any pipe. Requests and notifications go out, results and notifications come back. In version `2026-07-28` every request stands alone: it carries the protocol version and client capabilities in `_meta`, so the server keeps no session. `server/discover` returns what the server supports. If a server needs the user's input (`elicitation/create`), the client asks the user and retries. `subscriptions/listen` streams `list_changed` notices.
3. **Server**: offers three things: tools the model calls, resources the app reads, prompts the user picks. The client lists them with `tools/list` first, then calls `tools/call`, `resources/read` or `prompts/get`.

MCP only moves context; how to use it is up to the app.
