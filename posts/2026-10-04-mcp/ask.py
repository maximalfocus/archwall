"""When an MCP server needs the user: elicitation over Multi Round-Trip Requests.  Drawn from
https://modelcontextprotocol.io/docs/learn/architecture (Primitives: Elicitation, deprecated client
primitives) and https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr
(InputRequiredResult, requestState, Supported Requests, Basic Workflow),
.../client/elicitation (form and URL modes, accept / decline / cancel, capability) and .../deprecated.
Protocol version 2026-07-28, read 2026-10-05.  Run: python3 ask.py

Snake order: 1 the client sends a call (top left) -> 2 the server answers "input required"
(top right) -> 3 the client asks the user (bottom right) -> 4 the client tries again (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def col(x, top, cards, h=72, gap=48, y0=64, arrows=True):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind) in enumerate(cards):
        y = top + y0 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


d = Diagram("When the server needs the user",
            "1 The client sends a call, for example tools/call as request 1. Its capabilities say it can ask the "
            "user (elicitation). Only tools/call, resources/read and prompts/get can get this answer. "
            "2 The server replies 'input required' with an elicitation/create request inside, plus optional "
            "requestState, its own notes that the client sends back unchanged. The server sends no request of its "
            "own and stores nothing in between. "
            "3 The client asks the user. Form mode collects things like names and choices; URL mode sends the user "
            "to a web page, and must be used for passwords, keys and payment details. The user accepts, declines "
            "or cancels. "
            "4 The client tries again as request 2 with the same parameters plus the answers, and gets the final "
            "result. Sampling and roots use the same path but are deprecated in 2026-07-28.")

d.group(L, T1, W, H1, "Client sends a call", 1)
col(L, T1, [("Capabilities: elicitation|the client can ask the user", "data"),
            ("tools/call|request 1", "coding")], arrows=False)
d.note(L + W / 2, T1 + 352, "only tools/call, resources/read")
d.note(L + W / 2, T1 + 380, "and prompts/get can be asked back")

d.group(R, T1, W, H1, "Server: input required", 2)
col(R, T1, [("Input required|elicitation/create inside", "plan"),
            ("requestState|the server's own notes", "data")], arrows=False)
d.note(R + W / 2, T1 + 352, "an answer, not a request from the server;")
d.note(R + W / 2, T1 + 380, "the server stores nothing in between")

d.group(R, T2, W, H2, "Client asks the user", 3)
d.card(R + 30, T2 + 64, "Form mode|names, choices", "review", w=238, h=80)
d.card(R + 284, T2 + 64, "URL mode|passwords, keys", "review", w=238, h=80)
d.card(R + 30, T2 + 200, "User: accept, decline|or cancel", None, w=492, h=72, cls="human")
d.arrow(f"M{R + 149} {T2 + 144}V{T2 + 198}")
d.arrow(f"M{R + 403} {T2 + 144}V{T2 + 198}")
d.note(R + W / 2, T2 + 326, "secrets never go in a form;")
d.note(R + W / 2, T2 + 354, "URL mode sends the user to a web page")

d.group(L, T2, W, H2, "Client tries again", 4)
col(L, T2, [("tools/call, request 2|same parameters + answers", "coding"), ("Final result", "data")])
d.note(L + W / 2, T2 + 326, "requestState goes back unchanged;")
d.note(L + W / 2, T2 + 354, "the server may ask again")

d.arrow(f"M{L + W} {T1 + 246}H{R - 2}", label="call", at=(600, T1 + 234))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="input required", at=(R + W / 2 + 76, T1 + H1 + 21))
d.arrow(f"M{R} {T2 + 236}H{L + W + 2}", label="answers", at=(600, T2 + 224))

d.note(600, 888, "Sampling and roots use the same path but are deprecated in 2026-07-28")

d.save(Path(__file__).with_name("ask.svg"))
