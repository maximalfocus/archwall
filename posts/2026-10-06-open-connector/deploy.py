"""Where it runs: a Node server, Cloudflare Workers, a library inside your app, or OOMOL hosted.
Drawn from oomol-lab/open-connector at commit 20c6c44 (README.md, docs/configuration.md, docs/cloudflare.md,
docs/single-binary.md, docs/headless.md, deploy/helm/open-connector/README.md, docs/fly-io.md).
Run: python3 deploy.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Where it runs",
            "1 Node server: the Docker image from GHCR on port 3000, a single binary for six platforms built "
            "with Bun, or the Helm chart and Fly.io, both from that Dockerfile; SQLite by default, PostgreSQL 15 or newer with a database URL, "
            "and transit files on local disk or S3. "
            "2 Cloudflare: Workers run it, D1 keeps the records, R2 or Workers KV keeps transit files, and a "
            "once-a-minute cron does cleanup. "
            "3 Inside your app: the npm package @oomol-lab/open-connector; your server owns HTTP, configuration "
            "and the process; there is no Web Console and one runtime per process. "
            "4 OOMOL hosted: OOMOL's OAuth apps and runtime, with the same provider and action IDs, so you can "
            "move to self-hosting later.")

d.group(L, 16, GW, H1 + 68, "Node server", 1)
d.column(L, 16, [("Docker image|ghcr.io · port 3000", "coding"),
                 ("Single binary|6 platforms · built with Bun", "coding"),
                 ("Helm chart · Fly.io|same Dockerfile", "coding")])
d.notes(L, 16, H1 + 68, "SQLite by default · PostgreSQL 15+", "transit files: local disk or S3")

d.group(R, 16, GW, H1 + 68, "Cloudflare", 2)
d.column(R, 16, [("Workers|runs the gateway", "coding"),
                 ("D1|records", "write"),
                 ("R2 or Workers KV|transit files", "write")])
d.notes(R, 16, H1 + 68, "Cron once a minute for cleanup", "")

d.group(R, T2, GW, H2, "Inside your app", 3)
d.column(R, T2, [("npm library|@oomol-lab/open-connector", "coding"),
                 ("Your server|owns HTTP · config · process", "plan")])
d.notes(R, T2, H2, "No Web Console;", "one runtime per process")

d.group(L, T2, GW, H2, "OOMOL hosted", 4)
d.column(L, T2, [("OAuth apps ready|no app setup", "plan"),
                 ("Hosted runtime|managed by OOMOL", "coding")])
d.notes(L, T2, H2, "Same provider and action IDs:", "move to self-hosting later")

d.save(Path(__file__).with_name("deploy.svg"))
