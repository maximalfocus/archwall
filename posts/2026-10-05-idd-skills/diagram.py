"""idd-skills overview: plan, build one issue, land, finish; the loop runs one issue at a time.
Drawn from maximalfocus/idd-skills at commit f905928 (README.md, CONSTITUTION.md, skills/*/SKILL.md).
Run: python3 diagram.py

Snake order: 1 plan (top left) -> 2 build one issue (top right) -> 3 land (bottom right)
-> 4 finish (bottom left); a dashed arrow from land back to plan is the next round."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-skills overview",
            "In: your product idea, or code you already have. "
            "1 Plan: /idd-plan writes the product contract from an idea or from existing code into a private "
            "PRD repository holding PRD.md and PROGRESS.md, then picks one next issue in dependency order. "
            "2 Build one issue: /idd-issue files it after a duplicate search, and /idd-implement makes a branch, "
            "tests the change and opens a pull request into dev; it never merges, which is /idd-land's job. "
            "An optional review with /peerreview, a separate skill, can come before landing. "
            "3 Land: /idd-land checks the pull request and squash-merges it into dev, the issue is closed and the "
            "branch deleted, and the tracker update goes into a batch pull request in the PRD repository. "
            "Then the next round starts at plan again; /idd-auto runs these rounds by itself. "
            "4 Finish, once every issue has landed: /idd-acceptance tests the whole product end to end; "
            "/idd-promote, whenever you choose, moves dev to main with one merge commit, and the optional "
            "/idd-publish makes the code public while the PRD stays private. "
            "/idd routes any request to its phase, and /idd-evolve improves the method itself.")

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


d.pill(L, 16, W, 48, "In: your product idea, or code you already have")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Plan", 1)
column(L, T1, [("/idd-plan|from an idea, or from existing code", "plan"),
               ("Private PRD repo|PRD.md · PROGRESS.md", "write"),
               ("One next issue|in dependency order", "plan")])

d.group(R, T1, W, H1, "Build one issue", 2)
column(R, T1, [("/idd-issue|files it, after a duplicate search", "write"),
               ("/idd-implement|branch, tests, PR into dev", "coding"),
               ("Never merges|that is /idd-land's job", "review")])
notes(R, T1, H1, "Optional review before landing:", "/peerreview, a separate skill")

d.group(R, T2, W, H2, "Land", 3)
column(R, T2, [("/idd-land|checks, then squash into dev", "review"),
               ("Issue closed|branch deleted", "data"),
               ("Tracker update|batch PR in the PRD repo", "write")])

d.group(L, T2, W, H2, "Finish", 4)
column(L, T2, [("/idd-acceptance|the whole product, end to end", "critic"),
               ("/idd-promote, when you choose|dev → main, one merge commit", "write"),
               ("/idd-publish, optional|code public, PRD stays private", "review")])

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="next issue", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="PR", at=(R + 456, T1 + H1 + 24))
d.arrow(f"M{R + 120} {T2}V{T1 + H1 + 18}H{L + W / 2}V{T1 + H1 + 2}", back=True,
        label="next round (/idd-auto loops)", at=(522, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + W + 2}", label="all landed", at=(600, T2 + 164))

d.note(600, 888, "/idd routes any request to its phase · /idd-evolve improves the method itself")

d.save(Path(__file__).with_name("diagram.svg"))
