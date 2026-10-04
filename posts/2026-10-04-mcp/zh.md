AI 应用想读你的文件、查数据库、提一个 Sentry issue。MCP 是一个统一插口，不用每个工具单独接。

1. **宿主**：AI 应用本身，比如 Claude Code、VS Code。每接一个服务端，就开一个 MCP 客户端，各管一条连接。宿主把所有服务端的工具合成一张表给模型，模型要调哪个，就转给对应的客户端。
2. **传输**：本地服务端在同一台机器上，走 stdio，一般只服务一个客户端。远程服务端走 Streamable HTTP（POST，可选 SSE 推流），服务很多客户端，推荐用 OAuth 拿令牌。两种都走同样的 JSON-RPC 2.0 消息，双向：请求过去，结果和通知回来。
3. **服务端**：提供三样东西。模型能调用的工具、应用能读的资源、用户能复用的提示词。客户端先列出来（`tools/list`），再用 `tools/call`、`resources/read`、`prompts/get`。
4. **数据层**：`2026-07-28` 版里每个请求自成一体，在 `_meta` 里带上协议版本和客户端能力，服务端不记会话。`server/discover` 告诉你服务端支持什么。服务端要用户补信息，就发 `elicitation/create`。想知道变化，客户端开一个 `subscriptions/listen`，收 `list_changed` 通知。

MCP 只管传上下文。模型怎么用、上下文怎么用，是应用自己的事。
