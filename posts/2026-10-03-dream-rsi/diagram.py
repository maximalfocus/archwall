"""Dream-RSI loop, redrawn from Figure 1 of https://dream-rsi.com/.  Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram(1540, 430, "Dream-RSI loop",
            "1 Online explore: the exploration policy guides a coding agent, which grows a discovery tree. "
            "2 Each tree becomes an exact replay simulator, added to a growing pool. "
            "3 A policy agent proposes new policies and scores them by replaying them over the whole pool, at zero executions. "
            "The best policy, never worse than the current one, is deployed for the next round.")
A, B, C, GW = 24, 534, 1044, 472

# 1 online explore
d.group(A, 16, GW, 330, "Online explore", 1)
d.sub(A + 12, 56, GW - 24, 120, "Discovery run")
d.card(A + 28, 96, "Exploration|policy", "plan")
d.card(A + 280, 96, "Coding|agent", "coding")
d.arrow(f"M{A+192} 126H{A+274}"); d.note(A + 233, 116, "guides")
d.sub(A + 12, 192, GW - 24, 140, "Recorded")
d.card(A + 280, 226, "Discovery|tree", "data")
d.note(A + 362, 310, "every attempt + its real result")
d.arrow(f"M{A+362} 156V220")

# 2 replay simulator
d.group(B, 16, GW, 330, "Build replay simulator", 2)
d.sub(B + 12, 56, GW - 24, 120, "Each tree becomes a world")
d.card(B + 28, 96, "Discovery|tree", "data")
d.card(B + 280, 96, "Replay|simulator", "critic")
d.arrow(f"M{B+192} 126H{B+274}"); d.note(B + 233, 116, "exact")
d.sub(B + 12, 192, GW - 24, 140, "Simulator pool")
for i, t in enumerate(["Tree 1", "Tree 2", "… Tree t"]):
    d.card(B + 28 + i * 140, 226, t, "data", w=128)
d.note(B + GW / 2, 310, "one more world every round")
d.arrow(f"M{B+362} 156V220")

d.arrow(f"M{A+GW-12} 256H{A+GW+19}V126H{B+22}"); d.note(A + GW + 19, 286, "store")

# 3 dream
d.group(C, 16, GW, 330, "Dream a better policy", 3)
d.sub(C + 12, 56, GW - 24, 180, "Inner loop · zero executions")
d.card(C + 28, 92, "Policy|agent", "plan")
d.card(C + 280, 92, "New policy|πᵐ", "coding")
d.card(C + 280, 166, "Replay over|the whole pool", "critic")
d.card(C + 28, 166, "Score +|exec traces", "data")
d.arrow(f"M{C+192} 122H{C+274}"); d.note(C + 233, 112, "propose")
d.arrow(f"M{C+362} 152V160")
d.arrow(f"M{C+280} 196H{C+198}")
d.arrow(f"M{C+110} 166V158")
d.arrow(f"M{C+236} 236V256"); d.note(C + 250, 252, "pick the winner", "start")
d.card(C + 76, 262, "Best policy, never worse|(the current one is a candidate too)", "plan", w=320, h=56)

d.arrow(f"M{B+GW-12} 262H{B+GW+19}V206H{C+6}"); d.note(B + GW + 19, 286, "replay")

# back to step 1
d.arrow(f"M{C+236} 318V390H{A+110}V162", back=True)
d.note((A + C) / 2 + 120, 412, "deploy the best policy → next round explores further")

d.save(Path(__file__).with_name("diagram.svg"))
