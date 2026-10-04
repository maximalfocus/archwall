---
name: archwall
description: >-
  Write an archwall post from a source (repo, paper, doc URL): research it, draw the diagram(s) with
  tools/archdiagram.py, write the zh/en body, open the PR. Also lands reviewed PRs in order. Use when
  the user gives a project or link and asks for its architecture diagram (e.g. "pi agent 架构图 <url>"),
  or says land / merge / 合并 for archwall PRs, or changes the site's tooling or diagram style.
argument-hint: "<source URL or name> | land <PR#> [PR#...]"
---

# archwall

Rules for the content (length, voice, diagram look, 1200 x 900, multiple figures) live in the repo's
`CLAUDE.md` and the docstring of `tools/archdiagram.py`. Read both first; this file is only the steps.

## New post: `/archwall <source>`

1. **Workspace.** `git fetch`, then cut `post/<slug>` from `origin/main`. If the main checkout is on
   another branch or has changes that aren't yours, don't touch them: `git worktree add ../archwall-<slug>
   -b post/<slug> origin/main` and work there.
2. **Research.** Clone repos shallowly into the scratchpad. Read the project's own architecture or
   "how it works" docs and the package manifests before code. Note the commit hash: claims and the
   diagram docstring cite it. Every number and claim must be in the source.
   - Read the manifest's optional parts too (`optional-dependencies`, extras, feature flags). A feature
     that needs an extra, a flag or a config setting is labelled as such, in the text and the picture.
   - Docs simplify. Where the docs and the code disagree, the code wins; if you can't settle it, leave
     the claim out (graphify: the docs said 25 languages in one place and about 40 in another).
3. **Diagram.** `posts/<YYYY-MM-DD-slug>/diagram.py` → `diagram.svg`, the home-page card. If one picture
   can't hold it (e.g. overview + a data model + an integration), add `<name>.py` → `<name>.svg` and list
   them under `[[figures]]` in `meta.toml`; place each with `![](<name>.svg)` in both bodies.
4. **Look at it.** `python3 build.py && python3 tools/render.py posts/<slug>`, then Read every PNG in
   `_render/<slug>/`. Fix overflow, overlap, arrows through text, notes that should be arrow labels,
   colours that break the role meanings. Then check what the picture claims, against the code: what
   each arrow carries, which stage each part sits in, and that every stage really produces what the
   next one takes. Repeat until clean; a diagram nobody looked at is not done.
5. **Text.** `meta.toml` (titles, date, tags, figure, alt_zh/alt_en, source; captions for extra
   figures), `en.md`, `zh.md`: same content, plain voice. `build.py` prints each post's counts and warns past
   300 words / 300 hanzi; no warning allowed. Quote its counts in the PR, not your own. The diagrams carry few words, so the details go here.
6. **Commit, push, PR.** The repo is maximalfocus/archwall and gh's active account is usually another
   one: `gh auth switch -u maximalfocus`, create the PR (what the diagrams show, source + commit,
   word counts), switch back. The git hooks rebuild the preview on commit; give the owner the link
   once for a new post: `http://100.73.23.11:8765/post-<slug>/p/<slug>/`. Check
   `~/personal/archwall-preview/.build.log` if it doesn't show.
7. Revisions go on the same branch. Never merge without the owner's go-ahead.

Big batches (several diagrams to redraw) can fan out to parallel agents, one per diagram file; they
must not commit, and you look at their PNGs before committing.

## Land: `/archwall land <PR#> [PR#...]`

Only on the owner's explicit go-ahead, in the order given. With gh switched to maximalfocus:

1. For each PR: if its base is not `main`, first `gh pr edit <n> --base main`, then rebase its branch
   onto `origin/main` past the already-merged commits (`git rebase --onto origin/main <old base tip>`)
   and force-push. Do this **before** the base branch is deleted: GitHub closes a PR whose base branch
   disappears, and a closed PR whose head was force-pushed can't be reopened.
2. `gh pr merge <n> --squash --delete-branch` (one commit per post on `main`). Check the PR now shows
   only its own files (`gh pr view <n> --json files`) before merging.
3. After the last one: switch gh back, `git switch main && git pull`, remove worktrees of merged
   branches, wait for the "Deploy to GitHub Pages" run (`gh run list --limit 1`) to succeed, and curl
   the live post at https://maximalfocus.github.io/archwall/p/<slug>/.

## Site changes

Tooling or style changes (not a post) use `site/<topic>` and the same PR → land flow. A change to
`tools/archdiagram.py` that alters the look means re-rendering every diagram (`python3 posts/*/*.py`),
looking at each, and redrawing the ones that break, in the same PR.
