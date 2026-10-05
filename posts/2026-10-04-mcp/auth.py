"""Signing in to a remote MCP server (optional): the authorization flow for HTTP transports.  Drawn
from https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization (Protocol
Requirements: optional, HTTP only, stdio uses the environment; Roles; Authorization Flow Steps;
Resource Parameter; Access Token Usage; Token Handling; Scope Challenge Handling) and
.../basic/authorization/client-registration (priority order; Dynamic Client Registration deprecated).
Protocol version 2026-07-28, read 2026-10-05.  Run: python3 auth.py

Snake order: 1 no token yet (top left) -> 2 find the auth server (top right) ->
3 get a client ID and sign in (bottom right) -> 4 use the token (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def col(x, top, cards, h=64, gap=22, y0=64, arrows=False, cls=None):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind, *c) in enumerate(cards):
        y = top + y0 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h, **({"cls": c[0]} if c else {}))
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


d = Diagram("Signing in to a remote server",
            "Optional, and only for HTTP servers; a stdio server takes credentials from the environment. "
            "1 No token yet: the client calls the MCP server and gets 401 Unauthorized, with a link to the "
            "server's metadata. "
            "2 Find the auth server: the server's resource metadata names its authorization server, which may "
            "be a separate service; the authorization server's metadata gives its addresses. "
            "3 Get a client ID, pre-registered or from a client metadata URL (Dynamic Client Registration still "
            "works but is deprecated). The user approves in the browser and the client gets an access token for "
            "this server only. "
            "4 Use the token: Authorization: Bearer on every HTTP request. The server checks the token was issued "
            "for it and never passes tokens on. If more access is needed, the server answers 403 and the client "
            "asks for more scopes.")

d.group(L, T1, W, H1, "No token yet", 1)
col(L, T1, [("Client calls the server|without a token", "coding"),
            ("401 Unauthorized|plus a link to its metadata", "review")], h=72, gap=48, arrows=True)
d.note(L + W / 2, T1 + 352, "optional, for HTTP servers only;")
d.note(L + W / 2, T1 + 380, "stdio takes keys from the environment")

d.group(R, T1, W, H1, "Find the auth server", 2)
col(R, T1, [("Server's resource metadata|names its auth server", "data"),
            ("Auth server metadata|its addresses", "data")], h=72, gap=48, arrows=True)
d.note(R + W / 2, T1 + 366, "the auth server can be a separate service")

d.group(R, T2, W, H2, "Get a client ID, sign in", 3)
col(R, T2, [("Client ID|pre-registered or a metadata URL", "plan"),
            ("User approves|in the browser", None, "human"),
            ("Access token|for this server only", "data")], h=64, gap=20, arrows=True)
d.note(R + W / 2, T2 + 354, "old-style registration (DCR) is deprecated")

d.group(L, T2, W, H2, "Use the token", 4)
col(L, T2, [("Authorization: Bearer|on every HTTP request", "data"),
            ("Server checks the token|was issued for it", "review"),
            ("Need more access?|403, then ask for more", "review")], h=64, gap=20)
d.note(L + W / 2, T2 + 354, "servers never pass tokens on")

d.arrow(f"M{L + W} {T1 + 260}H{R - 2}", label="link", at=(600, T1 + 248))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="auth server", at=(R + W / 2 + 60, T1 + H1 + 21))
d.arrow(f"M{R} {T2 + 268}H{L + W + 2}", label="token", at=(600, T2 + 256))

d.note(600, 888, "Based on OAuth 2.1; the server is the resource, the auth server issues tokens")

d.save(Path(__file__).with_name("auth.svg"))
