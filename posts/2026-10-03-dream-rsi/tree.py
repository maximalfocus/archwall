"""Dream-RSI discovery tree: what one node holds and how a tree grows.  Drawn from the paper,
section 3 "Discovery trees and the shared decision interface" and "Online rollout", in
github.com/zhengkid/Dream-RSI papers/Dream-RSI.pdf (commit 4149ea9).  Run: python3 tree.py

Snake order: 1 one node = one try (top left) -> 2 how a tree grows (top right) ->
3 what a pick does (bottom right) -> 4 the pool (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Dream-RSI discovery tree",
            "1 One node is one try: the saved workspace after the try, the program and proposal the agent "
            "wrote, and the evaluator's score and diagnostics; each try starts from its parent's workspace. "
            "2 How a tree grows: the root is the starting workspace; branches hang off the root, and each "
            "branch is a chain of tries. Only the root and the leaves can be picked. "
            "3 What a pick does: picking the root opens a new branch, picking a leaf adds the next step on "
            "that branch, a refine or a repair; up to W picks run per round, one per worker; recorded nodes "
            "never change. 4 The pool: every finished tree joins the pool, one per round; the next run reads "
            "it as context but grows a new tree.")

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


d.group(L, T1, W, H1, "One node = one try", 1)
column(L, T1, [("Saved workspace|files after the try", "data"),
               ("Program + proposal|what the agent wrote", "write"),
               ("Score + diagnostics|from the evaluator", "critic")], arrows=False)
d.note(L + W / 2, T1 + 352, "each try starts from its parent's workspace")

d.group(R, T1, W, H1, "How a tree grows", 2)
cx = R + W / 2
d.card(cx - 130, T1 + 60, "Root|starting workspace", "data", w=260, h=60)
NW, NH = 120, 44
cols = [R + 60, R + 216, R + 372]      # left x of each branch's nodes
rows = [T1 + 170, T1 + 236, T1 + 302]
depth = [3, 2, 1]
for b, x in enumerate(cols):
    d.raw(f'<path d="M{cx} {T1 + 120}V{T1 + 145}H{x + NW / 2}V{rows[0] - 2}" class="flow"/>')
    for k in range(depth[b]):
        d.card(x, rows[k], "leaf" if k == depth[b] - 1 else "try", "data", w=NW, h=NH)
        if k:
            d.arrow(f"M{x + NW / 2} {rows[k] - 22}V{rows[k] - 2}")
d.note(cx, T1 + 382, "only the root and leaves can be picked")

d.group(R, T2, W, H2, "What a pick does", 3)
column(R, T2, [("Pick the root|opens a new branch", "plan"),
               ("Pick a leaf|next step: refine or repair", "plan"),
               ("Up to W picks a round|one per worker", "coding")], arrows=False)
d.note(R + W / 2, T2 + 352, "recorded nodes never change")

d.group(L, T2, W, H2, "The pool", 4)
for i, t in enumerate(["Tree 1", "Tree 2", "… Tree t"]):
    d.card(L + 30 + i * 166, T2 + 64, t, "data", w=150, h=64)
d.card(L + 30, T2 + 184, "Pool of trees|one more each round", "data", w=CW, h=CH)
for i in range(3):
    d.arrow(f"M{L + 105 + i * 166} {T2 + 128}V{T2 + 182}")
d.note(L + W / 2, T2 + 310, "the next run reads the pool for context,")
d.note(L + W / 2, T2 + 336, "but grows a brand-new tree")

d.arrow(f"M{L + W} 200H{R - 2}", label="nodes", at=(600, 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="each round", at=(R + W / 2 + 64, T1 + H1 + 30))
d.arrow(f"M{R} {T2 + 200}H{L + W + 2}", label="tree", at=(600, T2 + 188))

d.save(Path(__file__).with_name("tree.svg"))
