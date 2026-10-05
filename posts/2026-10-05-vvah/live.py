"""VVAH live check: exploit verification inside S6 (beta, API only, opt-in).  Drawn from the community
fork maximalfocus/visa-vulnerability-agentic-harness (docs/exploit-verification.md sections "Enabling it",
"Live verification (S6)", "Safety during verification", "Re-checking a fix", "How it works inside";
vvaharness/config/profiles/default.yaml, commit 1c292e3).  Run: python3 live.py

Snake order: 1 turn it on (top left) -> 2 plan (top right) -> 3 test and judge (bottom right)
-> 4 outcome (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def col(x, top, cards, h=72, gap=24, arrows=True):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind) in enumerate(cards):
        y = top + 64 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


def grid(x, top, cards, h=80, gap=16, y0=64):
    """Two columns of cards, filled row by row."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30 + (i % 2) * 254, top + y0 + (i // 2) * (h + gap), lbl, kind, w=238, h=h)


def handoffs(a, b, c, ya=T1 + 206, yc=T2 + 200):
    """Arrows between the four groups in snake order, with what each one carries."""
    if a:
        d.arrow(f"M{L + W} {ya}H{R - 2}", label=a, at=(600, ya - 12))
    if b:
        d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label=b, at=(R + W / 2 + 14 + len(b) * 4.6, T1 + H1 + 21))
    if c:
        d.arrow(f"M{R} {yc}H{L + W + 2}", label=c, at=(600, yc - 12))

d = Diagram("VVAH live check",
            "1 Turn it on: set EV_API_COLLECTION to the app's API collection and EV_TARGET_URL to a copy of the "
            "app running on this machine. Requests may only go to localhost, enforced in code with no override. "
            "A reachability probe runs before any AI spend. Safe mode, on by default, skips destructive tests. "
            "2 Plan: classify whether a web request can test the finding at all, map it to an endpoint, and pick "
            "a test for that kind of weakness. "
            "3 Test and judge: send the test and look for a clear sign, let an attacker agent try a few more times "
            "within a budget, then an independent judge rules from the real requests and responses only. "
            "4 Outcome: confirmed with a repro, not confirmed, needs review, or static only. The static verifier "
            "still owns the verdict. ev-replay re-runs a confirmed test after a fix.")

d.group(L, T1, W, H1, "Turn it on", 1)
col(L, T1, [("API collection|EV_API_COLLECTION", "data"),
            ("Target on this machine|localhost only, no override", "review"),
            ("Reachability probe|before any AI spend", "review")])
d.note(L + W / 2, T1 + 380, "safe mode skips destructive tests")

d.group(R, T1, W, H1, "Plan", 2)
col(R, T1, [("Classify|can a web request test it?", "plan"),
            ("Map|finding → endpoint", "plan"),
            ("Pick a test|by kind of weakness", "plan")])
d.note(R + W / 2, T1 + 380, "not testable over the web → static only")

d.group(R, T2, W, H2, "Test and judge", 3)
col(R, T2, [("Send and check|look for a clear sign", "coding"),
            ("Attacker agent|a few more tries, capped", "coding"),
            ("Independent judge|sees only real traffic", "critic")])

d.group(L, T2, W, H2, "Outcome", 4)
grid(L, T2, [("Confirmed|with a repro", "plan"), ("Not confirmed|evidence against", "data"),
             ("Needs review|could not decide", "data"), ("Static only|not testable live", "data")],
     h=72, gap=14)
d.ok(L + 248, T2 + 78)
d.card(L + 30, T2 + 248, "ev-replay|re-run a confirmed test after the fix", "write", w=492, h=72)
d.note(L + W / 2, T2 + 370, "the static verifier still owns the verdict")

handoffs("routes", "test plan", "ruling")
d.note(600, 888, "Beta, web APIs only. It adds proof; it never removes a finding.")

d.save(Path(__file__).with_name("live.svg"))
