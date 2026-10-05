"""MCP participants: host, clients, servers, and the walls between servers.  Drawn from
https://modelcontextprotocol.io/docs/learn/architecture (Participants: the VS Code, filesystem,
database and Sentry example) and https://modelcontextprotocol.io/specification/2026-07-28/architecture
(Host, Clients, Servers, design principle 3) plus the spec index (Security: user consent).
Protocol version 2026-07-28, read 2026-10-05.  Run: python3 participants.py

Snake order: 1 the host (top left) -> 2 one client per server (top right) -> 3 local or remote
servers (bottom right) -> 4 walls between servers (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def grid(x, top, cards, h=80, gap=16, y0=64):
    """Two columns of cards, filled row by row."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30 + (i % 2) * 254, top + y0 + (i // 2) * (h + gap), lbl, kind, w=238, h=h)


def col(x, top, cards, h=64, gap=22, y0=64):
    """One column of wide cards, top to bottom."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + y0 + i * (h + gap), lbl, kind, w=492, h=h)


d = Diagram("MCP participants",
            "1 The host is the AI app. It makes the clients, one per server, keeps the conversation history, "
            "asks the user before any tool runs and merges context from all clients. "
            "2 Each client keeps a dedicated connection to one server. In the docs' example, client 1 talks to a "
            "local filesystem server, client 2 to a local database server, and clients 3 and 4 both talk to the "
            "remote Sentry server. "
            "3 A server is the program that serves context, wherever it runs: a local one uses stdio and usually "
            "serves one client; a remote one uses Streamable HTTP and usually serves many. "
            "4 Servers get only the context they need, cannot see into other servers, and the host controls "
            "anything that crosses servers.")

d.group(L, T1, W, H1, "Host: runs the show", 1)
grid(L, T1, [("Makes the clients|one per server", "plan"), ("Keeps the history|of the conversation", "plan"),
             ("Asks the user|before a tool runs", "review"), ("Merges context|from all clients", "plan")])
d.note(L + W / 2, T1 + 300, "the user agrees before their data")
d.note(L + W / 2, T1 + 328, "goes to any server")

d.group(R, T1, W, H1, "Clients: one per server", 2)
rows = [T1 + 72 + i * 66 for i in range(4)]
for i, y in enumerate(rows):
    d.card(R + 30, y, f"Client {i + 1}", "coding", w=150, h=56)
d.card(R + 330, rows[0], "Server A|Filesystem", "coding", w=192, h=56)
d.card(R + 330, rows[1], "Server B|Database", "coding", w=192, h=56)
d.card(R + 330, rows[2], "Server C|Sentry", "coding", w=192, h=122)
for y in rows:
    d.arrow(f"M{R + 180} {y + 28}H{R + 328}")
d.note(R + W / 2, T1 + 366, "each client keeps its own connection")

d.group(R, T2, W, H2, "Servers: local or remote", 3)
d.card(R + 30, T2 + 64, "Local server|on this machine", "coding", w=238, h=80)
d.card(R + 284, T2 + 64, "Remote server|on a platform", "coding", w=238, h=80)
d.card(R + 30, T2 + 196, "stdio|usually one client", "data", w=238, h=80)
d.card(R + 284, T2 + 196, "Streamable HTTP|usually many", "data", w=238, h=80)
d.arrow(f"M{R + 149} {T2 + 144}V{T2 + 194}")
d.arrow(f"M{R + 403} {T2 + 144}V{T2 + 194}")
d.note(R + W / 2, T2 + 326, "a server is the program that serves context,")
d.note(R + W / 2, T2 + 354, "wherever it runs")

d.group(L, T2, W, H2, "Walls between servers", 4)
col(L, T2, [("Servers get only|the context they need", "review"), ("No server sees|into another server", "review"),
            ("The host controls|anything across servers", "review")])
d.note(L + W / 2, T2 + 354, "the full conversation stays in the host")

d.arrow(f"M{L + W} {T1 + 160}H{R - 2}", label="creates", at=(600, T1 + 148))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="two kinds", at=(R + W / 2 + 60, T1 + H1 + 21))
d.arrow(f"M{R} {T2 + 182}H{L + W + 2}", label="kept apart", at=(600, T2 + 170))

d.note(600, 888, "Example from the docs: VS Code as the host, with a filesystem, a database and Sentry")

d.save(Path(__file__).with_name("participants.svg"))
