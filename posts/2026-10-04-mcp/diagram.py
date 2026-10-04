"""MCP architecture, drawn from the official docs for protocol version 2026-07-28:
https://modelcontextprotocol.io/docs/learn/architecture and
https://modelcontextprotocol.io/specification/2026-07-28/basic/index.  Run: python3 diagram.py

Who talks (host, clients, servers) is drawn across the top; each client-server link is one
connection with two layers: the transport outside, the data layer inside. The bottom row
zooms into those two layers."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("MCP architecture",
            "1 The host, an AI app like Claude Code or VS Code, holds the model and makes one MCP client per server; "
            "it merges every server's tools for the model and routes each call to the right client. "
            "2 Each client has one connection to its server, with two layers: the transport layer outside "
            "(stdio for a local server, Streamable HTTP for a remote one) and the data layer inside "
            "(the same JSON-RPC 2.0 messages on either transport). Messages go both ways: requests and "
            "notifications out, results and notifications back. "
            "3 Each server offers tools the model calls, resources the app reads and prompts the user picks. "
            "Data layer: every request carries its protocol version and client capabilities in _meta, so the "
            "server keeps no session; server/discover returns what the server supports; when a server needs user "
            "input the client asks the user and retries; subscriptions/listen streams list_changed notices. "
            "Transport layer: with stdio the client starts the server as a subprocess; Streamable HTTP posts "
            "to one endpoint and replies as JSON or an SSE stream, with OAuth recommended.")

HX, HW = 24, 360      # host column
CX, CW = 392, 416     # connection column
SX, SW = 816, 360     # server column
TOP_H = 536
PIPES = [(288, "Transport: stdio, local", "Server A, local", "Filesystem"),
         (420, "Transport: Streamable HTTP", "Server B, remote", "Sentry")]
PH = 120              # pipe height: request arrow, data-layer card, result arrow

# 1 host
d.group(HX, 16, HW, TOP_H, "Host: the AI app", 1)
d.sub(HX + 12, 60, HW - 24, 208, "Claude Code, VS Code …")
d.card(HX + 40, 104, "LLM + conversation", "plan", w=HW - 80, h=52)
d.note(HX + HW / 2, 204, "merges every server's tools")
d.note(HX + HW / 2, 228, "routes each call to its client")
d.sub(HX + 12, 276, HW - 24, 264, "One client per server")
for i, (y0, *_) in enumerate(PIPES):
    d.card(HX + 176, y0 + 38, f"Client {i + 1}", "coding", w=160, h=78)

# 2 connection: one per client, two layers
d.group(CX, 16, CW, TOP_H, "One connection, two layers", 2)
d.sub(CX + 12, 60, CW - 24, 216, "One client, one server")
d.note(CX + CW / 2, 112, "outside: the transport layer, the pipe")
d.note(CX + CW / 2, 136, "inside: the data layer, the messages")
d.card(CX + 48, 160, "JSON-RPC 2.0|the same on any pipe", "plan", w=CW - 96, h=72)
for y0, transport, _, _ in PIPES:
    d.sub(CX + 12, y0, CW - 24, PH, transport)
    d.card(CX + 40, y0 + 60, "Data layer: JSON-RPC", "plan", w=CW - 80, h=40)

# 3 servers
d.group(SX, 16, SW, TOP_H, "Servers: give context", 3)
d.sub(SX + 12, 60, SW - 24, 216, "Each server offers")
for i, (t, k) in enumerate([("Tools: the model calls", "coding"), ("Resources: the app reads", "data"),
                            ("Prompts: the user picks", "write")]):
    d.card(SX + 28, 98 + i * 56, t, k, w=SW - 56, h=46)
for y0, _, title, name in PIPES:
    d.sub(SX + 12, y0, SW - 24, PH, title)
    d.card(SX + 100, y0 + 38, name, "data", w=SW - 124, h=78)

# zoom: data layer (inside)
BY, BH = 572, 284
d.group(HX, BY, 552, BH, "Inside: the data layer")
for i, t in enumerate(["_meta on each request|version + caps, no session", "server/discover|what the server supports",
                       "elicitation/create|ask the user, then retry", "subscriptions/listen|list_changed notices"]):
    d.card(HX + 20 + (i % 2) * 262, BY + 60 + (i // 2) * 104, t, "plan", w=250, h=84)

# zoom: transport layer (outside)
TX = 624
d.group(TX, BY, 552, BH, "Outside: the transport layer")
d.card(TX + 20, BY + 60, "stdio|client starts the server", "data", w=250, h=84)
d.card(TX + 282, BY + 60, "Streamable HTTP|POST, JSON or SSE", "data", w=250, h=84)
d.note(TX + 145, BY + 176, "local, usually one client")
d.note(TX + 407, BY + 176, "remote, many clients")
d.note(TX + 276, BY + 236, "remote auth: tokens or headers, OAuth recommended")

# client <-> server arrows last, so they sit on top of the groups they cross
for y0, *_ in PIPES:
    d.arrow(f"M{HX + 336} {y0 + 49}H{SX + 100}", label="requests", at=(CX + 120, y0 + 54))
    d.arrow(f"M{SX + 100} {y0 + 109}H{HX + 336}", label="results", at=(CX + CW - 120, y0 + 114))

d.note(600, 892, "MCP 2026-07-28 · MCP runs between each client and its server; the host coordinates the clients")

d.save(Path(__file__).with_name("diagram.svg"))
