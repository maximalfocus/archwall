"""/idd-acceptance: the finished product tested where people reach it, with classified failures.
Drawn from maximalfocus/idd-skills at commit f905928 (skills/idd-acceptance/SKILL.md,
skills/idd-acceptance/scripts/static-gate.sh, skills/idd-plan/scripts/manifest.sh verify).
Run: python3 acceptance.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-acceptance",
            "In: a finished pair, every issue landed, both trees clean. "
            "1 Bind: the exact pair with everything landed and no open issue, pull request or feature branch; if "
            "a tracker batch is still open it stops, since that needs a reconcile first; then each PRD outcome "
            "becomes a user journey, plus checks on the whole product. Unit tests alone are never the final "
            "boundary. "
            "2 The real boundary: a browser product through Playwright, by role and label; an HTTP service as "
            "its real process with real dependencies; a CLI or library in a fresh setup with pinned output; a "
            "container, worker or migration started for real, waiting for health, with throwaway state. "
            "3 Run it: start from clean or seeded state and wait for readiness, never fixed sleeps; run every "
            "journey, a bad path, and a restart when it matters; check that each preserved artifact exists and "
            "matches its row. Always tear down, even after a failure. "
            "4 PASS, or FAIL by kind: a product bug becomes one normal repair issue; bad fixture or data is "
            "fixed and run again; an unclear spec stops and asks for a clear contract; an environment problem is "
            "reported as the exact blocker. It never deploys, merges, edits the PRD or weakens a test.")

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


d.pill(L, 16, W, 48, "In: a finished pair, every issue landed, trees clean")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Bind", 1)
column(L, T1, [("Exact pair, all landed|no open issue, PR or branch", "review"),
               ("Tracker batch still open?|stop: reconcile it first", "review"),
               ("PRD outcomes → journeys|plus whole-product checks", "plan")])
notes(L, T1, H1, "Unit tests alone are never", "the final boundary")

d.group(R, T1, W, H1, "The real boundary", 2)
column(R, T1, [("Browser|Playwright, by role and label", "critic"),
               ("HTTP service|real process, real dependencies", "critic"),
               ("CLI or library|fresh setup, pinned output", "critic"),
               ("Container, worker, migration|wait for health, throwaway state", "critic")])

d.group(R, T2, W, H2, "Run it", 3)
column(R, T2, [("Clean or seeded start|wait for readiness, no fixed sleeps", "coding"),
               ("Every journey, a bad path|and a restart when it matters", "coding"),
               ("Preserved artifacts|exist, and match their row", "critic")])
notes(R, T2, H2, "Always tear down,", "even after a failure")

d.group(L, T2, W, H2, "PASS, or FAIL by kind", 4)
column4(L, T2, [("Product bug|→ one normal repair issue", "review"),
               ("Bad fixture or data|fix it, run again", "review"),
               ("Unclear spec|stop, ask for a clear contract", "review"),
               ("Environment|report the exact blocker", "review")])

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="journeys", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="start", at=(R + W / 2 + 34, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + W + 2}", label="results", at=(600, T2 + 164))

d.note(600, 888, "Never deploys, merges, edits the PRD or weakens a test")

d.save(Path(__file__).with_name("acceptance.svg"))
