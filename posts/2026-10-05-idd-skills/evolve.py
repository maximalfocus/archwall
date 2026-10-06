"""/idd-evolve: proven lessons change the method through a reviewed PR; the rest leaves no trace.
Drawn from maximalfocus/idd-skills at commit f905928 (CONSTITUTION.md Articles 2, 3, 5 and 6,
skills/idd-evolve/SKILL.md, skills/idd-evolve/scripts/propose.sh, land-evolution.sh, CONTRIBUTING.md).
Run: python3 evolve.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-evolve",
            "In: evidence from real runs, or a simplify pass. "
            "1 Evidence: post-plan looks at issue order and tracker accuracy; post-create at how an issue was "
            "written; post-issue at one issue's diff, checks and pull request; simplify merges, compresses or "
            "deletes. "
            "2 The gate is the constitution: proven and high value, not already covered, smaller than the "
            "friction it removes and preferring deletion to addition, leaving past issues the same or better by "
            "naming the one it could hurt, and within the size caps of 60 to 160 lines per skill file. "
            "3 Pass: the smallest edit, with validate.sh passing; propose.sh opens a pull request on "
            "evolve/<slug> and never writes main; the maintainer reviews, and land-evolution.sh merges it on "
            "their word. Skills linked to the checkout keep serving main until it lands. "
            "4 Fail: nothing happens, no log and no queue; git history is the only record. New features do not "
            "come this way; they go through the PRD and an issue. One reproduced defect is proof enough, while "
            "advice on behaviour needs several runs.")

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


d.pill(L, 16, W, 48, "In: evidence from real runs, or a simplify pass")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Evidence", 1)
column(L, T1, [("post-plan|issue order, tracker accuracy", "data"),
               ("post-create|how an issue was written", "data"),
               ("post-issue|one issue's diff, checks, PR", "data"),
               ("simplify|merge, compress, delete", "data")])

d.group(R, T1, W, H1, "Gate: the constitution", 2)
column(R, T1, [("Proven and high value|not already covered", "review"),
               ("Smaller than the friction|delete before adding", "review"),
               ("Past issues same or better|name the one it could hurt", "review"),
               ("Size caps|skill files 60 to 160 lines", "review")])

d.group(R, T2, W, H2, "Pass", 3)
column(R, T2, [("Smallest edit|validate.sh passes", "write"),
               ("propose.sh|a PR on evolve/<slug>, never main", "write"),
               ("Maintainer reviews|land-evolution.sh on their word", "plan")])
notes(R, T2, H2, "Skills linked to the checkout", "keep serving main until it lands")

d.group(L, T2, W, H2, "Fail", 4)
column(L, T2, [("Nothing happens|no log, no queue", "data"),
               ("Git history|is the only record", "data")])
notes(L, T2, H2, "New features don't come this way:", "they go through the PRD and an issue")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="candidate", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="pass", at=(R + W / 2 + 34, T1 + H1 + 24))
d.arrow(f"M{R + 60} {T1 + H1}V{T1 + H1 + 18}H{L + W / 2}V{T2 - 2}", label="fail",
        at=(L + W / 2 + 120, T1 + H1 + 24))

d.note(600, 888, "One reproduced defect is proof enough; advice on behaviour needs several runs")

d.save(Path(__file__).with_name("evolve.svg"))
