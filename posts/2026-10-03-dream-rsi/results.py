"""Dream-RSI results: the test and the three domains.  Numbers from the paper, section 4, Figure 3,
Table 1 and Figure 4, in github.com/zhengkid/Dream-RSI papers/Dream-RSI.pdf (commit 4149ea9), and
the results section of https://dream-rsi.com/ (read 2026-10-05).  Run: python3 results.py

Snake order: 1 the test (top left) -> 2 Lasso path solver (top right) -> 3 math (bottom right)
-> 4 GPU kernels (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Dream-RSI results",
            "1 The test: both arms start from the same hand-written parallel-refine policy, so round 1 is "
            "identical; Recursive Fixed Exploration never changes it, Dream-RSI rewrites it between rounds. "
            "Same agent, evaluator and budget; cost is the total number of agent calls. "
            "2 Lasso path solver, Gemini-3.1 Pro, 5 rounds: 317 calls against 550, average runtime 2931 ms "
            "against 3587 ms on 6 held-out datasets, and 162 times fewer calls than SimpleTES (51,200); faster "
            "than sklearn and glmnet on all 6. 3 Math, 3 problems, under 1,000 generations: sum-difference "
            "1.145427, the best listed; circle packing 2.635983, tied best; autocorrelation competitive but not "
            "best. 4 GPU kernels, 4 KernelBench tasks: VGG16 and LayerNorm reach the same result with 2.43 and "
            "1.79 times fewer generations; ConvDiv and ConvMax score 2.09 and 1.44 times higher on the same "
            "budget.")

L, R, W = 24, 624, 552
T1, H1 = 16, 404
T2, H2 = 468, 404
CW, CH, GAP = 492, 64, 26


def column(x, top, cards):
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + 64 + i * (CH + GAP), lbl, kind, w=CW, h=CH)


d.group(L, T1, W, H1, "The test", 1)
column(L, T1, [("Same start policy|parallel refine, round 1 identical", "plan"),
               ("Fixed exploration|never changes the policy", "data"),
               ("Dream-RSI|rewrites it between rounds", "plan")])
d.note(L + W / 2, T1 + 352, "same agent, evaluator, budget")
d.note(L + W / 2, T1 + 378, "cost = total agent calls")

d.group(R, T1, W, H1, "Lasso path solver", 2)
column(R, T1, [("317 vs 550 calls|Gemini-3.1 Pro, 5 rounds", "critic"),
               ("2931 vs 3587 ms|average on 6 held-out datasets", "critic"),
               ("162× fewer calls|than SimpleTES (51,200)", "critic")])
d.note(R + W / 2, T1 + 352, "faster than sklearn and glmnet on all 6")

d.group(R, T2, W, H2, "Math, 3 problems", 3)
column(R, T2, [("Sum–difference|1.145427, best listed", "critic"),
               ("Circle packing|2.635983, tied best", "critic"),
               ("Autocorrelation|competitive, not best", "critic")])
d.note(R + W / 2, T2 + 352, "under 1,000 generations")
d.note(R + W / 2, T2 + 378, "(SimpleTES: 51,200)")

d.group(L, T2, W, H2, "GPU kernels, 4 tasks", 4)
column(L, T2, [("VGG16 2.43×, LayerNorm 1.79×|fewer generations, same result", "critic"),
               ("ConvDiv 2.09×, ConvMax 1.44×|higher score, same budget", "critic")])
d.note(L + W / 2, T2 + 300, "KernelBench, Gemini-3.1 Pro")

d.save(Path(__file__).with_name("results.svg"))
