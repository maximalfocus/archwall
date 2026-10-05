"""Pi: what goes into one model request.  Drawn from the pi repo (https://github.com/earendil-works/pi,
packages/coding-agent/docs/how-pi-works.md, configuration.md, security.md, skills.md,
prompt-templates.md, sessions.md and src/core/system-prompt.ts, commit b2b5c42).  Run: python3 context.py

Snake order: 1 load at startup (top left) -> 2 system prompt (top right) -> 3 conversation
(bottom right) -> 4 the request (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi request context",
            "1 Load at startup: project trust decides whether the project's .pi folder loads (settings, "
            "extensions, skills, prompt templates, MCP servers, SYSTEM.md). Context files such as AGENTS.md "
            "and CLAUDE.md load with or without trust. "
            "2 System prompt: pi's base prompt, or SYSTEM.md in its place, then APPEND_SYSTEM.md, the context "
            "files, and a list of skills with name and description only; the full skill is read when needed. "
            "3 Conversation: the active branch of the session, a compaction summary in place of older "
            "messages, and your new message after prompt templates expand. "
            "4 The request: system prompt, tool declarations, messages and model settings. Extensions can "
            "change the messages first. It goes to the model through pi-ai.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400
CW = 492

# 1 load at startup
d.group(L, T1, W, H1, "Load at startup", 1)
d.card(L + 30, T1 + 72, "Project trust|you decide per folder", "review", w=CW, h=76)
d.card(L + 30, T1 + 184, ".pi folder|only if trusted", "data", w=CW, h=76)
d.card(L + 30, T1 + 296, "AGENTS.md, CLAUDE.md|load either way", "data", w=CW, h=76)
d.arrow(f"M{L + W / 2} {T1 + 148}V{T1 + 184}", label="yes", at=(L + W / 2 + 28, T1 + 172))

# 2 system prompt
d.group(R, T1, W, H1, "System prompt", 2)
for i, (lbl, k) in enumerate([("Base prompt|or SYSTEM.md instead", "data"), ("+ APPEND_SYSTEM.md", "data"),
                              ("+ context files", "data"), ("+ skill list|name + description", "data")]):
    d.card(R + 30, T1 + 64 + i * 82, lbl, k, w=CW, h=68)

# 3 conversation
d.group(R, T2, W, H2, "Conversation", 3)
d.card(R + 30, T2 + 72, "Active branch|of the session tree", "plan", w=CW, h=76)
d.card(R + 30, T2 + 172, "Compaction summary|instead of old messages", "write", w=CW, h=76)
d.card(R + 30, T2 + 272, "Your new message|templates expanded", w=CW, h=76, cls="human")

# 4 the request
d.group(L, T2, W, H2, "The request", 4)
for i, (lbl, k) in enumerate([("System prompt", "data"), ("Tool|declarations", "coding"),
                              ("Messages", "plan"), ("Model|settings", None)]):
    d.card(L + 30 + (i % 2) * 254, T2 + 72 + (i // 2) * 100, lbl, k, w=238, h=80)
d.note(L + W / 2, T2 + 318, "extensions can change the messages,")
d.note(L + W / 2, T2 + 344, "then pi-ai sends it to the model")

# hand-offs, drawn last so they sit on top
d.arrow(f"M{L + W} {T1 + 334}H{R}", label="files", at=(600, T1 + 322))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2}", label="prompt", at=(R + W / 2 + 46, T1 + H1 + 22))
d.arrow(f"M{R} {T2 + 210}H{L + W}", label="history", at=(600, T2 + 198))

d.note(600, 888, "full skill text is read only when a task needs it")

d.save(Path(__file__).with_name("context.svg"))
