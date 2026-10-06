"""Safety rails: who may manage, what a caller may do, how the layers stack, what leaves the box.
Drawn from oomol-lab/open-connector at commit 20c6c44 (docs/credentials.md, docs/configuration.md,
docs/runtime-api.md, AGENTS.md "Provider Network Egress", src/server/api/auth.ts).
Run: python3 safety.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Safety rails",
            "1 Admin side: OOMOL_CONNECT_ADMIN_TOKEN guards the admin API, the docs and the Web Console; "
            "set it whenever the Console is reachable beyond your machine; the server binds to 127.0.0.1 unless HOST is set to 0.0.0.0; runtime tokens are made there and shown once. "
            "2 Caller tokens: a persistent token carries its own grants for actions, proxies, connections and "
            "triggers; an empty proxy grant means no /v1/proxy calls, and an empty trigger grant means no triggers. "
            "3 Layers: deployment allow and block lists from environment variables, the runtime policy saved in the "
            "Console, and the token's grants; every layer must allow, a block always wins, and a token can only narrow. "
            "4 Data and egress: provider requests go through a guarded fetch that blocks private and cloud metadata "
            "addresses; private networks for self-hosted providers need the OOMOL_CONNECT_ALLOW_PRIVATE_NETWORK flag; "
            "stored secrets use AES-256-GCM only when OOMOL_CONNECT_ENCRYPTION_KEY is set.")

d.group(L, 16, GW, H1 + 68, "Admin side", 1)
d.column(L, 16, [("Admin token|guards /api · /docs · Console", "review"),
                 ("Binds to 127.0.0.1|HOST=0.0.0.0 to open it", "review"),
                 ("Runtime tokens|made here, shown once", "write")])
d.notes(L, 16, H1 + 68, "Set it whenever the Console", "is reachable beyond your machine")

d.group(R, 16, GW, H1 + 68, "Caller tokens", 2)
d.column(R, 16, [("Action rules|allow / block per token", "review"),
                 ("Proxy grant|empty = no /v1/proxy", "review"),
                 ("Connection grant|exact connection IDs", "review"),
                 ("Trigger grant|empty = no triggers", "review")], h=60, gap=14)

d.group(R, T2, GW, H2, "Layers", 3)
d.column(R, T2, [("Deployment|env allow / block lists", "plan"),
                 ("Runtime policy|saved in the Console", "plan"),
                 ("Token grants|can only narrow", "plan")])
d.notes(R, T2, H2, "Every layer must allow;", "a block always wins")

d.group(L, T2, GW, H2, "Data and egress", 4)
d.column(L, T2, [("Guarded fetch|blocks private · metadata IPs", "review"),
                 ("Private network|flag, self-hosted only", "review"),
                 ("Secrets at rest|AES-256-GCM, with a key", "write")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="issues", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {16 + H1 + 68}V{T2 - 2}", label="checked by", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="then", at=(600, T2 + 164))

d.save(Path(__file__).with_name("safety.svg"))
