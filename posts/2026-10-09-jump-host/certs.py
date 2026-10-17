"""SSH user certificates for a jump host: set up a CA, sign a user's key, sign in, revoke.
Snake order: 1 set up a CA (top left) -> 2 sign a key (top right) -> 3 sign in (bottom right)
-> 4 revoke (bottom left).
Drawn from openssh/openssh-portable at commit 6a46ea6 (ssh-keygen.1 CERTIFICATES, -s -I -n -V -k;
sshd_config.5 TrustedUserCAKeys, RevokedKeys; auth.c format_method_key).
Run: python3 certs.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("SSH certificates for a jump host",
            "In: many people and many servers; trust one certificate authority instead of copying each "
            "person's key around. "
            "1 Set up a CA: a CA key signs user keys; sshd's TrustedUserCAKeys lists the CA, so the server "
            "trusts the CA, not each key. A certificate with no principals is refused. "
            "2 Sign a user's key: ssh-keygen -s with the CA key signs the user's public key; -I sets a key ID "
            "that shows in the logs; -n names the principals, usually user names; -V sets when it is valid. "
            "3 Sign in: the laptop offers the key and its certificate; sshd checks the CA signature, the name "
            "and the dates; the log line names the key ID, serial and CA. "
            "4 Revoke: ssh-keygen -k writes a key revocation list; sshd's RevokedKeys refuses every key in "
            "it. If that file can't be read, all key logins are refused; replace it whole, never edit it in "
            "place.")

d.pill(L, 16, GW, 48, "In: trust one CA, not every person's key")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Set up a CA", 1)
d.column(L, T1, [("CA key|signs user keys", "write"),
                 ("TrustedUserCAKeys|sshd trusts the CA", "review")])
d.notes(L, T1, H1, "A certificate with no principals is refused", "")

d.group(R, T1, GW, H1, "Sign a user's key", 2)
d.column(R, T1, [("ssh-keygen -s ca_key|signs the user's public key", "write"),
                 ("-I key ID|shows in the logs", "data"),
                 ("-n names · -V validity|who it is for · until when", "plan")])

d.group(R, T2, GW, H2, "Sign in", 3)
d.column(R, T2, [("Laptop|offers key and certificate", "coding"),
                 ("sshd checks|CA signature · name · dates", "review"),
                 ("Log line|key ID · serial · CA", "data")])

d.group(L, T2, GW, H2, "Revoke", 4)
d.column(L, T2, [("ssh-keygen -k|writes a revocation list", "write"),
                 ("RevokedKeys|sshd refuses what is listed", "review")])
d.notes(L, T2, H2, "File unreadable: every key login refused", "Replace it whole, never edit in place")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="trusted CA", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="certificate", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="a key to stop", at=(600, T2 + 164))

d.save(Path(__file__).with_name("certs.svg"))
