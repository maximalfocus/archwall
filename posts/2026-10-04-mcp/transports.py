"""MCP's two transports: stdio for local servers, Streamable HTTP for remote ones.  Drawn from
https://modelcontextprotocol.io/docs/learn/architecture (Participants, Transport layer) and
https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/index (binding, Cancellation,
Custom Transports), .../basic/transports/stdio (subprocess, newline framing, stderr, Shutdown) and
.../basic/transports/streamable-http (MCP endpoint, POST, JSON or SSE, Security & Endpoint,
Request Metadata, Server Validation), .../basic/index (Statelessness, Auth).
Protocol version 2026-07-28, read 2026-10-05.  Run: python3 transports.py

Snake order: 1 stdio, local (top left) -> 2 Streamable HTTP, remote (top right) ->
3 HTTP safety (bottom right) -> 4 what is the same on every transport (bottom left)."""
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


def col(x, top, cards, h=64, gap=20, y0=64):
    """One column of wide cards, top to bottom."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + y0 + i * (h + gap), lbl, kind, w=492, h=h)


d = Diagram("MCP transports",
            "1 stdio, for a local server: the client starts the server as a child process; they talk over stdin "
            "and stdout, one JSON message per line; to stop, the client closes stdin, waits, then forces the "
            "process to quit. Logs go to stderr, credentials come from the environment, and it usually serves one client. "
            "2 Streamable HTTP, for a remote server: one endpoint such as /mcp; each message is its own HTTP POST; "
            "the reply is one JSON object or an SSE stream. It usually serves many clients. "
            "3 HTTP safety: servers check the Origin header against DNS rebinding, bind to 127.0.0.1 when local, "
            "and require headers that copy the method, name and version, which must match the body. Sign-in is "
            "optional and uses OAuth. "
            "4 The same on every transport: the same JSON-RPC messages, no sessions; cancelling works on both, by a notice on "
            "stdio or by closing the stream on HTTP. Custom transports must keep the same message format.")

d.group(L, T1, W, H1, "stdio: a local server", 1)
col(L, T1, [("Client starts the server|as a child process", "coding"),
            ("stdin and stdout|one JSON message per line", "data"),
            ("To stop: close stdin|wait, then force it", "data")])
d.note(L + W / 2, T1 + 352, "logs go to stderr; keys come from the")
d.note(L + W / 2, T1 + 380, "environment; usually one client")

d.group(R, T1, W, H1, "Streamable HTTP: remote", 2)
col(R, T1, [("One endpoint|for example /mcp", "data"),
            ("Each message|its own HTTP POST", "coding"),
            ("Reply: one JSON object|or an SSE stream", "data")])
d.note(R + W / 2, T1 + 366, "usually serves many clients")

d.group(R, T2, W, H2, "HTTP safety", 3)
grid(R, T2, [("Check Origin|stops DNS rebinding", "review"), ("Local? Bind to|127.0.0.1 only", "review"),
             ("Headers copy|method, name, version", "data"), ("Sign-in|optional, OAuth", "review")])
d.note(R + W / 2, T2 + 302, "headers that don't match")
d.note(R + W / 2, T2 + 330, "the body are rejected")

d.group(L, T2, W, H2, "Same on every transport", 4)
col(L, T2, [("Same JSON-RPC messages", "data"), ("No sessions|each request stands alone", "plan"),
            ("Cancel works on both|stdio: a notice · HTTP: close the stream", "data")])
d.note(L + W / 2, T2 + 354, "custom transports keep the same format")

d.note(600, 888, "Streamable HTTP replaced the old HTTP+SSE transport, now deprecated")

d.save(Path(__file__).with_name("transports.svg"))
