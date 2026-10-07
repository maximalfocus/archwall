"""Secrets and history: where secret bytes live, which value a request gets, the release rules, and the local Authorization History.
Drawn from automic-vault/automic-vault at commit d1011a5 (docs/architecture.md Secret custody and availability, Recording before release; README.md Secrets and Authorization History; docs/project-secrets.md).
Run: python3 custody.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Secrets and history",
            "1 Stored in the Keychain: secret bytes sit in the app's private group of the macOS Data Protection "
            "Keychain; gate policy and the history key each sit in a separate Keychain service. "
            "2 Which value: the nearest Project Value in the working folder or a folder above it on the same "
            "volume wins, otherwise the Global Value; if the chosen value cannot be read the request is denied, with no "
            "fallback. The folder only picks a value and grants nothing. "
            "3 Release rules: there is no call that simply loads a secret; an allowed use is recorded and read back "
            "before the secret leaves; on a locked Mac only secrets marked available while locked can be used. "
            "4 History: encrypted rows in one SQLite file on this Mac, kept up to 30 days or until a size cap, 25 MiB by default, "
            "whichever comes first; reading it with av history needs Approval or a separate grant. It is not tamper-proof.")

d.group(L, 16, GW, H1 + 68, "Stored in the Keychain", 1)
d.column(L, 16, [("Secret bytes|app-only Keychain group", "write"),
                 ("Gate policy|separate Keychain service", "write"),
                 ("History key|separate Keychain service", "write")])

d.group(R, 16, GW, H1 + 68, "Which value", 2)
d.column(R, 16, [("Project Value|nearest folder at or above · same volume", "data"),
                 ("Global Value|when no Project Value", "data"),
                 ("Read fails|denied · no fallback", "review")])
d.notes(R, 16, H1 + 68, "The folder picks a value,", "it grants nothing")

d.group(R, T2, GW, H2, "Release rules", 3)
d.column(R, T2, [("No 'just load it' call|only after a decision", "review"),
                 ("Record before release|saved and read back", "write"),
                 ("Mac locked|only if available while locked", "data")])

d.group(L, T2, GW, H2, "History", 4)
d.column(L, T2, [("Encrypted SQLite|on this Mac only", "data"),
                 ("Up to 30 days|or 25 MiB by default", "data"),
                 ("av history|needs Approval or a grant", "review")])
d.notes(L, T2, H2, "Not tamper-proof", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="secret", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {16 + H1 + 68}V{T2 - 2}", label="chosen value", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="record", at=(600, T2 + 164))

d.save(Path(__file__).with_name("custody.svg"))
