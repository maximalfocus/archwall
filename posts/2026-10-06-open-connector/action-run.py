"""One action call, step by step: who is calling, is it allowed, run it, record it.
Drawn from oomol-lab/open-connector at commit 20c6c44 (docs/runtime-api.md, docs/credentials.md,
src/server/actions/action-runner.ts, src/core/execution.ts, src/server/api/auth.ts).
Run: python3 action-run.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("One action call",
            "In: one call, for example POST /v1/actions/github.get_current_user or the MCP tool execute_action. "
            "1 Who is calling: a bootstrap token from an environment variable, a persistent token made in the "
            "Console whose hash is all that is stored, or a JWT, which is Node only and needs three settings; sent as a bearer token when runtime authentication is configured. "
            "2 Is it allowed: the action rules of deployment, runtime and token; then the named connection, "
            "or the default one; then the token's connection grant. A denial is a 403 before any secret is read. "
            "3 Run: the input is checked against the action's JSON schema, then the local provider code runs, "
            "or the call goes to the Marketplace or to SaaS; local provider requests time out after 30 seconds. "
            "4 Record: a redacted run log entry; with an Idempotency-Key header, HTTP only, a retry within "
            "24 hours replays the first answer; the answer carries the data and an executionId.")

d.pill(L, 16, GW, 48, "In: POST /v1/actions/<id> or MCP execute_action")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Who is calling", 1)
d.column(L, T1, [("Bootstrap token|from an env variable", "review"),
                 ("Persistent token|oct_… · only its hash stored", "review"),
                 ("JWT|Node only · needs 3 settings", "review")])
d.notes(L, T1, H1, "Sent as Authorization: Bearer,", "when runtime auth is configured")

d.group(R, T1, GW, H1, "Is it allowed", 2)
d.column(R, T1, [("Action rules|deployment · runtime · token", "review"),
                 ("Pick a connection|named, or the default", "plan"),
                 ("Connection grant|the token's allowed IDs", "review")])
d.notes(R, T1, H1, "No → 403, before any secret is read", "")

d.group(R, T2, GW, H2, "Run", 3)
d.column(R, T2, [("Check the input|JSON schema · else 400", "critic"),
                 ("Local provider code|or Marketplace / SaaS", "coding"),
                 ("Provider API|30 s timeout, local code", "coding")])

d.group(L, T2, GW, H2, "Record and answer", 4)
d.column(L, T2, [("Run log|input and output redacted", "data"),
                 ("Idempotency-Key, HTTP only|retry replays for 24 h", "write"),
                 ("Answer|data + executionId", "data")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="token ok", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="allowed", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="result", at=(600, T2 + 164))

d.save(Path(__file__).with_name("action-run.svg"))
