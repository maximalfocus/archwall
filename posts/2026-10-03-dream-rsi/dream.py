"""Dream-RSI step 3: dream a better policy (the inner loop).  Drawn from the paper, section 3
"Offline evaluation" and "Policy improvement and selection", in github.com/zhengkid/Dream-RSI
papers/Dream-RSI.pdf (commit 4149ea9), and https://dream-rsi.com/ "Why the policy can never get
worse" (read 2026-10-05).  Run: python3 dream.py

Snake order: 1 start (top left) -> 2 score (top right) -> 3 rewrite (bottom right), looping back to
2 for each new version -> 4 pick (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Dream-RSI step 3: dream",
            "1 Start: version 0 is the current policy; the pool of t trees stays fixed while dreaming. "
            "2 Score: each version is replayed on every tree at zero executions and gets its average score. "
            "3 Rewrite: a policy-development agent, an LLM that stays the same, reads the replay traces and "
            "scores, plus feedback from earlier versions, and writes the next version of the policy code, "
            "which is scored the same way. 4 Pick: after M versions, the one with the best average score is "
            "deployed for the next online run. Version 0 competes too, so the pick never scores worse on "
            "replay of these trees.")

L, R, W = 24, 624, 552
T1, H1 = 16, 404
T2, H2 = 468, 404
CW, CH, GAP = 492, 64, 26


def column(x, top, cards, arrows=True):
    for i, (lbl, kind) in enumerate(cards):
        y = top + 64 + i * (CH + GAP)
        d.card(x + 30, y, lbl, kind, w=CW, h=CH)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - GAP}V{y - 2}")


d.group(L, T1, W, H1, "Start", 1)
column(L, T1, [("Current policy|version 0", "plan"),
               ("Pool of t trees|fixed while dreaming", "data")], arrows=False)

d.group(R, T1, W, H1, "Score", 2)
column(R, T1, [("Replay on every tree|zero executions", "critic"),
               ("Average score|over all t trees", "data")])

d.group(R, T2, W, H2, "Rewrite", 3)
column(R, T2, [("Policy-dev agent|reads traces + scores", "plan"),
               ("Next version|new policy code", "write")])
d.note(R + W / 2, T2 + 300, "also reads feedback")
d.note(R + W / 2, T2 + 326, "from earlier versions")

d.group(L, T2, W, H2, "Pick", 4)
column(L, T2, [("Best average score|out of all M versions", "review"),
               ("Deploy it|for the next online run", "plan")])
d.note(L + W / 2, T2 + 300, "version 0 competes too: never worse")
d.note(L + W / 2, T2 + 326, "on replay of these trees")

d.arrow(f"M{L + W} 200H{R - 2}", label="version 0", at=(600, 188))
d.arrow(f"M{R + W / 2 - 90} {T1 + H1}V{T2 - 2}", label="scores", at=(R + W / 2 - 146, T1 + H1 + 30))
d.arrow(f"M{R + W / 2 + 90} {T2}V{T1 + H1 + 2}", back=True, label="next version", at=(R + W / 2 + 166, T1 + H1 + 30))
d.arrow(f"M{R} {T2 + 200}H{L + W + 2}", label="M done", at=(600, T2 + 188))

d.save(Path(__file__).with_name("dream.svg"))
