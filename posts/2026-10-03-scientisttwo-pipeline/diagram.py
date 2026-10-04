"""ScientistTwo pipeline, redrawn from the overview figure at https://scientist-two.github.io/.  Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("ScientistTwo closed-loop research pipeline",
            "Idea Generator, Evaluator and Analyzer test whether an idea works; Writer, Peer-Review and Meta-Review "
            "test whether the paper passes. Results feed back to evolve and refine ideas, and the meta-review sends "
            "the work back to the Analyzer until it clears the bar.")
L, R, GW, CW = 24, 624, 552, 180
T, A = 80, 416   # top row y, Analyzer / Writer row y

d.pill(L, 16, GW, 44, "Human: “I want to build an efficient tabular foundation model”")
d.legend(R + 8, 44, ["coding", "critic", "plan", "write", "review"],
         ["coding", "critic", "planning", "writing", "review"])
d.arrow(f"M{L+GW/2} 60V{T}")

# Idea Generator (top left)
d.group(L, T, GW, 300, "Idea Generator")
d.sub(L + 12, T + 48, GW - 24, 118, "Seed Idea Generator")
d.card(L + 30, T + 86, "Limitation|Extractor", w=CW)
d.card(L + 342, T + 86, "Novelty|Checker", "critic", w=CW)
d.arrow(f"M{L+210} {T+118}H{L+336}")
d.sub(L + 12, T + 176, GW - 24, 112, "Idea Evolver")
d.ok(L + 58, T + 222); d.text(L + 76, T + 229, "Good idea", "ag", "start")
d.bad(L + 58, T + 256); d.text(L + 76, T + 263, "Bad idea", "ag", "start")
d.arrow(f"M{L+200} {T+240}H{L+330}"); d.bulb(L + 352, T + 236); d.text(L + 370, T + 247, "New idea", "ag", "start")

# Evaluator (top right)
d.group(R, T, GW, 300, "Evaluator")
d.sub(R + 12, T + 48, GW - 24, 118, "Subset Experiment Agent")
d.card(R + 30, T + 86, "Coding|Agent", "coding", w=CW); d.card(R + 342, T + 86, "Critic|Agent", "critic", w=CW)
d.cycle(R + 276, T + 118, 10)
d.arrow(f"M{R+276} {T+166}V{T+174}")
d.sub(R + 12, T + 176, GW - 24, 112, "Full-Set Experiment Agent")
d.card(R + 30, T + 210, "Coding|Agent", "coding", w=CW); d.card(R + 342, T + 210, "Critic|Agent", "critic", w=CW)
d.cycle(R + 276, T + 242, 10)

# idea generator <-> evaluator
d.arrow(f"M{L+GW-12} {T+100}H{R+6}"); d.bulb(L + GW + 24, T + 86)
d.arrow(f"M{L+GW-12} {T+206}H{L+GW+12}V{T+136}H{R+6}"); d.bulb(L + GW + 1, T + 172)
d.arrow(f"M{R+12} {T+266}H{L+GW-6}"); d.ok(L + GW + 14, T + 284); d.bad(L + GW + 34, T + 284)

# Analyzer (middle right)
d.group(R, A, GW, 310, "Analyzer")
d.sub(R + 12, A + 48, GW - 24, 118, "Ablation Study Agent")
d.card(R + 30, A + 86, "Planning|Agent", "plan", w=CW); d.card(R + 342, A + 86, "Coding|Agent", "coding", w=CW)
d.arrow(f"M{R+210} {A+118}H{R+336}")
d.arrow(f"M{R+276} {A+166}V{A+174}")
d.sub(R + 12, A + 176, GW - 24, 122, "Idea Refiner")
d.card(R + 30, A + 216, "Critic|Agent", "critic", w=CW)
d.arrow(f"M{R+210} {A+248}H{R+330}"); d.bulb(R + 352, A + 244); d.text(R + 370, A + 255, "New idea", "ag", "start")

# evaluator <-> analyzer
d.arrow(f"M{R+180} {T+300}V{A-6}"); d.ok(R + 160, T + 318)
d.arrow(f"M{R+380} {A}V{T+306}"); d.bulb(R + 402, T + 318)

# Writer and Peer-Review (middle left), Meta-Review (bottom left)
d.group(L, A, GW, 136, "Writer Agent")
d.card(L + 30, A + 56, "Initial|Drafter", "write", w=CW); d.card(L + 342, A + 56, "Draft|Enhancer", "write", w=CW)
d.arrow(f"M{L+210} {A+88}H{L+336}")
d.arrow(f"M{R} {A+88}H{L+GW+6}")
P = A + 160
d.cycle(L + GW / 2, A + 148, 10)
d.group(L, P, GW, 136, "Peer-Review Agent")
d.card(L + 30, P + 56, "Review|Agent", "review", w=160); d.card(L + 362, P + 56, "Rebuttal|Agent", "review", w=160)
d.arrow(f"M{L+190} {P+88}H{L+356}", label="new experiments", at=(L + 273, P + 78))
M = P + 160
d.arrow(f"M{L+120} {P+136}V{M-6}")
d.group(L, M, GW, 136, "Meta-Review Agent")
d.card(L + 30, M + 56, "Critic|Agent", "critic", w=CW); d.card(L + 342, M + 56, "Idea|Refiner", w=CW)
d.arrow(f"M{L+210} {M+88}H{L+336}")

# outputs and the loop back
d.pill(R + 60, M + 66, GW - 120, 44, "Expanded frontier: paper + code", "front")
d.arrow(f"M{L+GW} {M+88}H{R+54}")
d.arrow(f"M{L+GW} {M+24}H{R+420}V{A+316}", back=True, label="not good enough", at=(R + 200, M + 30))

d.save(Path(__file__).with_name("diagram.svg"))
