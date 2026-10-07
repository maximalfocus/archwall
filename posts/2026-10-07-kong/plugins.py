"""What Kong's bundled plugins do, grouped by job; the 6 AI plugins have their own figure.
Snake order: 1 who is calling (top left) -> 2 guard traffic (top right) -> 3 change or forward (bottom right) -> 4 watch and log (bottom left).
Drawn from Kong/kong at commit 8927af6 (kong/constants.lua plugin list, kong/plugins/*/handler.lua PRIORITY and phases).
Run: python3 plugins.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("What the bundled plugins do",
            "In: a call that matched a route. Kong bundles 45 plugins; within each phase, the higher "
            "priority runs first. The 6 AI plugins have their own figure. "
            "1 Who is calling, 9 plugins: keys and tokens (key-auth, jwt, oauth2), passwords and signatures "
            "(basic-auth, ldap-auth, hmac-auth, standard-webhooks), sessions and groups (session, acl). "
            "2 Guard traffic, 9 plugins: limits (rate-limiting, response-ratelimiting, request-size-limiting), "
            "who may come in (ip-restriction, bot-detection, cors), and cache, stop or certificates "
            "(proxy-cache, request-termination, acme). "
            "3 Change or forward, 9 plugins: rewrite the call (request-transformer, response-transformer, "
            "redirect), other backends (aws-lambda, azure-functions, grpc-gateway, grpc-web), and your own code "
            "(pre-function runs first, post-function last). "
            "4 Watch and log, 12 plugins: metrics (prometheus, statsd, datadog), traces (opentelemetry, zipkin, "
            "correlation-id) and logs (http-log, file-log, tcp-log, udp-log, syslog, loggly). Most of them run "
            "in the log phase, after the reply.")

d.pill(L, 16, 1152, 48, "In: a call that matched a route · 45 bundled plugins · higher priority first · 6 AI ones: own figure")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Who is calling", 1)
d.column(L, T1, [("Keys and tokens|key-auth · jwt · oauth2", "review"),
                 ("Passwords and signatures|basic · ldap · hmac · webhooks", "review"),
                 ("Sessions and groups|session · acl", "review")])
d.notes(L, T1, H1, "9 plugins", "")

d.group(R, T1, GW, H1, "Guard traffic", 2)
d.column(R, T1, [("Limits|rate · response rate · request size", "review"),
                 ("Who may come in|ip-restriction · bot-detection · cors", "review"),
                 ("Cache · stop · certificates|proxy-cache · request-termination · acme", "coding")])
d.notes(R, T1, H1, "9 plugins", "")

d.group(R, T2, GW, H2, "Change or forward", 3)
d.column(R, T2, [("Rewrite the call|request · response-transformer · redirect", "coding"),
                 ("Other backends|aws-lambda · azure-functions · gRPC", "coding"),
                 ("Your own code|pre-function · post-function", "coding")])
d.notes(R, T2, H2, "9 plugins · pre-function first, post-function last", "")

d.group(L, T2, GW, H2, "Watch and log", 4)
d.column(L, T2, [("Metrics|prometheus · statsd · datadog", "data"),
                 ("Traces|opentelemetry · zipkin · correlation-id", "data"),
                 ("Logs|http · file · tcp · udp · syslog · loggly", "write")])
d.notes(L, T2, H2, "12 plugins · most run after the reply", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="caller known", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="allowed", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="sent", at=(600, T2 + 164))

d.save(Path(__file__).with_name("plugins.svg"))
