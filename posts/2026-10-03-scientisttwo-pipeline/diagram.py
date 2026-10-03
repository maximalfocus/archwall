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

d.pill(L, 16, GW, 44, "Human: “I want to build an efficient tabular foundation model”")
d.legend(R + 16, 44, ["coding", "critic", "plan", "write", "review"],
         ["coding", "critic", "planning", "writing", "review"])
d.arrow(f"M{L+GW/2} 60V80")

# Idea Generator (top left)
d.group(L, 84, GW, 280, "Idea Generator")
d.sub(L + 12, 124, GW - 24, 112, "Seed Idea Generator")
d.card(L + 30, 162, "Limitation|Extractor", w=CW)
d.card(L + 342, 162, "Novelty|Checker", "critic", w=CW)
d.arrow(f"M{L+210} 192H{L+336}")
d.sub(L + 12, 248, GW - 24, 104, "Idea Evolver")
d.ok(L + 58, 293); d.text(L + 74, 299, "Good idea", "ag", "start")
d.bad(L + 58, 323); d.text(L + 74, 329, "Bad idea", "ag", "start")
d.arrow(f"M{L+190} 310H{L+330}"); d.bulb(L + 352, 307); d.text(L + 370, 315, "New idea", "ag", "start")

# Evaluator (top right)
d.group(R, 84, GW, 280, "Evaluator")
d.sub(R + 12, 124, GW - 24, 112, "Subset Experiment Agent")
d.card(R + 30, 162, "Coding|Agent", "coding", w=CW); d.card(R + 342, 162, "Critic|Agent", "critic", w=CW); d.cycle(R + 276, 192, 10)
d.arrow(f"M{R+276} 236V242")
d.sub(R + 12, 248, GW - 24, 104, "Full-Set Experiment Agent")
d.card(R + 30, 282, "Coding|Agent", "coding", w=CW, h=56); d.card(R + 342, 282, "Critic|Agent", "critic", w=CW, h=56); d.cycle(R + 276, 310, 10)

# idea generator <-> evaluator
d.arrow(f"M{L+GW-12} 170H{R+6}"); d.bulb(L + GW + 24, 158)
d.arrow(f"M{L+GW-12} 270H{L+GW+12}V200H{R+6}"); d.bulb(L + GW + 1, 236)
d.arrow(f"M{R+12} 330H{L+GW-6}"); d.ok(L + GW + 14, 346); d.bad(L + GW + 34, 346)

# Analyzer (middle right)
d.group(R, 394, GW, 290, "Analyzer")
d.sub(R + 12, 434, GW - 24, 112, "Ablation Study Agent")
d.card(R + 30, 472, "Planning|Agent", "plan", w=CW); d.card(R + 342, 472, "Coding|Agent", "coding", w=CW)
d.arrow(f"M{R+210} 502H{R+336}")
d.arrow(f"M{R+276} 546V552")
d.sub(R + 12, 558, GW - 24, 116, "Idea Refiner")
d.card(R + 30, 598, "Critic|Agent", "critic", w=CW)
d.arrow(f"M{R+210} 628H{R+330}"); d.bulb(R + 352, 625); d.text(R + 370, 633, "New idea", "ag", "start")

# evaluator <-> analyzer
d.arrow(f"M{R+180} 364V388"); d.ok(R + 162, 379)
d.arrow(f"M{R+380} 394V370"); d.bulb(R + 400, 379)

# Writer and Peer-Review (middle left), Meta-Review (bottom left)
d.group(L, 394, GW, 130, "Writer Agent")
d.card(L + 30, 446, "Initial|Drafter", "write", w=CW); d.card(L + 342, 446, "Draft|Enhancer", "write", w=CW)
d.arrow(f"M{L+210} 476H{L+336}")
d.arrow(f"M{R} 459H{L+GW+6}")
d.cycle(L + GW / 2, 539, 12)
d.group(L, 554, GW, 130, "Peer-Review Agent")
d.card(L + 30, 606, "Review|Agent", "review", w=CW); d.card(L + 342, 606, "Rebuttal|Agent", "review", w=CW)
d.arrow(f"M{L+210} 636H{L+336}")
d.note(L + 273, 674, "answers with new experiments")
d.arrow(f"M{L+120} 684V708")
d.group(L, 714, GW, 130, "Meta-Review Agent")
d.card(L + 30, 766, "Critic|Agent", "critic", w=CW); d.card(L + 342, 766, "Idea|Refiner", w=CW)
d.arrow(f"M{L+210} 796H{L+336}")

# outputs and the loop back
d.pill(R + 60, 776, GW - 120, 44, "Expanded frontier: paper + code", "front")
d.arrow(f"M{L+GW} 798H{R+54}")
d.arrow(f"M{L+GW} 734H{R+420}V690", back=True)
d.note(R + 190, 756, "not good enough: back to analysis")

d.save(Path(__file__).with_name("diagram.svg"))
