"""Where Kong's config lives: change it, what it describes, store it, spread it to workers.
Snake order: 1 change it (top left) -> 2 what it describes (top right) -> 3 store it (bottom right) -> 4 spread to workers (bottom left).
Stage 3 shows its two stores side by side: they are options, picked with the database setting.
Drawn from Kong/kong at commit 8927af6 (kong/templates/kong_defaults.lua, kong.conf.default, kong/db/schema/entities,
kong/db/strategies/off/init.lua, kong/api/routes/config.lua, kong/global.lua, kong/runloop/handler.lua).
Run: python3 config.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Where the config lives",
            "In: an admin changes routes, plugins or upstreams. "
            "1 Change it: the Admin API listens on 127.0.0.1 port 8001, or 8444 with TLS, and should stay "
            "with admins; Kong Manager is a web UI on port 8002; a declarative config file is used with no database. "
            "2 What it describes: services and routes say where calls go, consumers and plugins say who calls "
            "and what runs, upstreams and targets list backend addresses; also certificates, SNIs, vaults and keys. "
            "3 Store it, one of two options picked with the database setting: Postgres, the default, where the "
            "Admin API edits each entity; or DB-less, database = off, where the config file is loaded into LMDB, "
            "the Admin API cannot create, update or delete single entities, and POST /config replaces the whole config. "
            "4 Spread to workers: each node keeps two memory caches of 128 MB each, nodes on Postgres poll for "
            "changes every 5 seconds, and every 5 seconds each worker rebuilds its router and plugin list if needed.")

d.pill(L, 16, GW, 48, "In: an admin changes routes · plugins · upstreams")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Change it", 1)
d.column(L, T1, [("Admin API|127.0.0.1:8001 · 8444 with TLS", "plan"),
                 ("Kong Manager|web UI · port 8002", "plan"),
                 ("Config file|declarative · for DB-less", "write")])
d.notes(L, T1, H1, "Keep the Admin API to admins", "")

d.group(R, T1, GW, H1, "What it describes", 2)
d.column(R, T1, [("Services · routes|where calls go", "data"),
                 ("Consumers · plugins|who calls · what runs", "data"),
                 ("Upstreams · targets|backend addresses", "data")])
d.notes(R, T1, H1, "Also certificates · SNIs · vaults · keys", "")

d.group(R, T2, GW, H2, "Store it", 3)
OW = 226
for x, cards in ((R + 30, [("Postgres|the default", "write"), ("Admin API|edits each entity", "plan")]),
                 (R + 30 + OW + 40, [("DB-less|database = off", "write"), ("Config file|loaded into LMDB", "write"),
                                     ("POST /config|replaces it all", "plan")])):
    for i, (label, kind) in enumerate(cards):
        d.card(x, T2 + 64 + i * 80, label, kind, w=OW)
d.note(R + 30 + OW + 20, T2 + 102, "or")
d.notes(R, T2, H2, "Pick one: the database setting", "DB-less: no edits to single entities")

d.group(L, T2, GW, H2, "Spread to workers", 4)
d.column(L, T2, [("Memory caches|two per node · 128 MB each", "data"),
                 ("Poll for changes|Postgres · every 5 s", "plan"),
                 ("Workers rebuild|router · plugin list every 5 s", "coding")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="describes", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="saved", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="loaded", at=(600, T2 + 164))

d.save(Path(__file__).with_name("config.svg"))
