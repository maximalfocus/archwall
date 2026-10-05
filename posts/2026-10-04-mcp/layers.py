"""MCP's two layers: the data layer inside, the transport layer outside.  Drawn from
https://modelcontextprotocol.io/docs/learn/architecture (Layers, Data layer, Transport layer) and
https://modelcontextprotocol.io/specification/2026-07-28/basic/index (Messages) and
.../basic/transports/index (Messages: no other direction exists).
Protocol version 2026-07-28, read 2026-10-05.  Run: python3 layers.py

Snake order: 1 data layer, what is said (top left) -> 2 the JSON-RPC messages (top right) ->
3 transport layer, how it travels (bottom right) -> 4 one inside the other (bottom left)."""
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


d = Diagram("MCP layers",
            "1 The data layer defines what is said: discovery of versions and capabilities, server features "
            "(tools, resources, prompts), client features (asking the user for input) and utilities (change "
            "notices, progress). "
            "2 It is written as JSON-RPC 2.0 messages. The client sends requests and notifications; the server "
            "sends a result or error for each request, and notifications. Servers never send requests. "
            "3 The transport layer defines how messages travel: connection setup, message framing and "
            "authorization, over stdio or Streamable HTTP. "
            "4 The data layer is the inner layer and the transport layer the outer one: swap the pipe and the "
            "messages stay the same.")

d.group(L, T1, W, H1, "Data layer: what is said", 1)
col(L, T1, [("Discovery|versions and capabilities", "plan"), ("Server features|tools, resources, prompts", "coding"),
            ("Client features|ask the user for input", "review"), ("Utilities|change notices, progress", "data")],
    h=60, gap=12)
d.note(L + W / 2, T1 + 386, "the inner layer")

d.group(R, T1, W, H1, "Messages: JSON-RPC 2.0", 2)
d.card(R + 30, T1 + 76, "Client", "coding", w=130, h=250)
d.card(R + 392, T1 + 76, "Server", "coding", w=130, h=250)
d.arrow(f"M{R + 160} {T1 + 130}H{R + 390}", label="request", at=(R + 276, T1 + 118))
d.arrow(f"M{R + 392} {T1 + 200}H{R + 162}", label="result or error", at=(R + 276, T1 + 188))
d.arrow(f"M{R + 160} {T1 + 262}H{R + 390}", label="notifications", at=(R + 276, T1 + 250))
d.arrow(f"M{R + 392} {T1 + 290}H{R + 162}")
d.note(R + W / 2, T1 + 362, "servers never send requests")
d.note(R + W / 2, T1 + 390, "notifications get no reply")

d.group(R, T2, W, H2, "Transport layer: how it travels", 3)
col(R, T2, [("Connection setup|start or reach the server", "data"), ("Message framing|where one message ends", "data"),
            ("Authorization|who may connect", "review")])
d.note(R + W / 2, T2 + 354, "stdio or Streamable HTTP")

d.group(L, T2, W, H2, "One inside the other", 4)
d.sub(L + 16, T2 + 64, W - 32, 208, "Outside: transport layer")
d.card(L + 56, T2 + 124, "Inside: data layer|JSON-RPC messages", "data", w=440, h=96)
d.note(L + W / 2, T2 + 326, "swap the pipe,")
d.note(L + W / 2, T2 + 354, "the messages stay the same")

d.arrow(f"M{L + W} {T1 + 210}H{R - 2}", label="written as", at=(600, T1 + 198))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="carried by", at=(R + W / 2 + 60, T1 + H1 + 21))
d.arrow(f"M{R} {T2 + 182}H{L + W + 2}", label="wraps", at=(600, T2 + 170))

d.note(600, 888, "Most developers work in the data layer; the SDKs handle the rest")

d.save(Path(__file__).with_name("layers.svg"))
