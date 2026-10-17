"""Jump host overview: reach the one door, prove who you are, hop to the target, keep a record.
Snake order: 1 reach the door (top left) -> 2 prove who you are (top right) -> 3 hop (bottom right)
-> 4 keep a record (bottom left).
Drawn from openssh/openssh-portable at commit 6a46ea6 (ssh.1 -J, ssh_config.5 ProxyJump, sshd_config.5,
auth.c auth_log) and aws-ia/cfn-ps-linux-bastion at commit 213dd9a (templates/, scripts/, docs/).
Run: python3 diagram.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Jump host overview",
            "In: an admin outside needs a server on a private network. "
            "1 Reach the door: the jump host is the one way in; the firewall lets in port 22 only from "
            "allowed addresses, or, in AWS's reference setup by default, no port is open and you come in "
            "through AWS Session Manager. "
            "2 Prove who you are: keys or certificates instead of passwords, a second factor with "
            "AuthenticationMethods, and only the users AllowUsers lists. "
            "3 Hop to the target: pass straight through with ssh -J (ProxyJump), or log in to the jump host "
            "and go on from its shell; the servers sit in the private subnets. "
            "4 Keep a record: sshd logs who signed in, with which key and from where; AWS's setup copies "
            "the audit log to CloudWatch; an optional banner warns that sessions are recorded.")

d.pill(L, 16, GW, 48, "In: an admin outside needs a private server")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Reach the door", 1)
d.column(L, T1, [("Jump host|the one way in", "coding"),
                 ("Firewall|port 22 from allowed IPs only", "review"),
                 ("Or no open port|AWS Session Manager", "plan")])

d.group(R, T1, GW, H1, "Prove who you are", 2)
d.column(R, T1, [("Keys or certificates|no passwords", "review"),
                 ("Second factor|AuthenticationMethods", "review"),
                 ("Only listed users|AllowUsers", "plan")])

d.group(R, T2, GW, H2, "Hop to the target", 3)
d.column(R, T2, [("Pass straight through|ssh -J · ProxyJump", "coding"),
                 ("Or log in, then hop|from the jump host's shell", "coding"),
                 ("Your servers|in the private subnets", "data")])

d.group(L, T2, GW, H2, "Keep a record", 4)
d.column(L, T2, [("sshd log|who · which key · from where", "data"),
                 ("Audit log|copied to CloudWatch (AWS)", "write"),
                 ("Banner (option)|sessions are recorded", "review")])

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="a connection", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="signed in", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="who · what", at=(600, T2 + 164))

d.save(Path(__file__).with_name("diagram.svg"))
