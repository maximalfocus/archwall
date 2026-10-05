"""Grafana: who gets in and what they may do.  Drawn from grafana/grafana at commit 6b6eaf7:
pkg/services/authn (clients; login form and basic auth on, anonymous, auth proxy and JWT off by default),
pkg/login/social/social.go (GitHub, GitLab, Google, Azure AD, Okta, generic OAuth, Grafana.com; all off by default),
SAML only as Enterprise (docs configure-access/configure-authentication/saml), pkg/components/satokengen (glsa_
tokens), pkg/apimachinery/identity/role_type.go (None, Viewer, Editor, Admin), ossaccesscontrol (folder and
dashboard permissions; data source permissions are a no-op in OSS), pkg/services/secrets (envelope encryption,
secret_key default in conf/defaults.ini, external KMS Enterprise), pkg/api/pluginproxy/ds_proxy.go.

Snake order: 1 sign in -> 2 who you are -> 3 what you may do -> 4 secrets kept safe.
Run: python3 access.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 416
T2, H2 = 456, 404


def col(x, top, cards, h=72, gap=24, arrows=True):
    """One column of wide cards, top to bottom, optionally joined by arrows."""
    for i, (lbl, kind) in enumerate(cards):
        y = top + 64 + i * (h + gap)
        d.card(x + 30, y, lbl, kind, w=492, h=h)
        if arrows and i:
            d.arrow(f"M{x + W / 2} {y - gap}V{y - 2}")


def notes(x, top, hgt, *lines):
    """Up to two note lines at the foot of a group."""
    for i, s in enumerate(lines):
        d.note(x + W / 2, top + hgt - 22 - (len(lines) - 1 - i) * 26, s)


def handoffs(a, b, c, ya=T1 + 206, yc=T2 + 200):
    """Arrows between the four groups in snake order, with what each one carries."""
    if a:
        d.arrow(f"M{L + W} {ya}H{R - 2}", label=a, at=(600, ya - 12))
    if b:
        d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label=b, at=(R + W / 2 + 14 + len(b) * 4.6, T1 + H1 + 21))
    if c:
        d.arrow(f"M{R} {yc}H{L + W + 2}", label=c, at=(600, yc - 12))

d = Diagram("Grafana: who gets in and what they may do",
            "1 Sign in: a username and password, checked against Grafana's own users or LDAP; single sign-on with "
            "GitHub, GitLab, Google, Azure AD, Okta or any OAuth provider; tokens for scripts. SAML is Enterprise; "
            "anonymous access, JWT and an auth proxy are off by default. "
            "2 Who you are: a user in one or more organisations, which are separate spaces inside one server; teams "
            "group users; service accounts are for scripts and have no login. "
            "3 What you may do: one role per organisation (None, Viewer, Editor or Admin), rights on each folder and "
            "dashboard, and a server admin who manages every organisation. Custom roles and data source rights are "
            "Enterprise. "
            "4 Secrets kept safe: data source passwords are encrypted before saving and never sent to the browser; "
            "the server adds them to each call. Change the default secret_key, which is the same in every install. "
            "External key vaults are Enterprise.")

d.group(L, T1, W, H1, "Sign in", 1)
col(L, T1, [("Username + password|Grafana's own users, or LDAP", "review"),
            ("Single sign-on|GitHub, Google, Okta, Azure AD ...", "review"),
            ("Tokens for scripts|service account tokens", "review")], arrows=False)
notes(L, T1, H1, "SAML: Enterprise · anonymous, JWT,", "auth proxy: off by default")

d.group(R, T1, W, H1, "Who you are", 2)
col(R, T1, [("User|in one or more organisations", "data"),
            ("Team|a group of users", "data"),
            ("Service account|for scripts, no login", "data")], arrows=False)
notes(R, T1, H1, "organisations are separate", "spaces inside one server")

d.group(R, T2, W, H2, "What you may do", 3)
col(R, T2, [("Role per organisation|None · Viewer · Editor · Admin", "review"),
            ("Folder and dashboard rights|view, edit, admin", "review"),
            ("Server admin|manages every organisation", "review")], gap=20, arrows=False)
notes(R, T2, H2, "custom roles, data source rights: Enterprise")

d.group(L, T2, W, H2, "Secrets kept safe", 4)
col(L, T2, [("Data source passwords|encrypted before saving", "write"),
            ("Never sent to the browser|the server adds them to calls", "review"),
            ("Change secret_key|the default is the same everywhere", "review")], gap=20, arrows=False)
notes(L, T2, H2, "external key vaults: Enterprise")

handoffs("identity", "role and rights", None)

d.save(Path(__file__).with_name("access.svg"))
