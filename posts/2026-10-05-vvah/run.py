"""VVAH day to day: commands, batches, resume and audit.  Drawn from the community fork
maximalfocus/visa-vulnerability-agentic-harness (docs/features.md section 6, docs/repos-csv.md,
docs/design-rationale.md, docs/architecture.md, docs/security.md, commit 1c292e3).  Run: python3 run.py

Snake order: 1 commands (top left) -> 2 many repos (top right) -> 3 never lose paid work
(bottom right) -> 4 audit and data (bottom left)."""
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

d = Diagram("VVAH day to day",
            "1 Commands: setup and doctor check readiness, estimate previews cost with no spend, scan runs the "
            "pipeline, remediate and validate fix and grade, ev-replay re-tests a fix, status and gc show progress "
            "and clean up. "
            "2 Many repos: a repos.csv with one row per repo; batch mode clones each one, can group repos by "
            "application for one report per app, and writes batch_summary.md. "
            "3 Never lose paid work: checkpoints per chunk and per finding in SQLite, outside the repo; an "
            "unfinished run continues by default and --fresh starts over; guards refuse when the commit or config "
            "changed. "
            "4 Audit and data: run_manifest.json records models, tokens and cost; prompts send code to the AI "
            "provider, so use approved endpoints; report folders get a local git-ignore rule so they are not "
            "committed by accident.")

d.group(L, T1, W, H1, "Commands", 1)
grid(L, T1, [("setup · doctor|check first", "review"), ("estimate|cost, no spend", "review"),
             ("scan|the pipeline", "coding"), ("remediate · validate|fix and grade", "coding"),
             ("ev-replay|re-test a fix", "critic"), ("status · gc|progress, cleanup", "data")],
     h=72, gap=14)

d.group(R, T1, W, H1, "Many repos", 2)
col(R, T1, [("repos.csv|one row per repo", "data"),
            ("Clone and group|one report per app", "coding"),
            ("batch_summary.md|the roll-up", "write")])

d.group(R, T2, W, H2, "Never lose paid work", 3)
col(R, T2, [("Checkpoints|per chunk, per finding", "data"),
            ("Resume by default|--fresh starts over", "plan"),
            ("Guards|same commit and config", "review")], arrows=False)
d.note(R + W / 2, T2 + 370, "stored in SQLite, outside the repo")

d.group(L, T2, W, H2, "Audit and data", 4)
col(L, T2, [("run_manifest.json|models, tokens, cost", "write"),
            ("Code goes to the AI provider|use approved endpoints", "review"),
            ("Reports kept out of git|local ignore rule", "review")], arrows=False)

handoffs("--repo-file", "per repo", "run record")
d.save(Path(__file__).with_name("run.svg"))
