"""Automic Vault overview: set up once, then every protected command is asked, decided, recorded and released.
Snake order: 1 set up (top left) -> 2 a command asks (top right) -> 3 decide (bottom right) -> 4 record and release (bottom left).
Drawn from automic-vault/automic-vault at commit d1011a5 (README.md, docs/architecture.md, docs/choosing-a-mechanism.md).
Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Automic Vault overview",
            "In: you, a terminal or an AI agent runs a tool such as gh, aws or brew on a Mac. "
            "1 Set up once: av scan checks over 100 developer-tool configurations for exposed credentials, "
            "av harden moves a supported tool's credentials into the macOS Keychain and changes how the tool asks "
            "for them, and av doctor checks that protection. "
            "2 A command asks: the Launcher (a terminal, IDE or agent app) starts the tool, a signed Automic Vault "
            "Gate Client sends the request, and the tool's Authorization Gate on the Mac receives it. "
            "3 Decide: the Mac checks the Launcher's live code signature, applies the gate's default Access Level or a rule for that "
            "Launcher, and asks for Approval on the Mac, with Touch ID or on an iPhone when policy cannot allow it; "
            "unknown operations always need Approval. "
            "4 Record and release: an Authorization Record is saved and read back first, then the secret goes to "
            "the program that needs it; with no record there is no secret.")

d.pill(L, 16, GW, 48, "In: you or an AI agent runs gh, aws, brew …")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Set up once", 1)
d.column(L, T1, [("av scan|finds exposed credentials", "critic"),
                 ("av harden <tool>|moves them into the Keychain", "write"),
                 ("av doctor|checks the protection", "review")])
d.notes(L, T1, H1, "Over 100 tool configurations checked", "")

d.group(R, T1, GW, H1, "A command asks", 2)
d.column(R, T1, [("Launcher|terminal · IDE · agent app", "coding"),
                 ("Gate Client|signed piece that sends the request", "coding"),
                 ("Authorization Gate|one per tool · on the Mac", "review")])

d.group(R, T2, GW, H2, "Decide", 3)
d.column(R, T2, [("Who is asking?|live code signature check", "review"),
                 ("Access Level|gate default or launcher rule", "plan"),
                 ("Approval|Mac · Touch ID · iPhone", "review")])
d.notes(R, T2, H2, "Unknown operations always ask", "")

d.group(L, T2, GW, H2, "Record and release", 4)
d.column(L, T2, [("Record first|saved and read back", "write"),
                 ("Secret to the program|e.g. gh gets its token", "coding"),
                 ("Keychain|the secret stays here otherwise", "data")])
d.notes(L, T2, H2, "No record, no secret", "")

A1, A2, A3 = "later", "request", "allowed"
d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label=A1, at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label=A2, at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label=A3, at=(600, T2 + 164))

d.save(Path(__file__).with_name("diagram.svg"))
