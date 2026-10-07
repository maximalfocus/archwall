"""One call through Kong, in the order of the Nginx phases Kong hooks into.
Snake order: 1 arrive (top left) -> 2 match a route (top right) -> 3 run plugins (bottom right) -> 4 proxy and return (bottom left).
Drawn from Kong/kong at commit 8927af6 (kong/init.lua Kong.ssl_certificate .. Kong.log, kong/runloop/handler.lua,
kong/runloop/certificate.lua, kong/templates/kong_defaults.lua).
Run: python3 request.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("One call through Kong",
            "In: an app sends an HTTP call to Kong. "
            "1 Arrive: the proxy listens on port 8000 for HTTP and 8443 for HTTPS; for HTTPS Kong picks the TLS "
            "certificate by the server name (SNI); global plugins run their rewrite step before routing. "
            "TCP and UDP ports are off by default. "
            "2 Match a route: the router checks host, path, method and more, finds the Route and the Service "
            "behind it; with no match Kong answers 404, no Route matched. "
            "3 Run plugins: the access step runs the plugins for this route, service or consumer, "
            "such as auth, limits and transforms; a plugin may answer early and stop the call. "
            "4 Proxy and return: the balancer picks a target, the upstream answers, response plugins "
            "change headers and body, and log plugins run after the reply.")

d.pill(L, 16, GW, 48, "In: an app sends an HTTP call")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Arrive", 1)
d.column(L, T1, [("Proxy port|8000 http · 8443 https", "coding"),
                 ("TLS certificate|picked by server name (SNI)", "review"),
                 ("Global plugins|rewrite step · before routing", "review")])
d.notes(L, T1, H1, "TCP and UDP ports: off by default", "")

d.group(R, T1, GW, H1, "Match a route", 2)
d.column(R, T1, [("Router|host · path · method …", "plan"),
                 ("Route → Service|which backend to call", "plan"),
                 ("No match|404 · no Route matched", "review")])

d.group(R, T2, GW, H2, "Run plugins", 3)
d.column(R, T2, [("Auth|key-auth · jwt · oauth2 …", "review"),
                 ("Limits|rate-limiting · ip-restriction …", "review"),
                 ("Transforms|request-transformer …", "coding")])
d.notes(R, T2, H2, "A plugin may answer early and stop", "")

d.group(L, T2, GW, H2, "Proxy and return", 4)
d.column(L, T2, [("Balancer|picks a target", "coding"),
                 ("Upstream answers|the reply comes back", "coding"),
                 ("Response plugins|change headers · body", "coding"),
                 ("Log plugins|run after the reply", "data")], h=60, gap=14, first=60)

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="request", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="matched", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="allowed", at=(600, T2 + 164))

d.save(Path(__file__).with_name("request.svg"))
