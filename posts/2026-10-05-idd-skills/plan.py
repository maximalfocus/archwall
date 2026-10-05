"""/idd-plan: four modes, picked by what already exists.
Drawn from maximalfocus/idd-skills at commit f905928 (skills/idd-plan/SKILL.md, CONSTITUTION.md
Article 1, skills/idd-plan/scripts/init-prd.sh).
Run: python3 plan.py

Top row: the two bootstrap modes. Both lead into default mode (bottom right); after an issue lands,
reconcile (bottom left) updates the tracker and the next issue comes from default mode again."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-plan modes",
            "/idd-plan picks its mode from what exists: no PRD yet, or an exact pair. "
            "1 New product, greenfield: ask about the product one decision at a time, draft PRD.md and "
            "PROGRESS.md with small slices in dependency order, and push a private, protected repository, or "
            "only show the drafts if you ask for a draft. It picks the technology itself unless that changes the "
            "product. "
            "2 Existing code, reconstruct: read the whole repository with its tests, docs and history, describe "
            "what it does at one named commit, and record one verified baseline; past commits never become "
            "slices. The --scope flag limits it to some paths in a repository too big to read at once. "
            "Both then push the PRD repository and go on in default mode. "
            "3 Default, what next: read the PRD, the tracker and GitHub without changing them, pick one next "
            "issue at the earliest unmet dependency, and write an issue contract with outcome, acceptance and "
            "non-goals. "
            "4 Reconcile, the tracker: run by the --reconcile flag or automatically after /idd-land; edit "
            "PROGRESS.md only, never PRD.md; run the gates, then commit to the batch pull request, which is "
            "merged at a milestone. Stale requirement text is reported, and fixed by your own docs(prd) pull "
            "request. No mode writes a plan file or a backlog, and there is at most one next issue.")

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


d.pill(L, 16, 2 * W + 48, 48, "/idd-plan picks its mode from what exists: no PRD yet, or an exact pair")

d.group(L, T1, W, H1, "New product: greenfield", 1)
column(L, T1, [("Ask about the product|one decision at a time", "plan"),
               ("Draft PRD.md, PROGRESS.md|small slices, in dependency order", "write"),
               ("Push a private repo, protected|or just drafts, if you ask", "write")])
notes(L, T1, H1, "Picks the tech itself, unless", "it changes the product")

d.group(R, T1, W, H1, "Existing code: reconstruct", 2)
column(R, T1, [("Read the whole repo|code, tests, docs, history", "plan"),
               ("Describe what it does|at one named commit", "write"),
               ("One verified baseline|past commits never become slices", "data")])
notes(R, T1, H1, "Flag --scope <paths>: for a repo", "too big to read at once")

d.group(R, T2, W, H2, "Default: what next?", 3)
column(R, T2, [("Read PRD, tracker, GitHub|read-only", "plan"),
               ("One next issue|earliest unmet dependency", "plan"),
               ("Issue contract|outcome, acceptance, non-goals", "write")])

d.group(L, T2, W, H2, "Reconcile: the tracker", 4)
column(L, T2, [("Flag --reconcile, or|automatically after /idd-land", "plan"),
               ("Edit PROGRESS.md only|never PRD.md", "write"),
               ("Gates, then the batch PR|merged at a milestone", "review")])
notes(L, T2, H2, "Stale requirement text is reported,", "fixed by your own docs(prd) PR")

d.arrow(f"M{L + W / 2} {T1 + H1}V{T1 + H1 + 18}H{R + W / 2}V{T2 - 2}", label="PRD pushed",
        at=(600, T1 + H1 + 24))
# Reconstruct joins the same line into default mode: a plain stroke, so only one arrowhead shows.
d.raw(f'<path d="M{R + W / 2} {T1 + H1}V{T1 + H1 + 18}" stroke="#5b6675" stroke-width="2" fill="none"/>')
d.arrow(f"M{R} {T2 + 150}H{L + W + 2}", label="landed", at=(600, T2 + 138))
d.arrow(f"M{L + W} {T2 + 250}H{R - 2}", back=True, label="next", at=(600, T2 + 238))

d.note(600, 888, "No mode writes a plan file or a backlog; at most one next issue")

d.save(Path(__file__).with_name("plan.svg"))
