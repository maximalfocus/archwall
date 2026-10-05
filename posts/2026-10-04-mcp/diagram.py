"""MCP overview: how an AI app reaches tools and data, in four steps.  Drawn from the official
docs for protocol version 2026-07-28 (the current version, read 2026-10-05):
https://modelcontextprotocol.io/docs/learn/architecture (Participants, Layers, Primitives, Example)
https://modelcontextprotocol.io/specification/2026-07-28/architecture
Run: python3 diagram.py

Snake order: 1 host makes one client per server (top left) -> 2 each connection has two layers
(top right) -> 3 servers give context (bottom right) -> 4 the host uses the results (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def col(x, top, cards, h=64, gap=22, y0=64):
    """One column of wide cards, top to bottom."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + y0 + i * (h + gap), lbl, kind, w=492, h=h)


d = Diagram("MCP overview",
            "1 The host is the AI app, such as Claude Code or VS Code. It keeps the model and the conversation "
            "and makes one MCP client per server. "
            "2 Each client has one connection to its server, with two layers: the transport layer outside is the "
            "pipe (stdio for a local server, Streamable HTTP for a remote one), and the data layer inside is the "
            "messages, JSON-RPC 2.0, the same on either pipe. "
            "3 Servers give context: tools the model calls, resources the app reads, prompts the user picks. "
            "A server can be local, like a filesystem server, or remote, like Sentry. "
            "4 The host merges every server's tools into one list for the model, routes each call to the right "
            "client and adds the result to the conversation. MCP moves context; the app decides how to use it.")

d.group(L, T1, W, H1, "Host: the AI app", 1)
d.card(L + 30, T1 + 64, "Model + conversation|Claude Code, VS Code …", "plan", w=492, h=72)
d.sub(L + 16, T1 + 164, W - 32, 220, "One MCP client per server")
for i in range(3):
    d.card(L + 40 + i * 164, T1 + 216, f"Client {i + 1}", "coding", w=144, h=60)
d.note(L + W / 2, T1 + 318, "each client talks to one server")
d.note(L + W / 2, T1 + 346, "and keeps its own connection")

d.group(R, T1, W, H1, "One connection, two layers", 2)
d.sub(R + 16, T1 + 64, W - 32, 176, "Outside: transport, the pipe")
d.card(R + 46, T1 + 112, "Inside: data layer, the messages|JSON-RPC 2.0", "data", w=460, h=96)
d.card(R + 30, T1 + 264, "stdio|local server", "data", w=238, h=72)
d.card(R + 284, T1 + 264, "Streamable HTTP|remote server", "data", w=238, h=72)
d.note(R + W / 2, T1 + 380, "same messages on either pipe")

d.group(R, T2, W, H2, "Servers: give context", 3)
col(R, T2, [("Tools|the model calls them", "coding"), ("Resources|the app reads them", "data"),
            ("Prompts|the user picks them", "write")])
d.note(R + W / 2, T2 + 354, "local (a filesystem) or remote (Sentry)")

d.group(L, T2, W, H2, "Host: uses the results", 4)
col(L, T2, [("Merge every tool|one list for the model", "plan"), ("Route each call|to the right client", "plan"),
            ("Add the result|to the conversation", "data")])
d.note(L + W / 2, T2 + 354, "MCP moves context; the app decides the rest")

d.arrow(f"M{L + W} {T1 + 246}H{R - 2}", label="requests", at=(600, T1 + 234))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="same messages", at=(R + W / 2 + 80, T1 + H1 + 21))
d.arrow(f"M{R} {T2 + 182}H{L + W + 2}", label="results", at=(600, T2 + 170))

d.note(600, 888, "MCP protocol version 2026-07-28, the current one")

d.save(Path(__file__).with_name("diagram.svg"))
