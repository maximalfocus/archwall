"""One request, from ask to release, following the authorization flow in docs/architecture.md.
Drawn from automic-vault/automic-vault at commit d1011a5 (docs/architecture.md Authorization flow, Policy model, Denial precedence, Recording before release; README.md Authorization Gates).
Run: python3 request.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("One request",
            "In: an AI agent with Read Only access runs gh issue create. "
            "1 Who is asking: the Launcher, here the agent app; the Gate Client, the signed piece that sends the "
            "request; and the Target, the program that will use the secret. Client and Target are kept apart. "
            "2 Check: the Launcher's identity from its live code signature; the complete request, meaning command, "
            "arguments, folder and secret names; and denial rules, which are checked first. Any failed check denies. "
            "3 Decide: a Blessing, the gate's policy or a Temporary Access Grant may allow it; an unknown or too "
            "broad operation needs Approval, which can allow or deny. With Read Only, gh issue create needs Approval. "
            "4 Release: the Authorization Record is saved and read back, then the secret is applied or the Target "
            "runs, and the menu bar shows the live use.")

d.pill(L, 16, GW, 48, "In: an agent with Read Only runs gh issue create")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Who is asking", 1)
d.column(L, T1, [("Launcher|the agent app", "coding"),
                 ("Gate Client|signed · sends the request", "coding"),
                 ("Target|the program that uses the secret", "coding")])
d.notes(L, T1, H1, "Client and Target are kept apart", "")

d.group(R, T1, GW, H1, "Check", 2)
d.column(R, T1, [("Launcher identity|live code signature", "review"),
                 ("The whole request|command · folder · secret names", "review"),
                 ("Denial rules|checked first", "review")])
d.notes(R, T1, H1, "Any failed check → denied", "")

d.group(R, T2, GW, H2, "Decide", 3)
d.column(R, T2, [("Blessing · policy · grant|may allow it", "plan"),
                 ("Unknown or too broad|needs Approval", "review"),
                 ("Approval|allow or deny", "review")])
d.notes(R, T2, H2, "Read Only + issue create → Approval", "")

d.group(L, T2, GW, H2, "Release", 4)
d.column(L, T2, [("Authorization Record|saved and read back", "write"),
                 ("Apply the secret|or run the Target", "coding"),
                 ("Live use|shown in the menu bar", "data")])

A1, A2, A3 = "request", "verified", "allowed"
d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label=A1, at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label=A2, at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label=A3, at=(600, T2 + 164))

d.save(Path(__file__).with_name("request.svg"))
