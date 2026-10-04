"""Pi and MCP: config, its own client, exposure, and how the model reaches MCP tools.  Drawn from the
pi repo (https://github.com/earendil-works/pi, packages/coding-agent/docs/mcp.md, codemode.md, cli.md,
packages/mcp/README.md and src/protocol, commit 2003871).  Run: python3 mcp.py

Snake order: 1 config (top left) -> 2 pi-mcp client (top right) -> 3 exposure (bottom right)
-> 4 how the model reaches the tools (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Pi MCP support",
            "1 Config: user servers in ~/.pi/agent/mcp.json, project servers in .pi/mcp.json, read only after "
            "the project is trusted; the same mcpServers format as Claude Code and Cursor; add them with "
            "pi mcp add or manage them with /mcp. 2 pi-mcp is pi's own MCP client, without the official SDK. "
            "It talks stdio to local servers and Streamable HTTP to remote ones, with OAuth sign-in, and "
            "supports protocol versions up to 2025-11-25. Each tool is named mcp__server__tool. "
            "3 Exposure, per server or per tool: codemode (the default), deferred, direct or hidden. "
            "4 The model reaches a codemode tool from a JavaScript script in a QuickJS sandbox, and only the "
            "script's output comes back; a deferred tool after tool_search declares it; a direct tool like a "
            "built-in one. Every call goes through pi's tool pipeline, so extension permission gates apply.")

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 396

# 1 config
d.group(L, T1, W, H1, "Config", 1)
d.card(L + 36, T1 + 70, "~/.pi/agent/mcp.json|user servers", "data", w=480, h=72)
d.card(L + 36, T1 + 160, ".pi/mcp.json|project, after trust", "data", w=480, h=72)
d.card(L + 36, T1 + 250, "pi mcp add  ·  /mcp", "write", w=480, h=64)
d.note(L + W / 2, T1 + 360, "same mcpServers format as Claude Code")
d.note(L + W / 2, T1 + 386, "a project entry wins over a user entry")

# 2 pi-mcp client
d.group(R, T1, W, H1, "pi-mcp: its own client", 2)
d.card(R + 36, T1 + 70, "stdio|local server", "coding", w=228, h=72)
d.card(R + 288, T1 + 70, "Streamable HTTP|remote, OAuth", "coding", w=228, h=72)
d.sub(R + 12, T1 + 172, W - 24, 150, "Each tool becomes")
d.card(R + 76, T1 + 222, "mcp__server__tool", "data", w=400, h=64)
d.note(R + W / 2, T1 + 360, "no official MCP SDK inside")
d.note(R + W / 2, T1 + 386, "protocol versions up to 2025-11-25")

# 3 exposure
d.group(R, T2, W, H2, "Exposure: per server or tool", 3)
for i, (lbl, k) in enumerate([("codemode|the default", "plan"), ("deferred|found by search", "plan"),
                              ("direct|like a built-in", "plan"), ("hidden|never reached", "data")]):
    d.card(R + 36 + (i % 2) * 252, T2 + 70 + (i // 2) * 100, lbl, k, w=228, h=76)
d.note(R + W / 2, T2 + 300, "toolExposure sets single tools,")
d.note(R + W / 2, T2 + 326, "for example delete_* hidden")

# 4 how the model reaches the tools
d.group(L, T2, W, H2, "How the model calls them", 4)
CX, CWD = L + 36, 228
d.card(CX, T2 + 64, "codemode script|QuickJS sandbox", "coding", w=CWD, h=72)
d.card(CX, T2 + 154, "tool_search|declares a match", "coding", w=CWD, h=72)
d.card(CX, T2 + 244, "direct call", "coding", w=CWD, h=64)
PX = L + 336
d.card(PX, T2 + 140, "Tool pipeline|permission gates", "review", w=180, h=96)
for y in (T2 + 100, T2 + 190, T2 + 276):
    d.arrow(f"M{CX + CWD} {y}C{CX + CWD + 40} {y} {PX - 40} {T2 + 188} {PX} {T2 + 188}")
d.note(L + W / 2, T2 + 344, "a script returns only its output")
d.note(L + W / 2, T2 + 370, "so big results stay out of context")

# hand-offs, drawn last so they sit on top
d.arrow(f"M{L + W} {T1 + 160}H{R}", label="connect", at=(600, T1 + 150))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2}", label="tools", at=(R + W / 2 + 36, T1 + H1 + 22))
d.arrow(f"M{R} {T2 + 200}H{L + W}", label="reach", at=(600, T2 + 190))

d.note(600, 884, "pi · github.com/earendil-works/pi · docs: mcp.md, codemode.md")

d.save(Path(__file__).with_name("mcp.svg"))
