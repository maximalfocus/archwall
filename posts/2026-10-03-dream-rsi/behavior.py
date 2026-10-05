"""Dream-RSI: what the learned policy does, and replay versus prompt tips.  Drawn from the paper,
section 5.1 (Figure 5) and 5.2 (Figure 6), both on the ConvDiv kernel task, in
github.com/zhengkid/Dream-RSI papers/Dream-RSI.pdf (commit 4149ea9), and the analysis section of
https://dream-rsi.com/ (read 2026-10-05).  Run: python3 behavior.py

Snake order: 1 scores climb (top left) -> 2 progress stalls (top right) -> 3 history as tips
(bottom right) -> 4 history as a world (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Dream-RSI learned behaviour",
            "On the ConvDiv kernel task. 1 Scores climb: as the round-best score rises, the learned policy "
            "spends less, cutting tries per round from 110 to 50. 2 Progress stalls: when the score flattens it "
            "spends more again, and those wider rounds line up with the next jumps in score. "
            "3 History as tips: turning past runs into direction tips in the prompt did worse than no tips, for "
            "both the fixed policy and Dream-RSI, at the same budget; the tips narrow the search. "
            "4 History as a world: replaying the history, as Dream-RSI does, beats using it as tips.")

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


d.group(L, T1, W, H1, "Scores climb", 1)
column(L, T1, [("Round-best score|rises", "data"),
               ("Policy spends less|110 → 50 tries a round", "plan")])
d.note(L + W / 2, T1 + 300, "ConvDiv kernel task")

d.group(R, T1, W, H1, "Progress stalls", 2)
column(R, T1, [("Score|flattens", "data"),
               ("Policy spends more|wider rounds", "plan")])
d.note(R + W / 2, T1 + 300, "the next score jumps follow")
d.note(R + W / 2, T1 + 326, "these wider rounds")

d.group(R, T2, W, H2, "History as tips", 3)
column(R, T2, [("Past runs → tips|written into the prompt", "write"),
               ("Did worse than no tips|fixed policy and Dream-RSI", "review")])
d.note(R + W / 2, T2 + 300, "tips narrow the search")

d.group(L, T2, W, H2, "History as a world", 4)
column(L, T2, [("Replay the history|what Dream-RSI does", "critic"),
               ("Beats the tips|same budget", "plan")])

d.arrow(f"M{L + W} 200H{R - 2}", label="then", at=(600, 188))
d.arrow(f"M{R} {T2 + 160}H{L + W + 2}", label="vs", at=(600, T2 + 148))

d.save(Path(__file__).with_name("behavior.svg"))
