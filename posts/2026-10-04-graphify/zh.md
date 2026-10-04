graphify 把文件夹里的代码、文档、图片和视频变成一张知识图。助手之后查图，不再 grep。它是技能（`/graphify .`），底层是 Python 库。

1. **扫描**：`detect()` 按类型分文件。SHA256 缓存跳过没变的文件。
2. **抽取**，分三遍。代码用 tree-sitter 在本地解析，不用 LLM。音视频（video 包）用 faster-whisper 在本地转写。文档、图片和转写稿交给并行的 LLM 子代理，只有这一遍花 token。每条边标 `EXTRACTED`（原文写明）、`INFERRED`（带分数）或 `AMBIGUOUS`（留给人看）。
3. **建图、分群**：合成一张 NetworkX 图。Leiden 按边密度分社区（leiden 包或 Louvain），不用嵌入和向量库。再找核心节点和跨模块意外连接。
4. **输出**到 `graphify-out/`：`graph.json`、可点的 `graph.html`、写要点的 `GRAPH_REPORT.md`。Obsidian、wiki、SVG、GraphML、Cypher 导出可选。

![](use.svg)

`graphify claude install` 加一段 CLAUDE.md 说明和一个 PreToolUse 钩子。搜索或读文件前，钩子提醒先用 `graphify query`。没有钩子的平台改用 `AGENTS.md` 等说明文件。查图走命令行（`query`、`path`、`explain`）或 MCP 服务端，一个人用 stdio，团队用 HTTP。拿回的是一小块子图，不是原文件。

`graphify hook install` 保持图最新。提交和切分支时后台重建代码部分，不花 API 钱。`git pull` 后跑 `graphify update .`。文档变了跑 `/graphify --update`。

在 52 个文件的混合语料上，每次查询比直接读文件少用 71.5 倍 token；6 个文件时没省。
