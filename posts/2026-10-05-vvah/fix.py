"""VVAH phase 4a: propose a fix (S10, remediate).  Drawn from the community fork
maximalfocus/visa-vulnerability-agentic-harness (docs/remediation.md, docs/features.md section 6,
vvaharness/config/profiles/*.yaml step_remediate, commit 1c292e3).  Run: python3 fix.py

Snake order: 1 start (top left) -> 2 plan and edit (top right) -> 3 safety rails (bottom right)
-> 4 fix record (bottom left)."""
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

d = Diagram("VVAH phase 4a: propose a fix",
            "1 Start: verified findings from the scan report. Turn it on with --remediate or run the remediate "
            "command; it is off in the default profile, and --top N limits it to the N worst findings. "
            "2 Plan and edit: a planner agent reads the code and plans a minimal fix; a fixer sub-agent edits "
            "files inside the repo. Report-only mode proposes the fix without editing. "
            "3 Safety rails: a policy gate blocks edits to CI, hooks and git metadata and reverts any that slip "
            "through; a kill switch (an environment variable or a file) turns every fix into advice only; no shell "
            "tool is given, on purpose. A policy file that will not load means no edits at all. "
            "4 Fix record per finding: finding_case.json with the finding, the fix and its status, diff.patch with "
            "secrets masked, and a stopgap such as a request rule, config change or feature flag to try. S11 grades it next.")

d.group(L, T1, W, H1, "Start", 1)
col(L, T1, [("Verified findings|from the scan report", "data"),
            ("Turn it on|--remediate or remediate command", "review")], h=80)
d.note(L + W / 2, T1 + 300, "off in the default profile")
d.note(L + W / 2, T1 + 328, "--top N: only the N worst")

d.group(R, T1, W, H1, "Plan and edit", 2)
col(R, T1, [("Planner agent|reads code, plans a minimal fix", "plan"),
            ("Fixer sub-agent|edits files inside the repo", "coding")], h=80)
d.note(R + W / 2, T1 + 300, "report-only mode: propose, no edits")

d.group(R, T2, W, H2, "Safety rails", 3)
col(R, T2, [("Policy gate|no edits to CI, hooks, .git", "review"),
            ("Kill switch|env var or file → advice only", "review"),
            ("No shell|left out on purpose", "review")], arrows=False)
d.note(R + W / 2, T2 + 370, "a policy that will not load → no edits")

d.group(L, T2, W, H2, "Fix record", 4)
col(L, T2, [("finding_case.json|finding, fix, status", "write"),
            ("diff.patch|the change, secrets masked", "write"),
            ("Stopgap|rule, config or flag to try", "write")], arrows=False)
d.note(L + W / 2, T2 + 370, "next: S11 grades the fix")

handoffs("findings", "proposed change", "allowed")
d.save(Path(__file__).with_name("fix.svg"))
