"""/idd-land: the one step that merges, then the tracker update.
Drawn from maximalfocus/idd-skills at commit f905928 (skills/idd-land/SKILL.md,
skills/idd-land/scripts/land.sh, skills/idd-plan/references/conventions.md).
Run: python3 land.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-land",
            "You run /idd-land with an issue; /idd-auto and /idd-publish may also call it. "
            "1 Refuse early: a clean tree, the right repository and exactly one linked pull request; checks green, "
            "not a draft, no changes requested; and the tracker row found before anything on GitHub changes. "
            "Anything ambiguous stops before GitHub changes. "
            "2 Acceptance gate: every acceptance item proven from the pull request, the tests and the current "
            "code, and the change fits the product model. If anything is unproven it stops; only the "
            "--accept-residuals flag goes on, and that flag never overrides red checks, requested changes or "
            "conflicts. "
            "3 land.sh, one script: it checks the names (pull request title equals the issue title, branch "
            "issue/<N>-<slug>), the branch protection and the line width, composes the commit subject from the "
            "Delivery-Type line, for example fix: <issue title> (#PR), squash-merges into dev bound to the "
            "checked commit, closes the issue, deletes the branch, pulls dev and verifies all of it. "
            "4 Then the tracker: the tracker gate keeps PROGRESS.md within budget, /idd-plan reconcile commits to "
            "the batch pull request, and if this fails the merge stands and the failure is reported. With no PRD "
            "repository it reports not configured. land.sh is read whole before it runs, so a checkout that "
            "changes cannot alter it.")

L, R, W = 24, 624, 552
T1, H1 = 84, 380
T2, H2 = 500, 364
CW, CH, GAP = 492, 64, 16


def column(x, top, cards, gap=GAP):
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + 64 + i * (CH + gap), lbl, kind, w=CW, h=CH)


def column4(x, top, cards):
    """Four cards in a bottom-row group: a little tighter, so they stay inside the frame."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + 60 + i * 74, lbl, kind, w=CW, h=60)


def notes(x, top, h, a, b):
    d.note(x + W / 2, top + h - 52, a)
    d.note(x + W / 2, top + h - 26, b)


d.pill(L, 16, W, 48, "You: /idd-land <issue>  (or /idd-auto, /idd-publish)")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Refuse early", 1)
column(L, T1, [("Clean tree, right repo|exactly one linked PR", "review"),
               ("Checks green, not a draft|no changes requested", "review"),
               ("Find the tracker row|before touching GitHub", "plan")])
notes(L, T1, H1, "Anything ambiguous stops", "before GitHub changes")

d.group(R, T1, W, H1, "Acceptance gate", 2)
column(R, T1, [("Every item proven?|PR, tests, current code", "critic"),
               ("Fits the product model|no unrecorded detours", "critic"),
               ("Not proven: stop|flag --accept-residuals to go on", "review")])
notes(R, T1, H1, "The flag never overrides red checks,", "requested changes or conflicts")

d.group(R, T2, W, H2, "land.sh, one script", 3)
column4(R, T2, [("Names, protection, width|PR title = issue, issue/<N>-<slug>", "review"),
               ("Subject from Delivery-Type|e.g. fix: <issue title> (#PR)", "review"),
               ("Squash into dev|bound to the checked commit", "write"),
               ("Close issue, delete branch|pull dev, verify all", "data")])

d.group(L, T2, W, H2, "Then the tracker", 4)
column(L, T2, [("Tracker gate|PROGRESS.md within budget", "review"),
               ("/idd-plan reconcile|commit to the batch PR", "write"),
               ("If this fails|the merge stands, reported", "data")])
notes(L, T2, H2, "No PRD repo: reported", "as \"not configured\"")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="ready", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="proven", at=(R + W / 2 + 44, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + W + 2}", label="merged", at=(600, T2 + 164))

d.note(600, 888, "land.sh is read whole before it runs, so a checkout that changes can't alter it")

d.save(Path(__file__).with_name("land.svg"))
