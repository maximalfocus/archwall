"""One MCP request, start to finish: per-request metadata, discovery, listing and calling a tool.
Drawn from https://modelcontextprotocol.io/docs/learn/architecture (Statelessness and discovery;
Example steps Discovery, Tool Discovery, Tool Execution) and
https://modelcontextprotocol.io/specification/2026-07-28/basic/index (Statelessness, _meta),
.../server/discover and .../basic/versioning.  Protocol version 2026-07-28, read 2026-10-05.
Run: python3 request.py

Snake order: 1 what every request carries (top left) -> 2 discover, optional (top right) ->
3 list the tools (bottom right) -> 4 call a tool (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def col(x, top, cards, h=64, gap=22, y0=64, arrows=False):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind) in enumerate(cards):
        y = top + y0 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


d = Diagram("One MCP request",
            "1 Every request carries, in its _meta field, the protocol version (for example 2026-07-28) and the "
            "client's capabilities, and should carry the client's name. So the server keeps no session and needs "
            "nothing from earlier requests. "
            "2 Discover, optional for the client: server/discover returns the server's supported versions, "
            "capabilities and name. Every server must answer it. If a request uses a version the server does not "
            "support, the error lists the versions it does. "
            "3 List the tools: tools/list returns each tool's name, title, description and input schema. The "
            "result carries a cache hint; five minutes in the docs' example. "
            "4 Call a tool: tools/call with the tool name and arguments returns content such as text or images, "
            "which the host hands to the model.")

d.group(L, T1, W, H1, "Every request carries", 1)
col(L, T1, [("Protocol version|e.g. 2026-07-28", "data"), ("Client capabilities|what the client can do", "data"),
            ("Client name|should be there", "data")], gap=18)
d.note(L + W / 2, T1 + 352, "so the server keeps no session")
d.note(L + W / 2, T1 + 380, "and needs nothing from before")

d.group(R, T1, W, H1, "Discover (optional)", 2)
col(R, T1, [("server/discover|the client asks first", "coding"),
            ("Versions, capabilities|and the server's name", "data")], h=72, gap=48, arrows=True)
d.note(R + W / 2, T1 + 352, "every server must answer it")
d.note(R + W / 2, T1 + 380, "wrong version? the error lists good ones")

d.group(R, T2, W, H2, "List the tools", 3)
col(R, T2, [("tools/list|what can this server do?", "coding"),
            ("Name, title, description|and input schema per tool", "data")], h=72, gap=48, arrows=True)
d.note(R + W / 2, T2 + 326, "the reply carries a cache hint:")
d.note(R + W / 2, T2 + 354, "5 minutes in the docs' example")

d.group(L, T2, W, H2, "Call a tool", 4)
col(L, T2, [("tools/call|tool name + arguments", "coding"),
            ("Result|text, images, other content", "data")], h=72, gap=48, arrows=True)
d.note(L + W / 2, T2 + 354, "the host hands the result to the model")

d.arrow(f"M{L + W} {T1 + 210}H{R - 2}", label="on each", at=(600, T1 + 198))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="capabilities", at=(R + W / 2 + 66, T1 + H1 + 21))
d.arrow(f"M{R} {T2 + 182}H{L + W + 2}", label="tool name", at=(600, T2 + 170))

d.note(600, 888, "Example walk-through from the docs; every message is JSON-RPC 2.0")

d.save(Path(__file__).with_name("request.svg"))
