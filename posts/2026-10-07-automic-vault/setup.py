"""Set up: detect exposed credentials, harden the tool, install Isotopes where needed, verify.
Drawn from automic-vault/automic-vault at commit d1011a5 (docs/tool-hardening.md, docs/architecture.md Exposure Detection and Tool Hardening, README.md, src/isotopes/).
Run: python3 setup.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Set up a tool",
            "1 Detect: Detectors check over 100 developer-tool configurations and report each Finding, an "
            "Exposure or a Hazard, with a fix; they never use a secret, and a clean scan is not a guarantee. "
            "2 Harden: a Hardener moves the credential from a file or helper into the macOS Data Protection "
            "Keychain and changes how the tool asks for it, through a credential helper, a wrapper or an Isotope; "
            "examples are gh, aws, docker and Homebrew. "
            "3 Isotopes: an Isotope is an Automic Vault-compatible build of a tool; signed fork releases are pinned "
            "in the Isotopes Homebrew tap, some vendor releases are kept signed in a protected folder under /opt/av, "
            "and without Homebrew executable-only Isotopes are verified and installed directly. "
            "4 Verify: av doctor checks identity, ownership, permissions and which command runs first; wrappers "
            "guard only the command path they sit on, not every way to run a program.")

d.group(L, 16, GW, H1 + 68, "Detect", 1)
d.column(L, 16, [("Detectors|100+ tool configurations", "critic"),
                 ("Findings|exposure or hazard + a fix", "data")])
d.notes(L, 16, H1 + 68, "Read only: never uses a secret", "A clean scan is not a guarantee")

d.group(R, 16, GW, H1 + 68, "Harden", 2)
d.column(R, 16, [("Move the secret|file → macOS Keychain", "write"),
                 ("Change how the tool asks|helper · wrapper · Isotope", "coding"),
                 ("Examples|gh · aws · docker · Homebrew", "data")])

d.group(R, T2, GW, H2, "Isotopes", 3)
d.column(R, T2, [("Isotope|an AV-compatible build", "coding"),
                 ("Signed fork releases|pinned in a Homebrew tap", "write"),
                 ("Some vendor releases|kept signed under /opt/av", "write")])
d.notes(R, T2, H2, "No Homebrew: verified, installed directly", "")

d.group(L, T2, GW, H2, "Verify", 4)
d.column(L, T2, [("av doctor|identity · owner · permissions", "review"),
                 ("Which command runs|the protected one first", "review")])
d.notes(L, T2, H2, "Wrappers guard their own path,", "not every way to run a program")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="findings", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {16 + H1 + 68}V{T2 - 2}", label="installs", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="then", at=(600, T2 + 164))

d.save(Path(__file__).with_name("setup.svg"))
