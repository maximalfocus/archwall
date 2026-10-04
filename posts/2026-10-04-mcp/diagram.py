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
TOP_H = 504
PIPES = [(232, "Transport: stdio, local", "Server A: filesystem"),
         (372, "Transport: Streamable HTTP", "Server B: Sentry, remote")]

# 1 host
d.group(HX, 16, HW, TOP_H, "Host: the AI app", 1)
d.sub(HX + 12, 60, HW - 24, 156, "Claude Code, VS Code …")
d.card(HX + 30, 100, "LLM + conversation", "plan", w=HW - 60, h=48)
d.note(HX + HW / 2, 176, "merges every server's tools for the LLM")
d.note(HX + HW / 2, 196, "and routes each call to its client")
d.sub(HX + 12, 232, HW - 24, 272, "One MCP client per server")
for i, (y0, _, _) in enumerate(PIPES):
    d.card(HX + 176, y0 + 53, f"Client {i + 1}", "coding", w=160, h=60)

# 2 connection: one per client, two layers
d.group(CX, 16, CW, TOP_H, "One connection, two layers", 2)
d.sub(CX + 12, 60, CW - 24, 156, "One client, one server")
d.note(CX + CW / 2, 106, "outside: the transport layer, the pipe")
d.note(CX + CW / 2, 130, "inside: the data layer, the messages")
d.note(CX + CW / 2, 160, "change the pipe, the messages stay the same:")
d.note(CX + CW / 2, 180, "JSON-RPC 2.0, client to server and back")
for y0, transport, _ in PIPES:
    d.sub(CX + 12, y0, CW - 24, 132, transport)
    d.card(CX + 28, y0 + 36, "Data layer: JSON-RPC", w=CW - 56, h=88)
    d.note(CX + 40, y0 + 56, "requests, notifications", "start")
    d.note(CX + CW - 40, y0 + 119, "results, notifications", "end")

# 3 servers
d.group(SX, 16, SW, TOP_H, "Servers: give context", 3)
d.sub(SX + 12, 60, SW - 24, 156, "Three primitives, found with */list")
d.note(SX + 30, 110, "Tools: the model calls them", "start")
d.note(SX + 30, 132, "Resources: the app reads them", "start")
d.note(SX + 30, 154, "Prompts: the user picks them", "start")
d.note(SX + SW / 2, 192, "tools/call · resources/read · prompts/get")
for y0, _, server in PIPES:
    d.sub(SX + 12, y0, SW - 24, 132, server)
    for j, (t, k) in enumerate([("Tools", "coding"), ("Resources", "data"), ("Prompts", "write")]):
        d.card(SX + 30 + j * 104, y0 + 50, t, k, w=96, h=60)

# zoom: data layer (inside)
BY = 540
d.group(HX, BY, 552, 300, "Inside: the data layer")
rows = [("_meta on every request", "version + client caps, no session"),
        ("server/discover", "versions, capabilities, identity"),
        ("elicitation/create", "client asks the user, then retries"),
        ("subscriptions/listen", "stream of list_changed notices")]
for i, (t, n) in enumerate(rows):
    y = BY + 56 + i * 60
    d.card(HX + 24, y, t, "plan", w=230, h=48)
    d.note(HX + 274, y + 29, n, "start")

# zoom: transport layer (outside)
TX = 624
d.group(TX, BY, 552, 300, "Outside: the transport layer")
d.sub(TX + 12, BY + 44, 528, 118, "Local")
d.card(TX + 30, BY + 80, "stdio|stdin / stdout", "data", w=190, h=60)
d.note(TX + 240, BY + 100, "the client starts the server", "start")
d.note(TX + 240, BY + 120, "usually serves one client", "start")
d.note(TX + 240, BY + 140, "credentials from the environment", "start")
d.sub(TX + 12, BY + 172, 528, 118, "Remote")
d.card(TX + 30, BY + 208, "Streamable HTTP|POST, JSON or SSE", "data", w=190, h=60)
d.note(TX + 240, BY + 228, "serves many clients", "start")
d.note(TX + 240, BY + 248, "bearer token, API key, headers", "start")
d.note(TX + 240, BY + 268, "OAuth recommended", "start")

# client <-> server arrows last, so they sit on top of the groups they cross
for y0, _, _ in PIPES:
    d.arrow(f"M{HX+176+160} {y0+62}H{SX+12}")
    d.arrow(f"M{SX+12} {y0+104}H{HX+176+160}")

d.note(600, 876, "MCP 2026-07-28 · MCP runs between each client and its server; the host coordinates the clients")

d.save(Path(__file__).with_name("diagram.svg"))
