"""Running Kong: prepare, start a node, watch it, and the day-to-day commands.
Snake order: 1 prepare (top left) -> 2 inside a node (top right) -> 3 watch it (bottom right) -> 4 day to day (bottom left).
Drawn from Kong/kong at commit 8927af6 (bin/kong, kong/cmd/*.lua, kong.conf.default, kong/templates/kong_defaults.lua,
kong/init.lua, kong/constants.lua, kong/status, kong/plugins/prometheus).
Run: python3 ops.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Running Kong",
            "In: an operator runs Kong with the kong command. "
            "1 Prepare: kong check validates a config file, kong migrations bootstrap, up and finish set up "
            "or update the Postgres schema, and kong hybrid gen_cert makes the certificate pair for hybrid mode. "
            "2 Inside a node, after kong start: Nginx runs worker processes, auto by default; on data planes "
            "an extra worker handles config, on by default; values in the config can be vault references such as "
            "{vault://env/...}, and env is the one bundled vault. "
            "3 Watch it: the Status API on port 8007, local only by default; /status/ready, which says whether the router and plugins are built; "
            "Prometheus metrics with its plugin, and tracing, which is off by default. Anonymous usage "
            "reports to Kong are on by default. "
            "4 Day to day: kong reload starts new workers with the changed config, kong drain makes /status/ready "
            "return 503, and kong quit lets requests finish before shutting down, while kong stop sends a plain SIGTERM.")

d.pill(L, 16, GW, 48, "In: an operator runs the kong command")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Prepare", 1)
d.column(L, T1, [("kong check|validates a config file", "review"),
                 ("kong migrations|bootstrap · up · finish", "write"),
                 ("kong hybrid gen_cert|cert pair for hybrid mode", "plan")])

d.group(R, T1, GW, H1, "Inside a node", 2)
d.column(R, T1, [("Nginx workers|count: auto by default", "coding"),
                 ("Config worker|data planes · on by default", "coding"),
                 ("Vault references|{vault://env/…} in the config", "data")])
d.notes(R, T1, H1, "env is the one bundled vault", "")

d.group(R, T2, GW, H2, "Watch it", 3)
d.column(R, T2, [("Status API|port 8007 · local only by default", "critic"),
                 ("/status/ready|router · plugins built?", "critic"),
                 ("Metrics · traces|Prometheus plugin · tracing off", "data")])
d.notes(R, T2, H2, "Usage reports to Kong: on by default", "")

d.group(L, T2, GW, H2, "Day to day", 4)
d.column(L, T2, [("kong reload|new workers · new config", "coding"),
                 ("kong drain|/status/ready → 503", "review"),
                 ("kong quit · stop|quit lets requests finish", "coding")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="kong start", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="reports", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="you act", at=(600, T2 + 164))

d.save(Path(__file__).with_name("ops.svg"))
