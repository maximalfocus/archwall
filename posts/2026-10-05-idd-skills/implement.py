"""/idd-implement: one issue from a safe branch to an open pull request, never further.
Drawn from maximalfocus/idd-skills at commit f905928 (skills/idd-implement/SKILL.md,
skills/idd-plan/references/conventions.md).
Run: python3 implement.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-implement",
            "In: one open issue, read with its comments. "
            "1 Safe start: protect-main.sh ensure, so pull requests target dev; read the issue and comments, which "
            "must be OPEN and in this repository; make the branch issue/<N>-<slug>, never work on the default "
            "branch. With a dirty tree it asks, or works in a separate worktree. "
            "2 Small change: a plan in chat with the outcome, checks and non-goals; trace the path from entry "
            "point through logic to result; the smallest coherent diff that follows existing patterns; tests at "
            "the boundary, with a regression test for a bug. "
            "3 Verify, cheapest first: unit and regression tests, then typecheck and lint, then integration and "
            "the repository gate, then the changed boundary itself: container, CLI, route or browser. "
            "4 Open the pull request: commit only the issue's files with typed subjects and lines within 100 "
            "characters; a pull request into dev titled exactly like the issue; a Delivery-Type line; Closes #N "
            "only if every acceptance item is proven. It never merges, deploys or closes the issue by hand. "
            "A red check is fixed if this branch caused it, proven to be red before, or named as a blocker.")

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


d.pill(L, 16, W, 48, "In: one open issue, read with its comments")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Safe start", 1)
column(L, T1, [("protect-main.sh ensure|PRs target dev", "review"),
               ("Issue and comments|must be OPEN, same repo", "plan"),
               ("Branch issue/<N>-<slug>|never the default branch", "data")])
notes(L, T1, H1, "Dirty tree? It asks, or works", "in a separate worktree")

d.group(R, T1, W, H1, "Small change", 2)
column(R, T1, [("Plan in chat|outcome, checks, non-goals", "plan"),
               ("Trace the path|entry point → logic → result", "coding"),
               ("Smallest coherent diff|follows existing patterns", "coding"),
               ("Tests at the boundary|a regression test for a bug", "coding")])

d.group(R, T2, W, H2, "Verify, cheapest first", 3)
column4(R, T2, [("Unit and regression tests", "critic"),
               ("Typecheck and lint", "critic"),
               ("Integration, repo gate", "critic"),
               ("The changed boundary|container, CLI, route, browser", "critic")])

d.group(L, T2, W, H2, "Open the PR", 4)
column(L, T2, [("Commit only issue files|typed subjects, lines ≤ 100", "write"),
               ("PR into dev|titled exactly like the issue", "write"),
               ("Delivery-Type line|Closes #N only if all proven", "write")])
notes(L, T2, H2, "Never merges, deploys or", "closes the issue by hand")

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="branch", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="change", at=(R + W / 2 + 44, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + W + 2}", label="checked", at=(600, T2 + 164))

d.note(600, 888, "Red check? Fix it if new, prove it was red before, or name the blocker")

d.save(Path(__file__).with_name("implement.svg"))
