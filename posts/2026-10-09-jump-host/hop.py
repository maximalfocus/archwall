"""Two ways through a jump host, side by side: pass straight through (ProxyJump) or log in, then hop.
Options, not steps: the two top groups are alternatives; the bottom group is client config for both.
Drawn from openssh/openssh-portable at commit 6a46ea6 (ssh.1 -J and -W, ssh_config.5 ProxyJump and
ForwardAgent, ssh.c ProxyJump -> ProxyCommand "ssh -W", serverloop.c direct-tcpip needs AllowTcpForwarding)
and aws-ia/cfn-ps-linux-bastion at commit 213dd9a (EnableTCPForwarding defaults to false).
Run: python3 hop.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, WIDE  # noqa: E402

d = Diagram("Two ways through a jump host",
            "In: you need a shell on a server behind the jump host. Two ways, pick one. "
            "Pass straight through: your laptop runs ssh -J jump target; it opens SSH to the jump host and "
            "asks it to forward bytes to the target's port 22; your own SSH session then runs to the target, "
            "and you sign in there directly. The jump host must allow TCP forwarding, which AWS's reference "
            "template turns off by default. "
            "Log in, then hop: you ssh to the jump host, get a shell there, and run ssh to the target from it. "
            "Commands run on the jump host, so it can log them. Agent forwarding is off by default; with it "
            "on, anyone who can get past file permissions on the jump host can use your keys. "
            "Client config, for both: -J a,b visits the jump hosts in order; settings for the jump hosts go "
            "in ~/.ssh/config, since command-line options apply to the target.")

TOP, GH = 84, 540
d.pill(L, 16, WIDE, 48, "In: you need a shell on a server behind the jump host · pick one way")

for x, title, cards, labels, notes in [
    (L, "Pass straight through",
     [("Your laptop|ssh -J jump target", "coding"),
      ("Jump host|forwards bytes to target:22", "coding"),
      ("Target|you sign in here directly", "data")],
     ["SSH · asks for a tunnel", "your own SSH session"],
     ("The jump host must allow TCP forwarding", "AWS's template turns it off by default")),
    (R, "Log in, then hop",
     [("Your laptop|ssh jump", "coding"),
      ("Jump host|a shell · you run ssh target", "coding"),
      ("Target|signs in from the jump host", "data")],
     ["SSH · a shell", "a second SSH session"],
     ("Commands run here, so the jump host can log them", "Agent forwarding: off by default, risky on")),
]:
    d.group(x, TOP, GW, GH, title)
    for i, (label, kind) in enumerate(cards):
        d.card(x + 30, TOP + 64 + i * 128, label, kind, w=GW - 60)
    for i, lb in enumerate(labels):
        y0 = TOP + 128 + i * 128
        d.arrow(f"M{x + GW / 2} {y0}V{y0 + 62}", label=lb, at=(x + GW / 2, y0 + 38))
    d.notes(x, TOP, GH, *notes)

BT, BH = 644, 240
d.group(L, BT, WIDE, BH, "On your laptop: ~/.ssh/config")
d.card(L + 30, BT + 64, "Many hops|-J a,b visits them in order", "plan", w=531)
d.card(L + 591, BT + 64, "Jump host settings|go in ~/.ssh/config", "plan", w=531)
d.notes(L, BT, BH, "Options on the command line apply to the target, not to the jump hosts", "", w=WIDE)

d.save(Path(__file__).with_name("hop.svg"))
