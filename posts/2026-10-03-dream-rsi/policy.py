"""Dream-RSI: what the exploration policy controls, and the rules while dreaming.  Drawn from the
paper, section 3 and appendix B.2 (the policy-development agent's prompt), in
github.com/zhengkid/Dream-RSI papers/Dream-RSI.pdf (commit 4149ea9), and README.md ("Zero gradient
steps on the coding agent") at the same commit.  Run: python3 policy.py

Snake order: 1 what the policy decides (top left) -> 2 one knob, beta (top right) ->
3 rules while dreaming (bottom right) -> 4 what never changes (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Dream-RSI policy and rules",
            "1 What the policy decides: where to go next, how many tries run at once (up to W), when to stop, "
            "and how wide and deep the next run's grid is (branches times steps). It is code, rewritten by an "
            "agent. 2 One knob, beta: high beta means wider and more patient, low beta means fewer tries and "
            "earlier stops; beta is fixed during a run, and its default is re-chosen between rounds. "
            "3 Rules while dreaming, from the policy-development agent's prompt: the policy sees only what it "
            "has revealed, never copies scores or node ids from the traces, reads traces only between rounds, "
            "and the agent edits only the policy file. 4 What never changes: the coding agent and its model get "
            "no training, and the evaluator and tools stay the same; only the policy code changes.")

L, R, W = 24, 624, 552
T1, H1 = 16, 404
T2, H2 = 468, 404


def grid(x, top, cards, h=80, gap=20, y0=64):
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30 + (i % 2) * 254, top + y0 + (i // 2) * (h + gap), lbl, kind, w=238, h=h)


d.group(L, T1, W, H1, "What the policy decides", 1)
grid(L, T1, [("Where next|which node", "plan"), ("How many at once|up to W", "plan"),
             ("When to stop|end the run", "plan"), ("How wide, how deep|the next run's grid", "plan")])
d.note(L + W / 2, T1 + 300, "it is code, rewritten by an agent")
d.note(L + W / 2, T1 + 326, "between rounds")

d.group(R, T1, W, H1, "One knob: beta", 2)
grid(R, T1, [("High beta|wider, more patient", "plan"), ("Low beta|fewer tries, stops early", "plan")])
d.note(R + W / 2, T1 + 200, "fixed during a run;")
d.note(R + W / 2, T1 + 226, "default re-chosen between rounds")

d.group(R, T2, W, H2, "Rules while dreaming", 3)
grid(R, T2, [("Sees only|what it revealed", "review"), ("No copying|scores or node ids", "review"),
             ("Traces only|between rounds", "review"), ("Agent edits only|the policy file", "review")])
d.note(R + W / 2, T2 + 300, "set in the policy-dev agent's prompt")

d.group(L, T2, W, H2, "What never changes", 4)
d.card(L + 30, T2 + 64, "Coding agent + model|no training at all", "coding", w=492, h=64)
d.card(L + 30, T2 + 154, "Evaluator + tools|same every round", "critic", w=492, h=64)
d.note(L + W / 2, T2 + 270, "only the policy code changes")

d.arrow(f"M{L + W} 200H{R - 2}", label="uses", at=(600, 188))

d.save(Path(__file__).with_name("policy.svg"))
