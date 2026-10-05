"""The charter: what "done" means for one run.
Drawn from maximalfocus/peerreview-skills at commit 2f8d61e (skills/peerreview/SKILL.md Steps 0.4-2,
templates/PROBLEM.md, scripts/charter-temp.sh, scripts/review-anchor.sh).
Run: python3 charter.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("peerreview charter",
            "1 Where intent comes from, in this order: your instruction now, an upstream source the project "
            "names, the PRD, plan or spec, then tests and docs. The code itself is evidence, never intent. "
            "2 The charter is a private temporary PROBLEM.md: problem, scope and non-goals; acceptance checks, "
            "each one testable; the verification gate, commands run every round; residuals, the known gaps. "
            "It is never added to the repo and is deleted at the end. "
            "3 Check the sources: if they conflict or none states the intended behaviour, stop and ask; "
            "if they agree, go on without a confirmation stop. "
            "4 Review plan: the repo type picks the review lenses, the run is full or only the changes since "
            "the last converged tag, and a round forecast is shown but is not a cap. The --dry-run flag stops here.")

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

d.pill(L, 16, W, 48, "In: your instruction and the repo's own docs")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Where intent comes from", 1)
column(L, T1, [("1  Your instruction now", "plan"),
               ("2  Upstream source it names", "plan"),
               ("3  PRD · plan · spec", "data"),
               ("4  Tests and docs", "data")])

d.group(R, T1, W, H1, "The charter (PROBLEM.md)", 2)
column(R, T1, [("Problem · scope · non-goals", "write"),
               ("Acceptance checks|each one testable", "write"),
               ("Verification gate|commands run every round", "write"),
               ("Residuals|known gaps, out of scope", "write")])

d.group(R, T2, W, H2, "Check the sources", 3)
column(R, T2, [("Conflict, or nothing written?|stop and ask you", "review"),
               ("Sources agree|go on, no confirmation stop", "plan")])
notes(R, T2, H2, "The code is evidence, never intent:", "checks from code would be circular")

d.group(L, T2, W, H2, "Review plan", 4)
column(L, T2, [("Repo type → lenses|e.g. cdd-prd, evidence-docs, code", "plan"),
               ("Full, or changes only|since the last converged tag", "plan"),
               ("Round forecast|shown to you, not a cap", "data")])
notes(L, T2, H2, "Flag --dry-run: show the plan", "and stop here")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="derive", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}")
d.arrow(f"M{R} {T2 + 176}H{L + W + 2}", label="go", at=(600, T2 + 164))

d.note(600, 888, "Private temp folder, never in the repo; deleted when the run ends, whatever the outcome")

d.save(Path(__file__).with_name("charter.svg"))
