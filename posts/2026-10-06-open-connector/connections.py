"""Connections: which account a call acts as, and where its secret lives.
Drawn from oomol-lab/open-connector at commit 20c6c44 (docs/credentials.md, docs/marketplace.md,
docs/saas-oauth.md, src/connection-service.ts resolveForExecution).
Run: python3 connections.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Connections",
            "In: a call names a connection, or none. "
            "1 Pick: a named connection must exist and is never swapped for another; with no name, the stored "
            "default comes first, then no_auth, then the Marketplace; a token can be limited to some connection IDs. "
            "2 Stored here: API key or custom fields that each provider declares, and OAuth2 through your own "
            "OAuth app, refreshed automatically when the provider gave a refresh token. Secrets sit in the runtime "
            "database, encrypted only when OOMOL_CONNECT_ENCRYPTION_KEY is set. "
            "3 Nothing stored: no_auth providers such as Hacker News, and Marketplace actions run by OOMOL with one "
            "Marketplace API key; only the action ID and input are sent. "
            "4 Kept on SaaS: an OAuth account authorised through an OOMOL SaaS project; its tokens stay on SaaS "
            "and its actions run there. Agents only ever see an account label, never a secret.")

d.pill(L, 16, GW, 48, "In: a call names a connection, or none")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Pick", 1)
d.column(L, T1, [("Named|must exist · no fallback", "plan"),
                 ("No name|default → no_auth → Marketplace", "plan"),
                 ("Token grant|only the allowed IDs", "review")])
d.notes(L, T1, H1, "Agents see an account label,", "never the secret")

d.group(R, T1, GW, H1, "Stored here", 2)
d.column(R, T1, [("API key · custom|fields the provider declares", "write"),
                 ("OAuth2|your own OAuth app", "write"),
                 ("Auto refresh|when a refresh token exists", "coding")])
d.notes(R, T1, H1, "Encrypted only with", "OOMOL_CONNECT_ENCRYPTION_KEY")

d.group(R, T2, GW, H2, "Nothing stored", 3)
d.column(R, T2, [("no_auth|e.g. Hacker News", "data"),
                 ("Marketplace|actions run by OOMOL", "coding"),
                 ("One Marketplace key|sends only action + input", "review")])

d.group(L, T2, GW, H2, "Kept on SaaS", 4)
d.column(L, T2, [("SaaS OAuth account|via an OOMOL project key", "write"),
                 ("Tokens stay on SaaS|only a reference here", "data"),
                 ("Runs remotely|no local fallback", "coding")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="local", at=(600, T1 + 188))
d.arrow(f"M{L + GW} {T1 + 290}H600V{T2 + 100}H{R - 2}", label="virtual", at=(600, T1 + H1 + 24))
d.arrow(f"M{L + GW / 2} {T1 + H1}V{T2 - 2}", label="SaaS", at=(L + GW / 2, T1 + H1 + 24))

d.save(Path(__file__).with_name("connections.svg"))
