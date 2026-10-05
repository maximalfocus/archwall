"""Dream-RSI step 2: replay one policy on one recorded tree.  Drawn from the paper, section 2,
section 3 "Offline evaluation" and "Replay objective", Figure 2 and appendix B.2, in
github.com/zhengkid/Dream-RSI papers/Dream-RSI.pdf (commit 4149ea9), and the demo text on
https://dream-rsi.com/ (read 2026-10-05).  Run: python3 replay.py

Snake order: 1 start (top left) -> 2 pick (top right) -> 3 reveal (bottom right), looping back to 2
each round -> 4 stop and score (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Dream-RSI step 2: replay",
            "1 Start: a recorded tree from the pool, which never changes; the policy starts fresh and sees "
            "only the root. 2 Pick: the policy picks a batch, the root or leaves, up to W, using only what it "
            "has seen; hidden scores stay hidden. 3 Reveal: a picked leaf reveals its recorded next step, a "
            "picked root reveals the next unopened branch. Nothing runs; results come off disk. Then the policy "
            "picks again. 4 Stop and score: replay stops on an empty pick, after K2 rounds, or when the whole "
            "tree is seen. The replay score rewards the best result found, charges for every node revealed, "
            "and rewards bigger batches.")

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
column(L, T1, [("Recorded tree|from the pool, never changes", "data"),
               ("Policy sees|only the root", "plan")])
d.note(L + W / 2, T1 + 300, "starts fresh on every tree")

d.group(R, T1, W, H1, "Pick", 2)
column(R, T1, [("Policy picks a batch|the root or leaves, up to W", "plan")])
d.note(R + W / 2, T1 + 200, "uses only what it has seen;")
d.note(R + W / 2, T1 + 226, "hidden scores stay hidden")

d.group(R, T2, W, H2, "Reveal", 3)
column(R, T2, [("Picked a leaf|its recorded next step", "data"),
               ("Picked the root|the next unopened branch", "data")], arrows=False)
d.note(R + W / 2, T2 + 300, "nothing runs:")
d.note(R + W / 2, T2 + 326, "results come off disk")

d.group(L, T2, W, H2, "Stop and score", 4)
column(L, T2, [("Stop|empty pick, K₂ rounds, all seen", "review"),
               ("Replay score|best result, tries, batching", "critic")])
d.note(L + W / 2, T2 + 300, "charged for every node it reveals,")
d.note(L + W / 2, T2 + 326, "rewarded for running them in batches")

d.arrow(f"M{L + W} 160H{R - 2}", label="root", at=(600, 148))
d.arrow(f"M{R + W / 2 - 90} {T1 + H1}V{T2 - 2}", label="batch", at=(R + W / 2 - 140, T1 + H1 + 30))
d.arrow(f"M{R + W / 2 + 90} {T2}V{T1 + H1 + 2}", back=True, label="next round", at=(R + W / 2 + 160, T1 + H1 + 30))
d.arrow(f"M{R} {T2 + 200}H{L + W + 2}", label="stop", at=(600, T2 + 188))

d.save(Path(__file__).with_name("replay.svg"))
