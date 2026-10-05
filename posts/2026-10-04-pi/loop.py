"""Pi's agent loop: one run, turn by turn.  Drawn from the pi repo (https://github.com/earendil-works/pi,
packages/coding-agent/docs/how-pi-works.md, compaction.md "When It Triggers", extensions.md,
packages/agent/README.md and src/agent.ts (toolExecution defaults to "parallel"), commit b2b5c42).
Run: python3 loop.py

Snake order: 1 input (top left) -> 2 call the model (top right) -> 3 run the tools (bottom right)
-> 4 next turn or stop (bottom left), with a dashed arrow back to 2 for another turn."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi agent loop",
            "1 Input: your prompt starts a run. A steering message typed while it works goes in after the "
            "current turn; a follow-up goes in once the agent has nothing left to do. "
            "2 Call the model: the request is rebuilt before every call, and the model streams back text and "
            "tool calls. "
            "3 Run the tools: each call is checked one by one, where extension hooks can block it, then the "
            "allowed calls run in parallel by default, and the results are recorded in the original order. "
            "4 Next: tool results or queued messages start another turn; if the context is near full pi "
            "compacts it first. With nothing left the run ends.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400
CW = 492

# 1 input
d.group(L, T1, W, H1, "Input", 1)
d.card(L + 30, T1 + 72, "Your prompt|starts a run", w=CW, h=76, cls="human")
d.card(L + 30, T1 + 184, "Steering|goes in after this turn", "plan", w=CW, h=76)
d.card(L + 30, T1 + 296, "Follow-up|goes in when all is done", "plan", w=CW, h=76)

# 2 call the model
d.group(R, T1, W, H1, "Call the model", 2)
d.card(R + 30, T1 + 72, "Build the request|fresh every turn", "data", w=CW, h=76)
d.card(R + 30, T1 + 196, "Model answers|streams text + tool calls", "plan", w=CW, h=76)
d.arrow(f"M{R + W / 2} {T1 + 148}V{T1 + 196}")
d.note(R + 40, T1 + 324, "no tool calls and no queued", "start")
d.note(R + 40, T1 + 350, "messages: the run ends", "start")

# 3 run the tools
d.group(R, T2, W, H2, "Run the tools", 3)
d.card(R + 30, T2 + 64, "Check each call|one by one", "review", w=CW, h=76)
d.card(R + 30, T2 + 170, "Run them|in parallel by default", "coding", w=CW, h=76)
d.card(R + 30, T2 + 276, "Record results|in the original order", "write", w=CW, h=76)
d.arrow(f"M{R + W / 2} {T2 + 140}V{T2 + 170}")
d.arrow(f"M{R + W / 2} {T2 + 246}V{T2 + 276}")

# 4 next turn or stop
d.group(L, T2, W, H2, "Next turn?", 4)
d.card(L + 30, T2 + 72, "Context near full?|compact first", "write", w=CW, h=76)
d.card(L + 30, T2 + 184, "Start another turn", "plan", w=CW, h=64)
d.arrow(f"M{L + W / 2} {T2 + 148}V{T2 + 184}")
d.note(L + W / 2, T2 + 300, "extension hooks can block a call,")
d.note(L + W / 2, T2 + 326, "change a result or ask for one more turn")

# hand-offs, drawn last so they sit on top
d.arrow(f"M{L + W} {T1 + 100}H{R + 30}", label="message", at=(600, T1 + 88))
d.arrow(f"M{R + W - 60} {T1 + 272}V{T2 + 64}", label="tool calls", at=(R + W - 120, T1 + H1 + 22))
d.arrow(f"M{R} {T2 + 314}H{L + W}", label="results", at=(600, T2 + 302))
d.arrow(f"M{L + W - 30} {T2 + 216}H{600}V{T1 + 138}H{R + 30}", back=True,
        label="again", at=(600, T2 + 120))

d.note(600, 888, "a turn = one model call + its tool calls")

d.save(Path(__file__).with_name("loop.svg"))
