AI 应用想读文件、查数据库、看 Sentry。MCP 是统一插口，不用每个工具单独接。本文按 `2026-07-28` 版协议。

**谁参与。**宿主是 AI 应用，如 Claude Code、VS Code。它给每个服务端配一个客户端，管着对话，工具运行前问用户。服务端只见所需。

![](participants.svg)

**两层。**内层数据层是消息：JSON-RPC 2.0，客户端发请求，服务端答。外层传输层是管子。

![](layers.svg)

**一个请求。**每个请求都带协议版本和客户端能力，服务端不记会话。`server/discover` 查它支持什么，然后 `tools/list`、`tools/call`。

![](request.svg)

**服务端提供。**模型调用的工具、应用读取的资源、用户选用的提示词。

![](primitives.svg)

**问用户。**服务端不发请求，只回"需要输入"；客户端问过用户后带答案重发。密码走网页，不走表单。

![](ask.svg)

**获知变化。**客户端用 `subscriptions/listen` 选想听的，如"工具列表变了"。需订阅，尽力送达。

![](updates.svg)

**传输。**本地走 stdio，客户端把它当子进程启动。远程走 Streamable HTTP：每条消息一个 POST，回 JSON 或 SSE 流。

![](transports.svg)

**登录**可选，只用于 HTTP。服务端指明授权服务器，用户在浏览器同意，之后每个请求带令牌。

![](auth.svg)

MCP 只管传上下文，怎么用归应用。
