"""Access rules: Access Levels, per-gate defaults and launcher rules, the gh Read Only example, and short-lived grants and denials.
Drawn from automic-vault/automic-vault at commit d1011a5 (docs/authorization.md Access Levels, docs/architecture.md Policy model, Denial precedence and Secure defaults, README.md Authorization Gates and Temporary Access Grants).
Run: python3 policy.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Access rules",
            "1 Access Levels, presets a gate offers: Approval Required asks every time, Read Only allows recognized "
            "reads, Write Access allows recognized reads and writes, and Full Access may allow recognized sensitive "
            "operations; some gates add Read & Update (Homebrew) or Local Write between them. "
            "2 Per gate: each gate has a default level, new secret gates start at Read Only, rules for a Verified "
            "Launcher override the default, and unknown operations need Approval at every level. "
            "3 Example, one GitHub token at Read Only: gh issue list is allowed automatically, gh issue create needs "
            "Approval, and gh auth token, which shows the secret, needs Approval. "
            "4 Short-lived changes: a Temporary Access Grant gives Write Access for ten active minutes to one gate, "
            "launcher and agent task; denial rules are checked before anything that allows; a temporary denial "
            "blocks one launcher at one gate for two minutes.")

d.group(L, 16, GW, H1 + 68, "Access Levels", 1)
d.column(L, 16, [("Approval Required|asks every time", "review"),
                 ("Read Only|recognized reads", "plan"),
                 ("Write Access|recognized reads and writes", "plan"),
                 ("Full Access|sensitive operations too", "plan")], h=60, gap=14)
d.notes(L, 16, H1 + 68, "Some gates add Read & Update", "or Local Write")

d.group(R, 16, GW, H1 + 68, "Per gate", 2)
d.column(R, 16, [("Gate default|Read Only for new secret gates", "plan"),
                 ("Launcher rules|override the default", "plan"),
                 ("Unknown operation|always needs Approval", "review")])

d.group(R, T2, GW, H2, "Example: gh at Read Only", 3)
d.column(R, T2, [("gh issue list|allowed automatically", "plan"),
                 ("gh issue create|needs Approval", "review"),
                 ("gh auth token|shows the secret · Approval", "review")])

d.group(L, T2, GW, H2, "Short-lived changes", 4)
d.column(L, T2, [("Temporary Access Grant|Write for 10 min · one agent task", "plan"),
                 ("Denial rules|checked before any allow", "review"),
                 ("Temporary denial|one launcher · 2 minutes", "review")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="pick one", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {16 + H1 + 68}V{T2 - 2}", label="e.g.", at=(R + 430, T1 + H1 + 24))

d.save(Path(__file__).with_name("policy.svg"))
