"""MCP architecture, drawn from the official docs for protocol version 2026-07-28:
https://modelcontextprotocol.io/docs/learn/architecture and
https://modelcontextprotocol.io/specification/2026-07-28/basic/index.  Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("MCP architecture",
            "1 The host, an AI app like Claude Code or VS Code, makes one MCP client per server; "
            "each client keeps one dedicated connection. "
            "2 Transport: stdio for a local server on the same machine, usually one client; "
            "Streamable HTTP (POST, optional SSE, OAuth recommended) for a remote server that serves many clients. "
            "Both carry the same JSON-RPC 2.0 messages both ways: requests out, results and notifications back. "
            "3 The server exposes tools, resources and prompts, found with */list and used with resources/read, prompts/get or tools/call. "
            "4 Every request carries its protocol version and client capabilities in _meta, so the server keeps no "
            "session; server/discover returns versions and capabilities; a server can ask the user for input "
            "through elicitation; subscriptions/listen opens a stream of change notifications.")
A, B, GW = 24, 624, 552

# 1 host (top left)
d.group(A, 16, GW, 400, "Host: the AI app", 1)
d.sub(A + 12, 60, GW - 24, 100, "Claude Code, Claude Desktop, VS Code …")
d.card(A + 130, 100, "LLM + conversation", "plan", w=GW - 284, h=48)
d.sub(A + 12, 176, GW - 24, 228, "One MCP client per server")
for i in range(4):
    d.card(A + 30 + i * 128, 220, f"Client {i + 1}", "coding", w=112, h=48)
d.note(A + GW / 2, 300, "each client keeps one dedicated connection")
d.note(A + GW / 2, 330, "the host merges every server's tools")
d.note(A + GW / 2, 350, "into one list for the LLM, and routes each call")
d.note(A + GW / 2, 370, "to the client that owns the tool")

# host -> transport
# host <-> transport: requests out, results and notices back
d.arrow(f"M{A+GW} 226H{B}"); d.note(A + GW + 24, 216, "call")
d.arrow(f"M{B} 262H{A+GW}"); d.note(A + GW + 24, 282, "result")

# 2 transport (top right)
d.group(B, 16, GW, 400, "Transport layer", 2)
d.sub(B + 12, 60, GW - 24, 150, "Local: same machine")
d.card(B + 30, 104, "stdio|stdin / stdout", "data", w=200, h=64)
d.note(B + 260, 124, "the client starts the server", "start")
d.note(B + 260, 144, "usually serves one client", "start")
d.note(B + 260, 164, "credentials from the environment", "start")
d.sub(B + 12, 226, GW - 24, 150, "Remote: over the network")
d.card(B + 30, 270, "Streamable HTTP|POST + optional SSE", "data", w=200, h=64)
d.note(B + 260, 290, "serves many clients", "start")
d.note(B + 260, 310, "bearer token, API key, headers", "start")
d.note(B + 260, 330, "OAuth recommended", "start")
d.note(B + GW / 2, 400, "same JSON-RPC 2.0 messages on both")

# transport -> server
# transport <-> server
d.arrow(f"M{B+GW/2-40} 416V446"); d.note(B + GW / 2 - 52, 436, "requests", "end")
d.arrow(f"M{B+GW/2+40} 446V416"); d.note(B + GW / 2 + 52, 436, "results, notifications", "start")

# 3 server (bottom right)
CY = 446
d.group(B, CY, GW, 370, "Server: gives context", 3)
d.sub(B + 12, CY + 44, GW - 24, 150, "Three primitives")
d.card(B + 30, CY + 88, "Tools|tools/call", "coding", w=152, h=64)
d.card(B + 200, CY + 88, "Resources|resources/read", "data", w=152, h=64)
d.card(B + 370, CY + 88, "Prompts|prompts/get", "write", w=152, h=64)
d.note(B + GW / 2, CY + 178, "find them first with tools/list, resources/list …")
d.sub(B + 12, CY + 206, GW - 24, 152, "Examples")
d.card(B + 30, CY + 250, "Filesystem|local, stdio", "data", w=230, h=64)
d.card(B + 292, CY + 250, "Sentry|remote, HTTP", "data", w=230, h=64)


# 4 data layer (bottom left)
d.group(A, CY, GW, 370, "Data layer: each request stands alone", 4)
rows = [("_meta on every request", "plan", "protocol version + client caps"),
        ("server/discover", "plan", "versions, capabilities, identity"),
        ("elicitation/create", "review", "server asks the user, via the host"),
        ("subscriptions/listen", "data", "stream of list_changed notices")]
for i, (t, k, n) in enumerate(rows):
    y = CY + 52 + i * 76
    d.card(A + 24, y, t, k, w=240, h=56)
    d.note(A + 284, y + 33, n, "start")

d.note(600, 868, "MCP 2026-07-28 · no session: a stdio process is not a conversation; state that spans requests needs an explicit ID")

d.save(Path(__file__).with_name("diagram.svg"))
