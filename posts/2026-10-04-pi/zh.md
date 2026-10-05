pi 是终端里的小型开源编程智能体。缺什么功能，自己加。

**总览。** 四种入口：终端界面、打印或 JSON 模式、RPC、SDK，共用一个会话。pi 拼请求，循环调模型和工具，保存对话。pi-ai 内置 42 家模型厂商。

![](packages.svg)

`pi` 命令在 pi-coding-agent 里，基于 pi-agent-core 和 pi-ai。远程会话的包仍是实验版。

![](context.svg)

请求带系统提示词、工具列表和对话。项目的 `.pi` 目录要先信任才加载。技能用到才读全文。

![](loop.svg)

模型回文字和工具调用。pi 逐个检查，默认并行执行，记下结果，再来一轮。中途可以插话。

![](tools.svg)

默认开四个工具：`read`、`bash`、`edit`、`write`。`codemode` 和 `tool-search` 是内置扩展，工具默认关，MCP 需要时自动开。

![](mcp.svg)

MCP 服务端写在 `mcp.json`。默认模型看不到 MCP 工具，而是写沙箱脚本去调，只拿回输出。

![](session.svg)

会话是 JSONL 文件里的一棵树，只有当前分支发给模型。快满时用摘要替掉旧消息。

![](extensions.svg)

扩展是 pi 进程里的 TypeScript，能加工具、命令、厂商和界面。技能、模板和主题不用写代码。

![](providers.svg)

用 `/login` 或 API key 登录。本地模型走 llama.cpp 或 `models.json`。

![](safety.svg)

pi 没有内置权限系统，工具用你账号的权限跑。要隔离就用容器。
