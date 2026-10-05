"""Dream-RSI overview: the outer loop, one round at a time.  Drawn from the paper (Figure 1, section 3)
in github.com/zhengkid/Dream-RSI papers/Dream-RSI.pdf (commit 4149ea9) and https://dream-rsi.com/
(read 2026-10-05).  Run: python3 diagram.py

Snake order: 1 explore online (top left) -> 2 store the tree (top right) -> 3 dream (bottom right)
-> 4 deploy the best (bottom left) -> back to 1 for the next round."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Dream-RSI overview",
            "1 Explore online: the exploration policy, which is code, decides where a coding agent continues, "
            "how many tries run at once and when to stop; a fixed evaluator scores each try. "
            "2 Store the tree: the run leaves a discovery tree of every try and its score, added to a pool "
            "that grows by one tree per round; replaying a tree reruns nothing. "
            "3 Dream: a policy-development agent rewrites the policy M times; each version is replayed on every "
            "tree in the pool at zero executions, and its scores and traces guide the next rewrite. "
            "4 Deploy the best: the version with the best replay score runs the next round; the current policy "
            "competes too, so the pick never scores worse on replay.")

L, R, W = 24, 624, 552
T1, H1 = 16, 404
T2, H2 = 468, 404
CW, CH, GAP = 492, 64, 26


def column(x, top, cards):
    for i, (lbl, kind) in enumerate(cards):
        y = top + 64 + i * (CH + GAP)
        d.card(x + 30, y, lbl, kind, w=CW, h=CH)
        if i:
            d.arrow(f"M{x + W / 2} {y - GAP}V{y - 2}")


d.group(L, T1, W, H1, "Explore online", 1)
column(L, T1, [("Exploration policy (code)|where, how many, when to stop", "plan"),
               ("Coding agent|makes one new try per pick", "coding"),
               ("Fixed evaluator|scores every try", "critic")])
d.note(L + W / 2, T1 + 352, "many tries run in parallel")

d.group(R, T1, W, H1, "Store the tree", 2)
column(R, T1, [("Discovery tree|every try + its real score", "data"),
               ("Simulator pool|one more tree each round", "data")])
d.note(R + W / 2, T1 + 300, "a tree replays exactly:")
d.note(R + W / 2, T1 + 326, "every result is already saved")

d.group(R, T2, W, H2, "Dream", 3)
column(R, T2, [("Policy-dev agent|rewrites the policy code", "plan"),
               ("Replay on every tree|zero executions", "critic"),
               ("Scores + traces|guide the next rewrite", "data")])
d.note(R + W / 2, T2 + 352, "M versions, current one included")
d.arrow(f"M{R + 522} {T2 + 276}H{R + 538}V{T2 + 96}H{R + 524}", back=True)

d.group(L, T2, W, H2, "Deploy the best", 4)
column(L, T2, [("Best replay score|wins", "review"),
               ("Never worse on replay|the current policy competes", "data"),
               ("New policy|runs the next round", "plan")])

# hand-offs, snake order
d.arrow(f"M{L + W} 200H{R - 2}", label="tree", at=(600, 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="pool", at=(R + W / 2 + 40, T1 + H1 + 30))
d.arrow(f"M{R} {T2 + 200}H{L + W + 2}", label="versions", at=(600, T2 + 188))
d.arrow(f"M{L + W / 2} {T2}V{T1 + H1 + 2}", back=True, label="next round", at=(L + W / 2 + 70, T1 + H1 + 30))

d.save(Path(__file__).with_name("diagram.svg"))
