idd-skills is ten skills that have an AI coding agent build software one GitHub issue at a time. Scripts do the fixed git and GitHub steps.

**The kit** runs in Claude Code, Codex, Pi or OpenCode.

![](package.svg)

**Two repos.** Code lives in `{project}`. Requirements and the tracker live in a private `{project}-prd`.

![](repos.svg)

**Branches.** Issue PRs squash into `dev`. `main` moves only through the optional `/idd-promote`, as one merge commit.

![](branches.svg)

**One way in.** `/idd` sends one request to the phase that owns it. Merging, publishing and other big steps run only when you name them.

![](router.svg)

**Plan.** `/idd-plan` writes the PRD from your idea or from existing code, then picks one next issue.

![](plan.svg)

**The PRD** has word budgets. A validated slice folds into its requirement, so the PRD stays small. A product too large for one coherent contract splits its PRD into contexts.

![](contract.svg)

![](contexts.svg)

**Issue.** `/idd-issue` files one issue, after a duplicate search.

![](issue.svg)

**Implement.** `/idd-implement` makes the smallest change, tests it where it really runs, and opens a PR. It never merges.

![](implement.svg)

**Land.** `/idd-land` checks the PR, squash-merges it, closes the issue and deletes the branch.

![](land.svg)

**Progress.** Each landing adds a tracker update to one batch PR, merged only at milestones.

![](progress.svg)

**Auto.** `/idd-auto` repeats plan, issue, implement and land until the PRD is done, then runs acceptance. A red check stops it.

![](auto.svg)

**Acceptance.** `/idd-acceptance` tests the finished product the way people reach it: browser, API, CLI or container.

![](acceptance.svg)

**Publish.** `/idd-publish` scans the whole history for secrets and private names, then makes only the code repo public.

![](publish.svg)

**Evolve.** `/idd-evolve` changes the method only for proven lessons, through a reviewed PR. Rejected ideas leave no trace.

![](evolve.svg)
