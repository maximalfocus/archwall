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
   "how it works" docs and the package manifests before code. Note the commit hash: claims and the diagram
   docstring cite it. Every number and claim must be in the source. Read the manifest's optional parts too
   (`optional-dependencies`, extras, feature flags), and check the docs against each other and the code.
3. **Diagrams.** `posts/<YYYY-MM-DD-slug>/diagram.py` → `diagram.svg`, the home-page card: an overview of
   the whole system. One `<name>.py` → `<name>.svg` for every phase, part or concern that a diagram (the
   overview or any other) only names, with no cap on the count, until a non-technical manager could
   explain the architecture from the pictures alone. Check it from the source's side too: list the source's
   own parts (components, scripts, services, config, doc sections) and make sure each is drawn, is detail of
   something drawn, or is left out on purpose; name the ones left out in the PR. List them under `[[figures]]`
   in `meta.toml`; place each with `![](<name>.svg)` in both bodies.
4. **Look at it.** `python3 tools/check.py posts/<slug>` is the post's one gate (/peerreview too): counts,
   figures, fresh SVGs, the layout Chrome measures (text in its box, overlaps, line and note limits, arrows
   through cards or text), and a whole-site build. Fix every failure. Then `python3 build.py && python3
   tools/render.py posts/<slug>` and Read every PNG in `_render/<slug>/` for what only eyes catch: a note that
   should be an arrow label, a colour that breaks its role. Check what each arrow carries, which stage each
   part sits in, and that each stage feeds the next. For each claim the post makes, read its source line; if
   that has a number, default, optional/flag/config status or scope word (only, unless, or else, first, all,
   never), add a row to the PR's `## Claims`: source `path:line` and every place the post says it (card, `.py`
   text, alt_zh, body, caption). No source line: drop the claim. A diagram nobody looked at is not done.
5. **Text.** `meta.toml` (titles, date, tags, figure, alt_zh, source; captions for extra figures; alt_en
   comes from the `.py`), `en.md`, `zh.md`: same content, plain voice, at most 300 words / 300 hanzi.
   Quote the counts check.py prints in the PR, not your own; details go here.
6. **Commit, push, PR.** The repo is maximalfocus/archwall. Run every gh call as `gh-as maximalfocus <args>`
   (never `gh auth switch`: the login is shared); no `gh-as` on PATH: stop and tell the owner. Create the PR
   (what the diagrams show, source + commit, word counts, what was left out on purpose). The git hooks
   rebuild a preview on commit only where `python3 tools/preview.py install` has run ("archwall preview"
   in `$(git rev-parse --git-common-dir)/hooks/post-commit`). There, give the owner the link once for a
   new post: `http://100.73.23.11:8765/post-<branch slug>/p/<post folder>/`, e.g.
   `post-idd-skills/p/2026-10-05-idd-skills/`, and check `~/personal/archwall-preview/.build.log` if it
   doesn't show. Without the hooks, say in the PR that no preview was built.
7. Revisions go on the same branch; after each one (or each /peerreview round), refresh the PR's counts,
   diagram list and `## Claims` rows. Never merge without the owner's go-ahead.

A post with over 6 diagrams, or a big redraw, fans out: one parallel agent per diagram file, no commits;
you look at every PNG and run check.py. Start each new post in a fresh session where possible.

## Land: `/archwall land <PR#> [PR#...]`

Only on the owner's explicit go-ahead, in the order given; every gh call below goes through
`gh-as maximalfocus` (step 6):

1. For each PR: if its base is not `main`, first `gh pr edit <n> --base main`, then rebase its branch
   onto `origin/main` past the already-merged commits (`git rebase --onto origin/main <old base tip>`)
   and force-push. Do this **before** the base branch is deleted: GitHub closes a PR whose base branch
   disappears, and a closed PR whose head was force-pushed can't be reopened.
2. `gh pr merge <n> --squash --delete-branch` (one commit per post on `main`). Check the PR now shows
   only its own files (`gh pr view <n> --json files`) before merging.
3. After the last one: `git switch main && git pull`, remove worktrees of
   merged branches, wait for the "Deploy to GitHub Pages" run (`gh run list --limit 1`) to succeed, and curl
   the live post at https://maximalfocus.github.io/archwall/p/<slug>/.

## Site changes

Tooling or style changes (not a post) use `site/<topic>` and the same PR → land flow.
`SKILL.md`: 80 lines, 110 chars max. `CLAUDE.md`: 40 lines, 130 chars max. Merge or delete before adding.
Name the post or PR that caused a change, in the PR description. A site PR runs `python3 tools/check.py` on
any post first; that also checks the caps. What a script can check goes in `tools/check.py`, not prose;
replace a sentence instead of adding one. If a change alters the look, re-render every diagram (`python3
posts/*/*.py`), look at each, and redraw what breaks, in the same PR.
