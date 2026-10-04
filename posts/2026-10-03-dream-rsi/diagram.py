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
A, B, GW, CW = 24, 624, 552, 200
L1, L2 = 30, GW - 30 - CW   # left / right card x inside a group

# 1 online explore (top left)
d.group(A, 16, GW, 380, "Online explore", 1)
d.sub(A + 12, 60, GW - 24, 130, "Discovery run")
d.card(A + L1, 104, "Exploration policy|(code)", "plan", w=CW)
d.card(A + L2, 104, "Coding|agent", "coding", w=CW)
d.arrow(f"M{A+L1+CW} 136H{A+L2-6}", label="guides", at=(A + GW / 2, 126))
d.sub(A + 12, 206, GW - 24, 176, "Recorded")
d.card(A + L2, 250, "Discovery|tree", "data", w=CW)
d.note(A + L2 + CW / 2, 342, "every attempt +")
d.note(A + L2 + CW / 2, 364, "its real result")
d.arrow(f"M{A+L2+CW/2} 168V244")

# 2 replay simulator (top right)
d.group(B, 16, GW, 380, "Build replay simulator", 2)
d.sub(B + 12, 60, GW - 24, 130, "Each tree becomes a world")
d.card(B + L1, 104, "Discovery|tree", "data", w=CW)
d.card(B + L2, 104, "Replay|simulator", "critic", w=CW)
d.arrow(f"M{B+L1+CW} 136H{B+L2-6}", label="exact", at=(B + GW / 2, 126))
d.sub(B + 12, 206, GW - 24, 176, "Simulator pool")
for i, t in enumerate(["Tree 1", "Tree 2", "… Tree t"]):
    d.card(B + 30 + i * 170, 250, t, "data", w=152)
d.note(B + GW / 2, 352, "one more world every round")
d.arrow(f"M{B+L2+CW/2} 168V244")

d.arrow(f"M{A+L2+CW} 282H{A+GW+24}V136H{B+L1-6}", label="store", at=(A + GW + 24, 230))

# 3 dream (bottom, full width)
C, CY = 24, 436
d.group(C, CY, 1152, 380, "Dream a better policy", 3)
d.sub(C + 12, CY + 44, 740, 324, "Inner loop · zero executions")
d.card(C + 48, CY + 100, "Policy-dev|agent", "plan", w=200, h=64)
d.card(C + 500, CY + 100, "Revised policy|πᵐ⁺¹", "coding", w=200, h=64)
d.card(C + 500, CY + 240, "Replay over|the whole pool", "critic", w=200, h=64)
d.card(C + 48, CY + 240, "History H|scores + traces", "data", w=200, h=64)
d.arrow(f"M{C+248} {CY+132}H{C+494}", label="revise", at=(C + 371, CY + 122))
d.arrow(f"M{C+600} {CY+164}V{CY+234}", label="score", at=(C + 640, CY + 205))
d.arrow(f"M{C+500} {CY+272}H{C+254}", label="store", at=(C + 377, CY + 262))
d.arrow(f"M{C+148} {CY+240}V{CY+170}", label="next revision", at=(C + 210, CY + 211))
d.arrow(f"M{C+752} {CY+196}H{C+838}")
d.card(C + 844, CY + 156, "Best policy|never worse", "plan", w=280, h=80)
d.note(C + 984, CY + 140, "after M revisions")
d.note(C + 970, CY + 272, "the current policy")
d.note(C + 970, CY + 294, "competes too")

d.arrow(f"M{B+GW/2} 396V{CY+84}H{C+758}", label="replay against", at=(B + GW / 2, 420))

# back to step 1
d.arrow(f"M{C+1100} {CY+236}V858H12V136H{A+L1-6}", back=True)
d.note(600, 884, "deploy the best policy → the next round explores further")

d.save(Path(__file__).with_name("diagram.svg"))
