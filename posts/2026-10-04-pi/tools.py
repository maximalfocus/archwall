"""Pi's tools: the built-ins, how a tool reaches the model, and the two built-in extensions that reach
tools the model can't see.  Drawn from the pi repo (https://github.com/earendil-works/pi,
packages/coding-agent/docs/cli.md "Tools", codemode.md, extensions.md "Tool exposure",
src/core/tools/, src/extensions/index.ts and packages/codemode/README.md, commit b2b5c42).
Run: python3 tools.py

Snake order: 1 built-in tools (top left) -> 2 exposure (top right) -> 3 codemode (bottom right)
-> 4 tool_search (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi tools",
            "1 Built-in tools: read, bash, edit and write are on by default; grep, find, ls and powershell "
            "(Windows) are built in but off until you turn them on. Extensions add more. "
            "2 Exposure decides how a tool reaches the model: direct tools are declared to the model, "
            "model-only tools are declared but scripts cannot call them, codemode tools are only called "
            "from scripts, deferred tools wait for a search, hidden tools are unreachable. "
            "3 codemode, a built-in extension, off by default and turned on when an MCP server needs it: the "
            "model writes a JavaScript script that runs in a QuickJS sandbox with no files, network or "
            "timers, calls other tools, and only the script's output goes back to the model. "
            "4 tool_search, from the built-in tool-search extension, off by default: it searches tools that "
            "are not declared and declares the matches for the next model call; they stay declared on that branch.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400

# 1 built-in tools
d.group(L, T1, W, H1, "Built-in tools", 1)
d.sub(L + 12, T1 + 58, W - 24, 222, "On by default")
for i, lbl in enumerate(["read", "bash", "edit", "write"]):
    d.card(L + 30 + (i % 2) * 254, T1 + 104 + (i // 2) * 84, lbl, "coding", w=238, h=64)
d.note(L + W / 2, T1 + 334, "built in, off: grep, find, ls,")
d.note(L + W / 2, T1 + 360, "powershell (Windows)")

# 2 exposure
d.group(R, T1, W, H1, "How a tool reaches the model", 2)
for i, (lbl, k) in enumerate([("direct|declared to it", "plan"), ("codemode|from scripts only", "plan"),
                              ("deferred|after a search", "plan"), ("hidden|unreachable", "data")]):
    d.card(R + 30 + (i % 2) * 254, T1 + 64 + (i // 2) * 88, lbl, k, w=238, h=72)
d.card(R + 30, T1 + 240, "model-only|the model calls it, scripts cannot", "plan", w=492, h=64)
d.note(R + W / 2, T1 + 340, "built-ins are direct;")
d.note(R + W / 2, T1 + 366, "MCP tools default to codemode")

# 3 codemode
d.group(R, T2, W, H2, "codemode (off by default)", 3)
d.card(R + 30, T2 + 64, "Model writes a script|JavaScript", "plan", w=492, h=72)
d.card(R + 30, T2 + 164, "QuickJS sandbox|no files, no network", "review", w=492, h=72)
d.card(R + 30, T2 + 264, "Script calls tools|only its output returns", "coding", w=492, h=72)
d.arrow(f"M{R + W / 2} {T2 + 136}V{T2 + 164}")
d.arrow(f"M{R + W / 2} {T2 + 236}V{T2 + 264}")

# 4 tool_search
d.group(L, T2, W, H2, "tool_search (off by default)", 4)
d.card(L + 30, T2 + 72, "Search undeclared tools|ranked by relevance", "plan", w=492, h=76)
d.card(L + 30, T2 + 184, "Declare the matches|for the next call", "coding", w=492, h=76)
d.arrow(f"M{L + W / 2} {T2 + 148}V{T2 + 184}")
d.note(L + W / 2, T2 + 318, "both turn on by themselves")
d.note(L + W / 2, T2 + 344, "when an MCP server needs them")

# hand-offs, drawn last so they sit on top
d.arrow(f"M{L + W} {T1 + 200}H{R}", label="exposure", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2}", label="codemode tools", at=(R + W / 2 + 80, T1 + H1 + 22))
d.arrow(f"M{R + 40} {T1 + H1}V{T1 + H1 + 16}H{L + W - 40}V{T2}", label="deferred tools", at=(600, T1 + H1 + 22))

d.note(600, 888, "codemode scripts can also run classifier and image models")

d.save(Path(__file__).with_name("tools.svg"))
