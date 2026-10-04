AI 应用想读你的文件、查数据库、提一个 Sentry issue。MCP 是一个统一插口，不用每个工具单独接。

1. **宿主**：AI 应用，比如 Claude Code、VS Code。它管着模型，每接一个服务端就开一个 MCP 客户端。它把所有工具合成一张表给模型，调用时转给对应的客户端。MCP 本身跑在客户端和服务端之间。
2. **连接**：每个客户端一条，分两层。
   - 外层是**传输层**，好比管子。本地服务端走 stdio，由客户端启动，一般只服务一个客户端。远程服务端走 Streamable HTTP（POST，回 JSON 或 SSE），服务多个客户端，令牌推荐用 OAuth。
   - 内层是**数据层**，就是消息：JSON-RPC 2.0，换什么管子都一样。请求和通知过去，结果和通知回来。`2026-07-28` 版里每个请求自成一体，`_meta` 带上协议版本和客户端能力，服务端不记会话。`server/discover` 查服务端支持什么。服务端要用户补信息（`elicitation/create`），客户端问完再重发。`subscriptions/listen` 推送 `list_changed` 通知。
3. **服务端**：提供三样：模型调用的工具、应用读取的资源、用户选用的提示词。先用 `tools/list` 列出，再用 `tools/call`、`resources/read`、`prompts/get`。

MCP 只管传上下文，怎么用是应用自己的事。
