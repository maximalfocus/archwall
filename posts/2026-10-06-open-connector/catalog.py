"""Providers and the catalog: from one folder per provider to what callers can discover.
Drawn from oomol-lab/open-connector at commit 20c6c44 (docs/catalog-format.md, AGENTS.md "Architecture",
docs/configuration.md, docs/runtime-api.md "Action Guides").
Run: python3 catalog.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Providers and the catalog",
            "1 Source: one folder per provider under src/providers, with definition.ts for actions, schemas and "
            "scopes, and executors.ts for the code that calls the provider's API. "
            "2 Build: npm run generate:catalog writes one JSON file per provider plus an index, and a generated "
            "registry maps each provider to a lazy import of its executors. "
            "3 Runtime: the index loads at startup for listing and search; a provider's code loads the first time "
            "one of its actions, its proxy or its credential check runs; keeping schemas on disk is an optional "
            "flag, OOMOL_CONNECT_CATALOG_LAZY_SCHEMAS. "
            "4 What callers see: an agent-readable guide per action, an OpenAPI document, and for each action "
            "whether it reads, writes or destroys, and whether it can run locally or is catalog only.")

d.pill(L, 16, GW, 48, "In: 1,000+ providers, one folder each")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Source", 1)
d.column(L, T1, [("definition.ts|actions · schemas · scopes", "plan"),
                 ("executors.ts|calls the provider API", "coding")])
d.notes(L, T1, H1, "src/providers/<service>/", "")

d.group(R, T1, GW, H1, "Build", 2)
d.column(R, T1, [("npm run generate:catalog|a JSON per provider + index", "write"),
                 ("Provider registry|service → lazy import", "write")])

d.group(R, T2, GW, H2, "Runtime", 3)
d.column(R, T2, [("Index at startup|list · search", "data"),
                 ("Provider code|loaded on first use", "coding"),
                 ("Schemas on disk|optional flag", "data")])
d.notes(R, T2, H2, "OOMOL_CONNECT_CATALOG_LAZY_SCHEMAS", "")

d.group(L, T2, GW, H2, "What callers see", 4)
d.column(L, T2, [("Action guide|agent.md per action", "write"),
                 ("OpenAPI|/openapi.json", "write"),
                 ("Labels|read · write · destructive", "data")])
d.notes(L, T2, H2, "Also: runs locally, or catalog only", "")

d.arrow(f"M{L + GW} {T1 + 140}H{R - 2}", label="generate", at=(600, T1 + 128))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="load", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="serve", at=(600, T2 + 164))

d.save(Path(__file__).with_name("catalog.svg"))
