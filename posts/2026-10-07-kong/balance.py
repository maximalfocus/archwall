"""Picking a backend: service, upstream and targets; the balancing algorithm; health checks; retries.
Snake order: 1 where it goes (top left) -> 2 algorithm (top right) -> 3 health checks (bottom right) -> 4 retries (bottom left).
Drawn from Kong/kong at commit 8927af6 (kong/db/schema/entities/services.lua, upstreams.lua, targets.lua;
kong/runloop/balancer/init.lua; kong/init.lua Kong.balancer).
Run: python3 balance.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Picking a backend",
            "In: a call has matched a route, so Kong knows its service. "
            "1 Where it goes: the service names a host. If that host is the name of an upstream, Kong balances "
            "the call across the upstream's targets, each an address and port with a weight, 100 by default; "
            "otherwise it goes to that one host. "
            "2 Algorithm: round-robin by default, or consistent-hashing on the consumer, IP, a header, a cookie, "
            "the path, a query argument or a URI capture, or least-connections, or latency. "
            "3 Health checks: active probing sends test requests to targets; it is off by default. "
            "Passive checks watch real responses as a circuit breaker; also off by default. "
            "4 Retries and timeouts: on a failure Kong reports it to the health checker and tries again, "
            "up to the service's retries, 5 by default; connect, write and read timeouts are 60 seconds by default.")

d.pill(L, 16, GW, 48, "In: the call matched a route and its service")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Where it goes", 1)
d.column(L, T1, [("Service|names a host", "plan"),
                 ("Upstream|a pool, if the host is its name", "plan"),
                 ("Targets|address:port · weight 100 default", "coding")])
d.notes(L, T1, H1, "Not an upstream → that one host", "")

d.group(R, T1, GW, H1, "Algorithm", 2)
d.column(R, T1, [("Round-robin|the default", "plan"),
                 ("Consistent hashing|consumer · IP · header · cookie …", "plan"),
                 ("Least connections|or latency", "plan")])

d.group(R, T2, GW, H2, "Health checks", 3)
d.column(R, T2, [("Active probes|test requests · off by default", "critic"),
                 ("Passive checks|circuit breaker · off by default", "critic")])
d.notes(R, T2, H2, "Unhealthy targets get no calls", "")

d.group(L, T2, GW, H2, "Retries and timeouts", 4)
d.column(L, T2, [("Try again on failure|up to 5 retries by default", "coding"),
                 ("Timeouts|connect · write · read 60 s", "review"),
                 ("Failure reported|to the health checker", "data")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="pool", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="target", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="call sent", at=(600, T2 + 164))

d.save(Path(__file__).with_name("balance.svg"))
