"""Branches and who may change them: dev, main, the PRD's main, and the rules GitHub enforces.
Drawn from maximalfocus/idd-skills at commit f905928 (skills/idd-plan/references/conventions.md,
skills/idd-plan/scripts/protect-main.sh, skills/idd-plan/scripts/progress-pr.sh guard,
skills/idd-promote/SKILL.md, skills/idd-promote/scripts/promote.sh, CONSTITUTION.md Article 6).
Run: python3 branches.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-skills branches",
            "Delivery phases start with protect-main.sh ensure. "
            "1 dev, the integration branch: one issue/<N>-<slug> branch per issue; dev is the default branch "
            "every issue pull request targets; squash only, one commit per issue pull request; "
            "linear history, no force-push, no deletion. "
            "2 main, the release branch: changed only by the optional /idd-promote, one dev to main pull request "
            "merged as a merge commit so main never drifts from dev, and only when GitHub reports it clean; the "
            "--open-only flag waits for review. Promoting is not deploying: nothing is hosted or published. "
            "3 The PRD repository has one branch, main: the tracker changes through a progress/batch pull "
            "request merged at milestones, the contract through your own docs(prd) pull request on a prd/<slug> "
            "branch, and a local pre-push hook refuses a direct push. It never uses dev, and the first commit at "
            "bootstrap is its only direct push. "
            "4 Set up by protect-main.sh: a pull request is required, with no bypass and review threads resolved. "
            "On a private repository only the merge settings apply, and the rules are applied once it is public. A "
            "line Integration-branch: main opts a repository out of dev. Protection is set at bootstrap and checked "
            "before every landing. Names are rules too: the pull request title equals the issue title, commit "
            "subjects are typed, and added lines stay within 100 characters.")

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


d.pill(L, 16, W, 48, "Delivery phases start with protect-main.sh ensure")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "dev: integration", 1)
column(L, T1, [("issue/<N>-<slug>|one branch per issue", "data"),
               ("Default branch|every issue PR targets it", "data"),
               ("Squash only|one commit per issue PR", "review"),
               ("Linear history|no force-push, no deletion", "review")])

d.group(R, T1, W, H1, "main: release", 2)
column(R, T1, [("Only /idd-promote|optional, one dev → main PR", "write"),
               ("Merge commit|so main never drifts from dev", "write"),
               ("Only when CLEAN|flag --open-only waits for review", "review")])
notes(R, T1, H1, "Promoting is not deploying:", "nothing is hosted or published")

d.group(R, T2, W, H2, "PRD repo: main only", 3)
column(R, T2, [("Tracker|progress/batch PR, merged at milestones", "data"),
               ("Contract changes|your own docs(prd) PR on prd/<slug>", "data"),
               ("Local pre-push hook|refuses a direct push", "review")])
notes(R, T2, H2, "Never uses dev. Bootstrap's first", "commit is its only direct push")

d.group(L, T2, W, H2, "Set up by protect-main.sh", 4)
column(L, T2, [("PR required, no bypass|review threads resolved", "review"),
               ("Private repo: settings only|rules applied once public", "review"),
               ("Opt out of dev with a line|Integration-branch: main", "data")])
notes(L, T2, H2, "Set at bootstrap,", "checked before every landing")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="promote", at=(600, T1 + 188))

d.note(600, 888, "Names are rules too: PR title = issue title, typed commit subjects, lines ≤ 100 chars")

d.save(Path(__file__).with_name("branches.svg"))
