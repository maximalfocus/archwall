"""Gates without a hardened tool's token: GPG commit signing, the SSH agent, the Homebrew Execution Gate, and protected Git over HTTPS.
Drawn from automic-vault/automic-vault at commit d1011a5 (README.md GPG Signing and SSH Agent, docs/architecture.md Runtime Authorization and Secure defaults, docs/securing-git.md).
Run: python3 gates.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Signing, SSH and Homebrew",
            "1 GPG signing: Git hands the commit to av-gpg; the private key stays in the Keychain and Git never "
            "sees it; the gate offers Approval Required, its default, or Allow Signing. "
            "2 SSH agent, optional: av ssh-agent serves its own socket; each key has its own gate and policy; it "
            "signs in memory and private keys are never added to the system agent. "
            "3 Homebrew: an Execution Gate controls brew even when no secret is involved; its default, Read & Update, "
            "allows reads and brew update but not install, upgrade or remove. "
            "4 Git over HTTPS: av git is a protected HTTPS path that narrows use of the gh credential; it is still "
            "under validation.")

d.group(L, 16, GW, H1 + 68, "GPG signing", 1)
d.column(L, 16, [("av-gpg|Git hands it the commit", "coding"),
                 ("Key in the Keychain|Git never sees it", "write"),
                 ("Approval Required|default · or Allow Signing", "review")])

d.group(R, 16, GW, H1 + 68, "SSH agent, optional", 2)
d.column(R, 16, [("av ssh-agent|its own socket", "coding"),
                 ("One gate per key|each with its own policy", "review"),
                 ("Signs in memory|keys never in the system agent", "write")])

d.group(R, T2, GW, H2, "Homebrew", 3)
d.column(R, T2, [("Execution Gate|no secret involved", "review"),
                 ("Read & Update|default · reads + brew update", "plan"),
                 ("Install · upgrade · remove|not in the default", "review")])

d.group(L, T2, GW, H2, "Git over HTTPS", 4)
d.column(L, T2, [("av git|protected HTTPS path", "coding"),
                 ("Narrows the gh credential|for Git's network step", "review")])
d.notes(L, T2, H2, "Still under validation", "")

d.save(Path(__file__).with_name("gates.svg"))
