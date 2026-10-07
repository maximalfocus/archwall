"""Human Approval: on the Mac, with Touch ID, or on an iPhone through an encrypted relay; the Mac checks every answer.
Drawn from automic-vault/automic-vault at commit d1011a5 (docs/architecture.md iPhone Approval, Touch ID Approval and Secret custody and availability, docs/authorization.md, README.md).
Run: python3 approval.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Human Approval",
            "In: a request that policy cannot allow. "
            "1 On the Mac: an Approval window shows the complete request and the chain of programs behind it; "
            "optional Touch ID needs a fresh fingerprint each time. Mac approval needs an active session and awake "
            "displays. "
            "2 On an iPhone, optional: the iPhone app on the same iCloud Keychain account; an encrypted relay server "
            "passes requests and answers but cannot read or forge them; allowing needs a subscription, denying does not. "
            "3 The Mac checks the answer: it must match the exact request, the first valid answer wins and replays "
            "are rejected, and the record is saved before release. "
            "4 Limits: when the Mac is locked only secrets marked available while locked can be used; with iPhone "
            "Approval on, the Mac has no click-to-allow; if the phone or relay is unreachable the request fails "
            "closed unless Touch ID Approval is also enabled.")

d.pill(L, 16, GW, 48, "In: a request policy cannot allow")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "On the Mac", 1)
d.column(L, T1, [("Approval window|full request + program chain", "review"),
                 ("Touch ID, optional|fresh fingerprint each time", "review")])
d.notes(L, T1, H1, "Needs an active session", "and awake displays")

d.group(R, T1, GW, H1, "On an iPhone, optional", 2)
d.column(R, T1, [("iPhone app|same iCloud Keychain account", "review"),
                 ("Encrypted relay|can't read or forge requests", "data"),
                 ("Subscription|needed to allow · not to deny", "data")])

d.group(R, T2, GW, H2, "The Mac checks the answer", 3)
d.column(R, T2, [("Exact match|bound to this request", "review"),
                 ("First valid answer wins|replays rejected", "review"),
                 ("Record · then release", "write")])

d.group(L, T2, GW, H2, "Limits", 4)
d.column(L, T2, [("Mac locked|only secrets available while locked", "data"),
                 ("iPhone Approval on|no click-to-allow on the Mac", "review"),
                 ("Phone or relay down|fails closed unless Touch ID", "review")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="or", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="answer", at=(R + 430, T1 + H1 + 24))

d.save(Path(__file__).with_name("approval.svg"))
