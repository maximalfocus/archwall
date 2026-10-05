graphify 把文件夹里的代码、文档、论文、图片和视频变成一张知识图。助手查图，不再 grep。它是技能（`/graphify .`），底层是 Python 库。

**1. 读文件夹。** `detect()` 跳过忽略的文件、构建产物和密钥，再按类型分。

![](scan.svg)

**2. 抽事实。** 代码用 tree-sitter 在本机解析，不用 LLM，不花钱。第二遍连起跨文件调用。

![](code.svg)

音视频在本机转写（video 包）。文档、论文、图片和转写稿分批并行交给 LLM，只有这遍花 token。SHA256 缓存跳过没变的文件。

![](media.svg)

每条边标明把握：`EXTRACTED`（原文写明）、`INFERRED`（带分推断）或 `AMBIGUOUS`（待人核对）。

![](model.svg)

**3. 建图。** 合成一张 NetworkX 图并去重。Leiden（leiden 包，否则 Louvain）按连接分社区，不用嵌入和向量库。报告列出核心节点、意外连接和可问的问题。

![](cluster.svg)

**4. 用起来。** `graphify claude install` 加 CLAUDE.md 说明和钩子，助手搜索或读文件前先被提醒用 `graphify query`。命令行或 MCP 服务端（mcp 包）回一小块子图。

![](use.svg)

`graphify hook install` 让提交和切分支免费重建代码部分。`git pull` 后跑 `graphify update .`。

![](current.svg)

代码不出本机。文档、图片和转写稿交给你选的模型。

![](privacy.svg)

周边工具管多仓库、PR 和工作记忆。

![](more.svg)

52 个混合文件上，查询比读文件省 71.5 倍 token；6 个文件时没省。
