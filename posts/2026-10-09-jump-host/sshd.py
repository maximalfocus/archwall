"""Settings on the jump host's sshd, grouped by job; a catalogue, not steps.
Defaults are the ones sshd_config.5 states.
Drawn from openssh/openssh-portable at commit 6a46ea6 (sshd_config.5: AllowUsers, PasswordAuthentication,
AuthenticationMethods, AllowTcpForwarding, PermitOpen, Match, ClientAliveInterval, ChannelTimeout,
PerSourcePenalties, LogLevel, Banner; auth.c auth_log).
Run: python3 sshd.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2, WIDE  # noqa: E402

d = Diagram("Settings on the jump host's sshd",
            "In: the sshd_config file on the jump host. Its settings grouped by job, not in any order. "
            "Who gets in: AllowUsers lets in only the listed users, optionally from listed hosts; "
            "PasswordAuthentication no turns passwords off, the default is yes; AuthenticationMethods can "
            "ask for a key plus a second method. "
            "What they may do: AllowTcpForwarding local allows the forwarding that ssh -J uses; PermitOpen "
            "limits forwarding to listed host and port pairs; Match blocks set other rules for some users or "
            "groups. "
            "Close what's idle: ClientAliveInterval checks on quiet clients, 0 by default, which means off; "
            "ChannelTimeout closes idle channels; "
            "PerSourcePenalties, on by default, refuses an address that looks like an attack for a while. "
            "Logs and notice: LogLevel is INFO by default, and each accepted login is logged with its key "
            "fingerprint and source address; Banner shows text before login, none by default.")

d.pill(L, 16, WIDE, 48, "In: sshd_config on the jump host · grouped by job · defaults as sshd_config(5) gives them")

d.group(L, T1, GW, H1, "Who gets in")
d.column(L, T1, [("AllowUsers|only the listed users", "review"),
                 ("PasswordAuthentication no|default: yes", "review"),
                 ("AuthenticationMethods|key plus a second factor", "review")])

d.group(R, T1, GW, H1, "What they may do")
d.column(R, T1, [("AllowTcpForwarding local|what ssh -J needs", "plan"),
                 ("PermitOpen|only listed host:port", "plan"),
                 ("Match|other rules per user or group", "plan")])

d.group(L, T2, GW, H2, "Close what's idle")
d.column(L, T2, [("ClientAliveInterval|default 0: off", "critic"),
                 ("ChannelTimeout|close idle channels", "critic"),
                 ("PerSourcePenalties|on: refuse attackers a while", "critic")], h=60, gap=14, first=60)

d.group(R, T2, GW, H2, "Logs and notice")
d.column(R, T2, [("LogLevel|default INFO", "data"),
                 ("Accepted … from …|names the key and the address", "data"),
                 ("Banner|text before login · default none", "review")], h=60, gap=14, first=60)

d.save(Path(__file__).with_name("sshd.svg"))
