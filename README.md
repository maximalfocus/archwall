# archwall

一图一架构。首页是架构图墙，每张图链接到一篇不超过 300 字的中英双语短文。
One diagram, one architecture: a wall of vector diagrams, each linking to a short bilingual note.

- 静态站点，`python3 build.py` 生成到 `_site/`（只用 Python 标准库，3.12+）；`python3 build.py --serve` 本地预览。
- 推送到 `main` 后由 GitHub Actions 部署到 GitHub Pages（Settings → Pages → Source 选 GitHub Actions）。
- 首页每页 50 篇，带搜索（标题、标签、正文，中英都搜）；右下角悬浮按钮切换中 / EN。

## 一篇文章 / A post

`posts/<YYYY-MM-DD-slug>/`：

| 文件 | 内容 |
|---|---|
| `meta.toml` | `title_zh`、`title_en`、`date`、`tags`、`figure`、`alt_zh`、`alt_en`、可选 `source` |
| `zh.md` / `en.md` | 正文，各不超过 300 字 / 词（超了构建会警告） |
| `diagram.py` → `diagram.svg` | 用 `tools/archdiagram.py` 画的矢量图，全站一个样式；首页和文章用同一张 |
| 更多图（可选） | 一张图说不全时，在 `meta.toml` 里加 `[[figures]]`（`file`、`alt_zh`、`alt_en`，可选 `caption_zh`、`caption_en`），正文单起一行 `![](loop.svg)` 放到那段旁边；没放进正文的排在正文后面。首页只用第一张 |

## 发文流程 / Workflow

1. 每篇文章从 `main` 开新分支 `post/<slug>`，在分支上自由提交。
2. 推送分支、开 PR，审稿、修改，直到定稿。
3. 定稿后 **squash merge** 到 `main`（一篇文章一个提交），删除分支；`main` 自动部署。
