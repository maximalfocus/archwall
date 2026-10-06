"""OpenConnector overview: callers come in, the gateway checks them, runs the action, keeps records.
Drawn from oomol-lab/open-connector at commit 20c6c44 (README.md, docs/runtime-api.md,
docs/credentials.md, docs/configuration.md, src/server/actions/action-runner.ts).
Run: python3 diagram.py

Snake order: 1 way in (top left) -> 2 checks (top right) -> 3 run (bottom right) -> 4 records (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("OpenConnector overview",
            "In: AI agents and apps that need your accounts on other services. "
            "1 Way in: MCP at /mcp with five tools, the HTTP API under /v1 used by the SDK, the oo CLI and "
            "OpenAPI clients, and the Web Console on the admin API under /api. "
            "2 Checks: a bearer token when one is configured (runtime token, JWT or admin), allow and block rules per action, "
            "then picking which connected account to use. "
            "3 Run: the input is checked against the action's schema, the provider's code loads the first "
            "time it is used, and its requests go out through a guarded fetch that blocks private addresses; "
            "out to 1,000+ provider APIs, or to OOMOL's Marketplace or SaaS for remote accounts. "
            "4 Records: a redacted run log, the connections with their secrets (encrypted when a key is set), "
            "and temporary transit files. Secrets never go back to the agent.")

d.pill(L, 16, GW, 48, "In: AI agents and apps that need your accounts")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Way in", 1)
d.column(L, T1, [("MCP|POST /mcp · 5 tools", "coding"),
                 ("HTTP API /v1|SDK · oo CLI · OpenAPI", "coding"),
                 ("Web Console|admin API /api", "plan")])
d.notes(L, T1, H1, "Same action IDs and schemas", "on every way in")

d.group(R, T1, GW, H1, "Checks", 2)
d.column(R, T1, [("Bearer token, when set|runtime token · JWT · admin", "review"),
                 ("Action rules|allow / block lists", "review"),
                 ("Pick a connection|which account to act as", "plan")])
d.notes(R, T1, H1, "A denied call stops here", "before any secret is read")

d.group(R, T2, GW, H2, "Run", 3)
d.column(R, T2, [("Check the input|against the action schema", "critic"),
                 ("Provider code|loaded the first time it runs", "coding"),
                 ("Guarded fetch|no private addresses", "review")])
d.notes(R, T2, H2, "Out to 1,000+ provider APIs,", "or to OOMOL Marketplace / SaaS")

d.group(L, T2, GW, H2, "Records", 4)
d.column(L, T2, [("Run log|redacted · last 5,000 by default", "data"),
                 ("Connections|secrets encrypted when a key is set", "write"),
                 ("Transit files|temporary uploads", "data")])
d.notes(L, T2, H2, "SQLite · PostgreSQL · Cloudflare D1", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="call", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="allowed", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="logged", at=(600, T2 + 164))

d.save(Path(__file__).with_name("diagram.svg"))
