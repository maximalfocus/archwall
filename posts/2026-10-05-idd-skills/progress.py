"""Tracker updates: one batch pull request in the PRD repo, merged only at a milestone.
Drawn from maximalfocus/idd-skills at commit f905928 (skills/idd-plan/scripts/progress-pr.sh,
skills/idd-plan/SKILL.md Reconcile mode, skills/idd-land/SKILL.md Step 3, skills/idd-publish/SKILL.md,
README.md).
Run: python3 progress.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-skills progress batch",
            "In: a landed issue, its pull request and its squash commit. "
            "1 Who writes: /idd-land after every merge, automatically; /idd-plan with the --reconcile flag "
            "to repair or resync; /idd-publish for the publication row. Only PROGRESS.md is edited, never PRD.md. "
            "2 Checks first: the tracker gate (80-word cells, no dates in cells), the PRD size and fold gates, which "
            "only report, the manifest drift check for unlisted files, and line width within 100 characters. "
            "3 One open batch pull request: the branch progress/batch with docs(progress) commits; it stays open "
            "for review and each update adds a commit; if two batches are open, it stops until there is one. "
            "4 Merged only at a milestone: a slice validated or a release finished, before acceptance or before "
            "publishing, at the end of /idd-auto, or on your own --reconcile. With changes requested or review "
            "threads open it exits with code 2, awaiting review. A pre-push hook refuses direct pushes to the "
            "PRD's main; it is not added if the clone already has its own hooks.")

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


d.pill(L, 16, W, 48, "In: a landed issue, its PR and squash commit")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Who writes", 1)
column(L, T1, [("/idd-land|after every merge, automatically", "review"),
               ("/idd-plan, flag --reconcile|repair or resync", "plan"),
               ("/idd-publish|the publication row", "review")])
notes(L, T1, H1, "Only PROGRESS.md,", "never PRD.md")

d.group(R, T1, W, H1, "Checks first", 2)
column(R, T1, [("Tracker gate|80-word cells, no dates in cells", "review"),
               ("PRD size and fold gates|report only", "review"),
               ("Manifest drift|no unlisted files", "review"),
               ("Line width|≤ 100 characters", "review")])

d.group(R, T2, W, H2, "One open batch PR", 3)
column(R, T2, [("Branch progress/batch|docs(progress): … commits", "write"),
               ("Stays open for review|each update adds a commit", "write"),
               ("Two batches open?|stop until there is one", "review")])

d.group(L, T2, W, H2, "Merged at a milestone", 4)
column(L, T2, [("Slice validated|or a release finished", "plan"),
               ("Before acceptance|or before publishing", "plan"),
               ("End of /idd-auto|or your own --reconcile", "plan")])
notes(L, T2, H2, "Changes requested or threads open:", "exit 2, awaiting review")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="edit", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="push", at=(R + W / 2 + 34, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + W + 2}", label="merge", at=(600, T2 + 164))

d.note(600, 888, "A pre-push hook refuses direct pushes to the PRD's main (skipped if the clone has its own hooks)")

d.save(Path(__file__).with_name("progress.svg"))
