"""midPoint's own security: sign in, check rights, run the change, record it.
Snake order: 1 sign in (top left) -> 2 check rights (top right) -> 3 run the change (bottom right) -> 4 record it (bottom left).
Drawn from Evolveum/midpoint at commit 160887ba (docs/security/authentication/flexible-authentication,
docs/security/security-policy, docs/security/authorization/configuration, docs/security/credentials,
docs/security/privilege-elevation.adoc, docs/security/power-of-attorney.adoc, docs/security/audit,
docs/repository/native-audit.adoc, repo/system-init/src/main/resources/config.xml).
Run: python3 security.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("midPoint's own security",
            "In: a person or a client calls midPoint through the web GUI, REST or the actuator endpoints. "
            "1 Sign in: the security policy, global and from the user's organization and archetype merged, "
            "picks an authentication sequence for each channel; the sequence runs modules such as login form, "
            "LDAP, SAML, OIDC and TOTP. Passwords are encrypted with AES by default, or hashed; password reset "
            "has its own channel. "
            "2 Check rights: authorization statements in roles allow or deny; what is not allowed is denied, "
            "and deny always wins. The GUI page or the service is checked first. A Superuser role holds one "
            "statement that allows everything. "
            "3 Run the change: a request check runs before mappings and policies, an execution check after "
            "recompute, with all its effects. Expressions can run as another user or with full privileges. "
            "An attorney can act on another user's approval work items. "
            "4 Record it: the audit trail writes a request record, an execution record and resource records; "
            "the shipped config.xml sends it to a PostgreSQL table and to the log file.")

d.pill(L, 16, GW, 48, "In: a call through the GUI · REST · actuator")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Sign in", 1)
d.column(L, T1, [("Security policy|global · org · archetype merged", "plan"),
                 ("Sequence|one per channel", "plan"),
                 ("Modules|form · LDAP · SAML · OIDC · TOTP …", "review")])
d.notes(L, T1, H1, "Passwords: AES-encrypted by default, or hashed", "Password reset has its own channel")

d.group(R, T1, GW, H1, "Check rights", 2)
d.column(R, T1, [("Statements in roles|allow or deny", "review"),
                 ("Default deny|deny always wins", "review"),
                 ("Page or service|GUI · REST checked first", "review")])
d.notes(R, T1, H1, "Superuser role: one statement allows all", "")

d.group(R, T2, GW, H2, "Run the change", 3)
d.column(R, T2, [("Request check|before mappings run", "review"),
                 ("Execution check|after recompute · all effects", "review"),
                 ("Elevated expressions|runAsRef · runPrivileged", "coding")])
d.notes(R, T2, H2, "Attorney: act on another's work items", "")

d.group(L, T2, GW, H2, "Record it", 4)
d.column(L, T2, [("Request record|as the user asked", "data"),
                 ("Execution record|as it ran · implied accounts", "data"),
                 ("Resource records|changes on the systems", "data"),
                 ("Audit trail|PostgreSQL table · log file", "write")], h=60, gap=14, first=60)

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="signed in", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="allowed", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="audit records", at=(600, T2 + 164))

d.save(Path(__file__).with_name("security.svg"))
