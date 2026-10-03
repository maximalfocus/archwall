"""Dream-RSI loop, redrawn from Figure 1 of https://dream-rsi.com/.  Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Dream-RSI loop",
            "1 Online explore: the exploration policy (code) guides a coding agent, which grows a discovery tree. "
            "2 Each tree becomes an exact replay simulator, added to a growing pool. "
            "3 A policy-development agent revises the policy M times in a row; each version is scored by replay over "
            "the whole pool at zero executions, and the scores and traces go into its history for the next revision. "
            "The best version, never worse than the current one, is deployed for the next round.")
A, B, GW, CW = 24, 624, 552, 180

# 1 online explore (top left)
d.group(A, 16, GW, 380, "Online explore", 1)
d.sub(A + 12, 60, GW - 24, 130, "Discovery run")
d.card(A + 30, 104, "Exploration policy|(code)", "plan", w=CW)
d.card(A + 342, 104, "Coding|agent", "coding", w=CW)
d.arrow(f"M{A+210} 134H{A+336}"); d.note(A + 273, 124, "guides")
d.sub(A + 12, 206, GW - 24, 176, "Recorded")
d.card(A + 342, 250, "Discovery|tree", "data", w=CW)
d.note(A + 432, 340, "every attempt +")
d.note(A + 432, 358, "its real result")
d.arrow(f"M{A+432} 164V244")

# 2 replay simulator (top right)
d.group(B, 16, GW, 380, "Build replay simulator", 2)
d.sub(B + 12, 60, GW - 24, 130, "Each tree becomes a world")
d.card(B + 30, 104, "Discovery|tree", "data", w=CW)
d.card(B + 342, 104, "Replay|simulator", "critic", w=CW)
d.arrow(f"M{B+210} 134H{B+336}"); d.note(B + 273, 124, "exact")
d.sub(B + 12, 206, GW - 24, 176, "Simulator pool")
for i, t in enumerate(["Tree 1", "Tree 2", "… Tree t"]):
    d.card(B + 30 + i * 170, 250, t, "data", w=152)
d.note(B + GW / 2, 349, "one more world every round")
d.arrow(f"M{B+432} 164V244")

d.arrow(f"M{A+522} 280H{A+GW+24}V134H{B+24}"); d.note(A + GW + 24, 300, "store")

# 3 dream (bottom, full width)
C, CY = 24, 436
d.group(C, CY, 1152, 380, "Dream a better policy", 3)
d.sub(C + 12, CY + 44, 740, 324, "Inner loop · zero executions")
d.card(C + 48, CY + 100, "Policy-dev|agent", "plan", w=200, h=64)
d.card(C + 500, CY + 100, "Revised policy|πᵐ⁺¹", "coding", w=200, h=64)
d.card(C + 500, CY + 240, "Replay over|the whole pool", "critic", w=200, h=64)
d.card(C + 48, CY + 240, "History H|scores + traces", "data", w=200, h=64)
d.arrow(f"M{C+248} {CY+132}H{C+494}"); d.note(C + 371, CY + 122, "revise")
d.arrow(f"M{C+600} {CY+164}V{CY+234}")
d.arrow(f"M{C+500} {CY+272}H{C+254}"); d.note(C + 377, CY + 262, "store")
d.arrow(f"M{C+148} {CY+240}V{CY+170}"); d.note(C + 160, CY + 210, "next revision", "start")
d.arrow(f"M{C+752} {CY+196}H{C+838}"); d.note(C + 984, CY + 124, "after M revisions,")
d.note(C + 984, CY + 142, "pick the best")
d.card(C + 844, CY + 156, "Best policy|never worse", "plan", w=280, h=80)
d.note(C + 960, CY + 262, "the current policy is")
d.note(C + 960, CY + 280, "a candidate too")

d.arrow(f"M{B+GW/2} 396V{CY+84}H{C+758}")  # pool -> inner loop
d.note(B + GW / 2 + 12, 418, "replay against", "start")

# back to step 1
d.arrow(f"M{C+1100} {CY+236}V858H12V134H{A+24}", back=True)
d.note(600, 884, "deploy the best policy → the next round explores further")

d.save(Path(__file__).with_name("diagram.svg"))
