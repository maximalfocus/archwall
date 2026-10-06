"""Partitioned contracts: one product contract split into a root index and per-context models.
Drawn from maximalfocus/idd-skills at commit f905928 (README.md, CONSTITUTION.md Articles 1 and 7,
skills/idd-plan/SKILL.md, skills/idd-plan/scripts/contract.sh, skills/idd-issue/SKILL.md,
skills/idd-implement/SKILL.md, skills/idd-land/SKILL.md, skills/idd-acceptance/SKILL.md).
Run: python3 contexts.py

Group 1 is the root index, group 2 one context, group 3 keeps issues and files in step, group 4 the
modes and gates."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-skills contexts",
            "A product too large for one coherent contract partitions the private PRD into contexts. "
            "The root PRD.md is the index: a Contexts table, a portfolio panel with a row for every "
            "context, and the manifest and cross-context invariants. A context is admitted only when "
            "work is planned there, and it is one coherent model with its own Scope of implementation "
            "paths, a Depends on list naming the contexts it references without restating them, and its "
            "own non-goals. An issue carries its context's name as a label, changed files must resolve "
            "to that context, and one context per issue goes dependency first; a change that crosses "
            "contexts is a design decision in the index first. The --context flag works on one context "
            "at a time, the contract gate runs over the index and then every context, the portfolio "
            "picks active work or the earliest unmet dependency, and acceptance goes context by context "
            "plus the index's cross-context invariants.")

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


d.pill(L, 16, W, 48, "A product too large for one coherent contract")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "The root contract: an index", 1)
column(L, T1, [("Index PRD.md|the Contexts table", "write"),
               ("Portfolio panel|a row for every context", "data"),
               ("The manifest|and cross-context invariants", "data")])
notes(L, T1, H1, "A context is admitted only", "when work is planned there")

d.group(R, T1, W, H1, "One context: its own model", 2)
column(R, T1, [("contexts/<name>/|PRD.md and PROGRESS.md", "write"),
               ("Scope|the implementation paths it owns", "plan"),
               ("Depends on|names contexts, never restates", "plan")])
notes(R, T1, H1, "A file in no context, or in two,", "is a scope question, not a cheap fix")

d.group(R, T2, W, H2, "Kept in step", 3)
column(R, T2, [("Issue label|the context name", "write"),
               ("Changed files|resolve to that context", "review"),
               ("One context per issue|dependency first", "review")])
notes(R, T2, H2, "A change that crosses contexts is a", "design decision in the index first")

d.group(L, T2, W, H2, "Modes and gates", 4)
column(L, T2, [("Flag --context <name>|one context at a time", "plan"),
               ("contract.sh gate|index, then every context", "review"),
               ("Portfolio order|active work, or earliest unmet", "plan")])
notes(L, T2, H2, "Every gate runs over the index", "and each context")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="indexes", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="labels the issue", at=(R + W / 2 + 44, T1 + H1 + 24))

d.note(600, 888, "Acceptance goes context by context, plus the index's cross-context invariants")

d.save(Path(__file__).with_name("contexts.svg"))
