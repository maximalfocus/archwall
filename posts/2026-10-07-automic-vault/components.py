"""The pieces and where they run: the av CLI and helpers, the menu bar app, the iPhone app and relay, and how it is installed.
Drawn from automic-vault/automic-vault at commit d1011a5 (Cargo.toml [[bin]] targets, src/menu-helper/, src/ios/, src/approval_relay/, deploy/approval-relay/, docs/architecture.md, README.md Quickstart).
Run: python3 components.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("The pieces",
            "1 Command-line side, on the Mac: the av CLI in Rust is the Gate Client; small signed helpers are "
            "av-gpg, the Homebrew brew stub and the proxy helper; Isotopes are the hardened builds of tools. "
            "2 Menu bar app, on the Mac: written in Swift, it is the approval service; it alone owns the Keychain "
            "with secrets, policy and history, and starts at login as a macOS LaunchAgent. The CLI talks to it "
            "over authenticated XPC. "
            "3 Phone side, optional: the iPhone app approves or denies; the approval relay is a Rust server that "
            "passes encrypted messages over WebSocket and wakes the phone through Apple push notifications. "
            "4 Install: Automic Vault.app from a release or the Homebrew cask; Isotopes come from the signed "
            "Isotopes tap; the app installs its CLI with administrator approval.")

d.group(L, 16, GW, H1 + 68, "Command-line side", 1)
d.column(L, 16, [("av CLI|Rust · the Gate Client", "coding"),
                 ("Signed helpers|av-gpg · brew stub · proxy", "coding"),
                 ("Isotopes|hardened builds of tools", "coding")])
d.notes(L, 16, H1 + 68, "On your Mac", "")

d.group(R, 16, GW, H1 + 68, "Menu bar app", 2)
d.column(R, 16, [("Approval service|Swift", "review"),
                 ("Owns the Keychain|secrets · policy · history", "write"),
                 ("Starts at login|macOS LaunchAgent", "data")])
d.notes(R, 16, H1 + 68, "On your Mac", "")

d.group(R, T2, GW, H2, "Phone side, optional", 3)
d.column(R, T2, [("iPhone app|approve or deny", "review"),
                 ("Approval relay|Rust server · WebSocket", "data"),
                 ("Apple push|wakes the phone", "data")])

d.group(L, T2, GW, H2, "Install", 4)
d.column(L, T2, [("Automic Vault.app|release or Homebrew cask", "write"),
                 ("Isotopes tap|signed fork releases", "write"),
                 ("CLI install|with administrator approval", "review")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="XPC", at=(600, T1 + 188))
d.arrow(f"M{L + GW / 2} {T2}V{T1 + H1 + 2}", label="installs", at=(L + GW / 2, T1 + H1 + 24))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="encrypted", at=(R + 430, T1 + H1 + 24))

d.save(Path(__file__).with_name("components.svg"))
