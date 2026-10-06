idd-skills 是十个技能，让 AI 编程助手一次做一个 GitHub issue，把软件做出来。固定的 git 和 GitHub 步骤归脚本。

**工具包**在 Claude Code、Codex、Pi 或 OpenCode 里跑。

![](package.svg)

**两个仓库。** 代码在 `{project}`，需求和进度在私有的 `{project}-prd`。

![](repos.svg)

**分支。** issue 的 PR 压缩合并进 `dev`。`main` 只靠可选的 `/idd-promote` 用合并提交推进。

![](branches.svg)

**一个入口。** `/idd` 把一个请求交给一个阶段。合并、公开这类大事，你点名才做。

![](router.svg)

**规划。** `/idd-plan` 从想法或现有代码写 PRD，再挑下一个 issue。

![](plan.svg)

**PRD** 有字数上限。验证过的切片并回需求，PRD 不会越写越长。合同太大就分上下文。

![](contract.svg)

![](contexts.svg)

**建 issue。** `/idd-issue` 先查重，再建 issue。

![](issue.svg)

**实现。** `/idd-implement` 改动最小，在真正运行的地方测，再开 PR，从不合并。

![](implement.svg)

**落地。** `/idd-land` 检查 PR，压缩合并，关 issue，删分支。

![](land.svg)

**进度。** 每次落地更新进一个批量 PR，到里程碑才合并。

![](progress.svg)

**自动。** `/idd-auto` 反复规划、建 issue、实现、落地，直到 PRD 做完再验收。检查一红就停。

![](auto.svg)

**验收。** `/idd-acceptance` 在用户用的地方测成品：浏览器、API、命令行或容器。

![](acceptance.svg)

**公开。** `/idd-publish` 扫遍历史，查密钥和私有名称，再只公开代码。

![](publish.svg)

**进化。** `/idd-evolve` 只为证明过的教训改方法，走评审过的 PR。没通过的不留痕迹。

![](evolve.svg)
