"""The product contract: what PRD.md and PROGRESS.md hold, their budgets, and folding a done slice.
Drawn from maximalfocus/idd-skills at commit f905928 (CONSTITUTION.md Articles 1 and 7,
skills/idd-plan/SKILL.md, skills/idd-plan/scripts/prd-size-gate.sh, tracker-gate.sh, prd-fold-gate.sh,
manifest.sh, contract.sh).
Run: python3 contract.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-skills product contract",
            "Inside the private {project}-prd repository. "
            "1 PRD.md is one coherent model: requirements with stable IDs, the accepted behaviour; slices, small "
            "and in order, one issue each; the domain boundary with explicit non-goals; and preserved artifacts, "
            "the files a rewrite must keep. "
            "2 PROGRESS.md, using the same IDs, is a control panel: status per slice (ready, active, blocked, or "
            "missing acceptance), a "
            "baseline of what is done and verified, and an update rule for how rows may change. Its "
            "table cells carry no dates, since Git and GitHub keep the history. "
            "3 Budgets checked by scripts: PRD.md at most 1,000 words a section and 10,000 in all; PROGRESS.md at "
            "most 80 words a cell and a baseline of at most 20 lines. They change only through /idd-evolve, never "
            "per project, and were set from 4 real contracts and 11 trackers. "
            "4 Once a slice is validated, its acceptance moves into the requirement it extends, or becomes a "
            "new one, and the slice "
            "shrinks to one row; the fold gate flags a slice still holding a section. So the PRD grows with the "
            "model, not with the number of deliveries. A product too big for one model splits its PRD into "
            "contexts, each with its own scope.")

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


d.pill(L, 16, W, 48, "Inside the private {project}-prd")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "PRD.md: one coherent model", 1)
column(L, T1, [("Requirements|stable IDs, the accepted behaviour", "write"),
               ("Slices|small, in order, one issue each", "plan"),
               ("Domain boundary|explicit non-goals", "plan"),
               ("Preserved artifacts|files a rewrite must keep", "data")])

d.group(R, T1, W, H1, "PROGRESS.md: a control panel", 2)
column(R, T1, [("Status per slice|ready, active, blocked, missing acceptance", "write"),
               ("Baseline|what is done and verified", "data"),
               ("Update rule|how rows may change", "plan")])
notes(R, T1, H1, "No dates in cells: Git and", "GitHub keep the history")

d.group(R, T2, W, H2, "Budgets, checked by scripts", 3)
column(R, T2, [("PRD.md|≤ 1,000 words a section, ≤ 10,000 in all", "review"),
               ("PROGRESS.md|≤ 80 words a cell, baseline ≤ 20 lines", "review"),
               ("Changed only by /idd-evolve|never per project", "review")])
notes(R, T2, H2, "Set from 4 real contracts", "and 11 trackers")

d.group(L, T2, W, H2, "A slice, once validated", 4)
column(L, T2, [("Acceptance moves|into its requirement, or a new one", "write"),
               ("Slice shrinks to one row|in the slices table", "data"),
               ("Fold gate|flags a slice still holding a section", "review")])
notes(L, T2, H2, "The PRD grows with the model,", "not with the number of deliveries")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="same IDs", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="checked", at=(R + W / 2 + 46, T1 + H1 + 24))
d.arrow(f"M{L + W / 2} {T2}V{T1 + H1 + 2}", label="folds into", at=(L + W / 2 + 62, T1 + H1 + 24))

d.note(600, 888, "Too big for one model? The PRD splits into contexts, each with its own scope")

d.save(Path(__file__).with_name("contract.svg"))
