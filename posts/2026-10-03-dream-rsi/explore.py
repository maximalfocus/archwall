"""Dream-RSI step 1: one online run.  Drawn from the paper, section 3 "Online rollout", section 4
setup and appendix B.1 (exploration prompt), in github.com/zhengkid/Dream-RSI papers/Dream-RSI.pdf
(commit 4149ea9).  Run: python3 explore.py

Snake order: 1 pick (top left) -> 2 try (top right) -> 3 score (bottom right) ->
4 again or stop (bottom left) -> back to 1 for the next decision round."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Dream-RSI step 1: one online run",
            "1 Pick: the exploration policy, code that stays fixed for the whole run, picks a batch of up to W "
            "nodes, one per worker. 2 Try: for each pick a coding agent (Gemini CLI in the tests) resumes the "
            "parent's saved workspace, first reads every past try, wins and failures, then writes a new attempt: "
            "a program and a proposal, and never kills unrelated processes. 3 Score: a fixed evaluator scores "
            "it and writes diagnostics; the result becomes a new child node in the tree. 4 Again or stop: the "
            "next round picks again from the root and leaves; the run stops when the policy picks nothing or "
            "after K1 rounds, and the finished tree joins the pool.")

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


d.group(L, T1, W, H1, "Pick", 1)
column(L, T1, [("Exploration policy|code, fixed for the run", "plan"),
               ("Batch of picks|the root or leaves, up to W", "plan")])
d.note(L + W / 2, T1 + 300, "root = open a new branch")
d.note(L + W / 2, T1 + 326, "leaf = next step on its branch")

d.group(R, T1, W, H1, "Try", 2)
column(R, T1, [("Coding agent|resumes the parent's workspace", "coding"),
               ("Reads every past try|wins and failures", "data"),
               ("Writes a new attempt|program + proposal", "write")])
d.note(R + W / 2, T1 + 352, "in the tests: Gemini CLI, one per worker")
d.note(R + W / 2, T1 + 378, "never kills unrelated processes")

d.group(R, T2, W, H2, "Score", 3)
column(R, T2, [("Fixed evaluator|score + diagnostics", "critic"),
               ("New child node|added to the tree", "data")])
d.note(R + W / 2, T2 + 300, "same evaluator every round")

d.group(L, T2, W, H2, "Again or stop", 4)
d.card(L + 30, T2 + 64, "Next round|pick the root or leaves", "plan", w=CW, h=CH)
d.card(L + 30, T2 + 184, "Stop|empty pick or K₁ rounds", "review", w=CW, h=CH)
d.arrow(f"M{L + W / 2} {T2 + 248}V{T2 + 290}")
d.pill(L + 76, T2 + 292, 400, 46, "finished tree joins the pool", "front")

d.arrow(f"M{L + W} 200H{R - 2}", label="picks", at=(600, 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="attempt", at=(R + W / 2 + 50, T1 + H1 + 30))
d.arrow(f"M{R} {T2 + 160}H{L + W + 2}", label="tree", at=(600, T2 + 148))
d.arrow(f"M{L + W / 2} {T2 + 64}V{T1 + H1 + 2}", back=True, label="next round", at=(L + W / 2 + 70, T1 + H1 + 30))

d.save(Path(__file__).with_name("explore.svg"))
