"""Other ways to use a secret when a hardened tool does not fit: Blessed Scripts, av inject, the Secret Proxy, and Varlock.
Drawn from automic-vault/automic-vault at commit d1011a5 (docs/choosing-a-mechanism.md, README.md Scripting and Credential Proxies, docs/direct-secret-access.md, docs/secret-proxy.md, docs/varlock.md).
Run: python3 mechanisms.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Other ways to use a secret",
            "1 Blessed Scripts: av bless reviews a script once; the script declares the secret names and tool "
            "capabilities it needs; editing it ends the Blessing. "
            "2 av inject: puts named secrets into a program's environment; --mode=fd hands each secret through its "
            "own pipe and needs fresh Approval every time; a Direct Access Rule lets one launcher use one secret name "
            "with any program, the broadest and least preferred option. "
            "3 Secret Proxy: av proxy gives the app a random stand-in reference; a separately signed proxy helper "
            "puts the real secret into outbound HTTPS requests only for destinations you approve, for that session; "
            "the references are still bearer values. "
            "4 Varlock, optional: the Varlock plugin asks for all its secrets in one request, with one Approval per run and no "
            "standing rules or Blessings.")

d.pill(L, 16, GW, 48, "In: a hardened tool does not fit")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Blessed Scripts", 1)
d.column(L, T1, [("av bless|review a script once", "plan"),
                 ("It declares its needs|secret names · tool capabilities", "plan"),
                 ("Edit the script|the Blessing ends", "review")])

d.group(R, T1, GW, H1, "av inject", 2)
d.column(R, T1, [("Environment|secrets as variables", "coding"),
                 ("--mode=fd|one pipe per secret · ask each time", "coding"),
                 ("Direct Access Rule|one name · one launcher · broad", "review")])
d.notes(R, T1, H1, "Least preferred: the program", "gets the secret itself")

d.group(R, T2, GW, H2, "Secret Proxy", 3)
d.column(R, T2, [("av proxy|the app gets a stand-in", "coding"),
                 ("Proxy helper|swaps in the real secret", "coding"),
                 ("Approved destinations|for this session only", "review")])
d.notes(R, T2, H2, "Stand-ins are still bearer values", "")

d.group(L, T2, GW, H2, "Varlock, optional", 4)
d.column(L, T2, [("Varlock plugin|all its secrets in one request", "coding"),
                 ("One Approval per run|no rules or Blessings", "review")])

d.save(Path(__file__).with_name("mechanisms.svg"))
