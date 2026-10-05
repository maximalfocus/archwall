"""How the method itself changes: /peerreview-evolve and the constitution.
Drawn from maximalfocus/peerreview-skills at commit 2f8d61e (CONSTITUTION.md, skills/peerreview-evolve/SKILL.md,
skills/peerreview/SKILL.md Step 1.5, skills/peerreview-approach-*/).
Run: python3 evolve.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("peerreview evolution",
            "1 Triggers: after a review, from the raw session traces; research on a real gap, pulled and never "
            "scheduled; or simplifying, monthly or when a size cap is breached. "
            "2 The gate is the constitution: the change must be proven and high value, with impact times "
            "confidence over effort at least 3, not already covered, and it must fit the size caps of 1000, 800 "
            "and 150 lines. "
            "3 Pass: edit the skill, usually one of the seven lens modules for a repo type, and open a pull request "
            "with propose.sh; the maintainer lands it. "
            "4 Fail: nothing happens; there is no log and no queue, and git history is the only record.")

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

d.pill(L, 16, W, 48, "In: a lesson from a run, a gap, or a size breach")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Triggers", 1)
column(L, T1, [("After a review|from the raw session traces", "data"),
               ("Research a real gap|pulled, never scheduled", "data"),
               ("Simplify|monthly, or a size cap breached", "data")])
notes(L, T1, H1, "Run with /peerreview-evolve", "")

d.group(R, T1, W, H1, "Gate: the constitution", 2)
column(R, T1, [("Proven, high value|impact × confidence / effort ≥ 3", "review"),
               ("Not already covered", "review"),
               ("Fits the size caps|1000 · 800 · 150 lines", "review"),
               ("Leaves every past case|the same or better", "review")])

d.group(R, T2, W, H2, "Pass", 3)
column(R, T2, [("Edit the skill|often one of 7 lens modules", "write"),
               ("Open a PR|propose.sh; maintainer lands it", "write")])
notes(R, T2, H2, "Lens modules, one per repo type:", "PRD, conformance, evidence docs ...")

d.group(L, T2, W, H2, "Fail", 4)
column(L, T2, [("Nothing happens|no log, no queue", "data"),
               ("Git history|is the only record", "data")])
notes(L, T2, H2, "\"Maybe someday\" counts as fail:", "the same trigger will come back")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="candidate", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="pass", at=(R + W / 2 + 30, T1 + H1 + 24))
d.arrow(f"M{R + 60} {T1 + H1}V{T1 + H1 + 18}H{L + W / 2}V{T2 - 2}", label="fail", at=(L + W / 2 + 120, T1 + H1 + 24))

d.note(600, 888, "A lesson is either written into a skill now or dropped")

d.save(Path(__file__).with_name("evolve.svg"))
