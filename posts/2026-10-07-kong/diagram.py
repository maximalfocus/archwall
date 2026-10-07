"""Kong Gateway overview: set up the APIs, keep the config, handle each call, reach the backend.
Snake order: 1 set up (top left) -> 2 keep the config (top right) -> 3 handle each call (bottom right) -> 4 reach the backend (bottom left).
Drawn from Kong/kong at commit 8927af6 (README.md, kong.conf.default, kong/init.lua, kong/runloop, kong/clustering).
Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Kong Gateway overview",
            "In: an admin describes the APIs, then apps and AI clients call them through Kong. "
            "1 Set up: the Admin API on port 8001, Kong Manager on port 8002, or a declarative config file "
            "describe services, routes, plugins and upstreams. "
            "2 Keep the config: in Postgres, or with no database from a config file held in memory, "
            "or in hybrid mode where a control plane pushes it to data planes. "
            "3 Handle each call: apps call port 8000 or 8443; Kong matches a route, runs the plugins "
            "for it, such as auth, rate limits and logging, and picks a healthy target. "
            "4 Reach the backend: your services, LLM providers through the AI plugins, "
            "and logs and metrics tools.")

d.pill(L, 16, GW, 48, "In: an admin sets up the APIs that apps call")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Set up", 1)
d.column(L, T1, [("Admin API|port 8001 · local only by default", "plan"),
                 ("Kong Manager|web UI · port 8002", "plan"),
                 ("Config file|declarative · for DB-less", "write")])
d.notes(L, T1, H1, "Describes services · routes · plugins", "")

d.group(R, T1, GW, H1, "Keep the config", 2)
d.column(R, T1, [("Postgres|the default store", "data"),
                 ("No database|config file held in memory", "data"),
                 ("Hybrid mode|control plane → data planes", "plan")])

d.group(R, T2, GW, H2, "Handle each call", 3)
d.column(R, T2, [("Match a route|host · path · method", "plan"),
                 ("Run plugins|auth · limits · logs", "review"),
                 ("Pick a target|load balancing · health", "coding")])
d.notes(R, T2, H2, "Apps call port 8000 or 8443", "")

d.group(L, T2, GW, H2, "Reach the backend", 4)
d.column(L, T2, [("Your services|the APIs behind Kong", "coding"),
                 ("LLM providers|through the AI plugins", "coding"),
                 ("Logs and metrics|Prometheus · OpenTelemetry …", "data")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="config", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="loaded", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="proxied", at=(600, T2 + 164))

d.save(Path(__file__).with_name("diagram.svg"))
