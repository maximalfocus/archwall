"""Two repositories per product: the code, and the private product contract next to it.
Drawn from maximalfocus/idd-skills at commit f905928 (README.md, CONSTITUTION.md Article 1,
skills/idd-plan/SKILL.md Orient, skills/idd-plan/scripts/resolve-prd-pair.sh,
skills/idd-auto/SKILL.md Orient, skills/idd-implement/SKILL.md Step 4).
Run: python3 repos.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-skills two repositories",
            "One product, two GitHub repositories, cloned side by side. "
            "1 {project}, the code: code, tests and docs; issues and pull requests, one pull request for each "
            "issue; branches dev, main and issue/<N>-<slug>. It is private when IDD creates it, and /idd-publish "
            "can make it public. "
            "2 {project}-prd, the plan: PRD.md with requirements, slices and non-goals; PROGRESS.md with what is "
            "ready, active or blocked; a single main branch changed by pull request. It is always private. "
            "The PRD side sends the next issue to the code side, and landed work flows back to the tracker. "
            "3 How they find each other: sibling folders such as widget and widget-prd, the same GitHub owner "
            "checked from both origins, or for another owner the local setting git config idd.prdRepo. With no "
            "PRD repository, issues still work and landing skips the tracker. "
            "4 Who is right about what: GitHub about what happened, PRD.md about what is wanted, and PROGRESS.md "
            "is checked evidence, not permission. Commits, issues and pull requests never name the private PRD "
            "repository. For a new product the PRD repository comes first, and /idd-auto can create the "
            "code repository, private.")

L, R, W = 24, 624, 552
T1, H1 = 84, 380
T2, H2 = 500, 364
CW, CH, GAP = 492, 64, 16


def column(x, top, cards, gap=GAP):
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + 64 + i * (CH + gap), lbl, kind, w=CW, h=CH)


def notes(x, top, h, a, b):
    d.note(x + W / 2, top + h - 52, a)
    d.note(x + W / 2, top + h - 26, b)


d.pill(L, 16, 2 * W + 48, 48, "One product, two GitHub repositories, cloned side by side")

d.group(L, T1, W, H1, "{project}: the code", 1)
column(L, T1, [("Code, tests, docs|the product itself", "coding"),
               ("Issues and PRs|one PR for each issue", "write"),
               ("Branches|dev, main, issue/<N>-<slug>", "data")])
notes(L, T1, H1, "Private when IDD creates it;", "/idd-publish can make it public")

d.group(R, T1, W, H1, "{project}-prd: the plan", 2)
column(R, T1, [("PRD.md|requirements, slices, non-goals", "write"),
               ("PROGRESS.md|what's ready, active, blocked", "write"),
               ("One branch, main|changed by pull request", "data")])
notes(R, T1, H1, "Always private:", "never published")

d.group(R, T2, W, H2, "How they find each other", 3)
column(R, T2, [("Sibling folders|widget and widget-prd", "data"),
               ("Same GitHub owner|checked from both origins", "review"),
               ("Another owner?|setting: git config idd.prdRepo", "data")])
notes(R, T2, H2, "No PRD repo: issues still work,", "landing skips the tracker")

d.group(L, T2, W, H2, "Who is right about what", 4)
column(L, T2, [("GitHub|what happened: issues, PRs, merges", "data"),
               ("PRD.md|what is wanted", "write"),
               ("PROGRESS.md|checked evidence, not permission", "write")])
notes(L, T2, H2, "Commits, issues and PRs never", "name the private PRD repo")

d.arrow(f"M{R} {T1 + 150}H{L + W + 2}", label="next issue", at=(600, T1 + 138))
d.arrow(f"M{L + W} {T1 + 260}H{R - 2}", label="landed", at=(600, T1 + 248))

d.note(600, 888, "New product: the PRD repo comes first, and /idd-auto can create the code repo, private")

d.save(Path(__file__).with_name("repos.svg"))
