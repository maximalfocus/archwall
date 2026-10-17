"""AWS's reference Linux bastion: who comes in, where the bastions sit, what they reach, where logs go.
A map of parts, not steps: unnumbered groups joined by arrows that name what flows.
Drawn from aws-ia/cfn-ps-linux-bastion at commit 213dd9a (templates/linux-bastion-entrypoint-*-vpc.template.yaml:
RemoteAccessCIDR default disabled-onlyssmaccess, NumBastionHosts 1-4 default 1, EnableTCPForwarding and
EnableX11Forwarding default false, NumberOfAZs 2, security group ingress; scripts/bastion_bootstrap.sh:
audit.log to CloudWatch, stream {instance_id}; docs/deployment_guide/partner_editable/architecture.adoc).
Run: python3 aws.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2, WIDE  # noqa: E402

d = Diagram("AWS's reference Linux bastion",
            "In: AWS's CloudFormation templates for Linux bastion hosts; a map of parts, not steps. "
            "Outside: by default no port is open and admins come in through AWS Session Manager; if you "
            "set an allowed address range, admins from it may use SSH on port 22, and ping. "
            "Public subnets in two availability zones: an Auto Scaling group runs 1 to 4 bastions, 1 by "
            "default; each gets an Elastic IP only when an address range is set; TCP and X11 forwarding are "
            "off by default. The new-VPC template also adds NAT gateways. "
            "Private subnets: your servers, which reach the internet through the NAT gateways; the bastions "
            "reach them by SSH. "
            "Logs: auditd writes the audit log on each bastion, and the CloudWatch agent copies it to a "
            "CloudWatch log group, one stream per instance ID.")

d.pill(L, 16, WIDE, 48, "In: AWS's CloudFormation templates for Linux bastion hosts · a map, not steps")

d.group(L, T1, GW, H1, "Outside")
d.column(L, T1, [("Session Manager|the default · no open port", "plan"),
                 ("SSH on port 22|only from the CIDR you set", "coding")])
d.notes(L, T1, H1, "No CIDR set: no inbound rule at all", "")

d.group(R, T1, GW, H1, "Public subnets · 2 AZs")
d.stack(R + 30, T1 + 64, "Bastions|Auto Scaling · 1 to 4, default 1", "coding", w=GW - 84, step=8)
d.card(R + 30, T1 + 156, "Elastic IP|only when a CIDR is set", "data", w=GW - 60)
d.card(R + 30, T1 + 232, "NAT gateways|new-VPC template only", "data", w=GW - 60)
d.notes(R, T1, H1, "TCP and X11 forwarding: off by default", "")

d.group(L, T2, GW, H2, "Logs")
d.column(L, T2, [("auditd|audit.log on each bastion", "data"),
                 ("CloudWatch log group|one stream per instance ID", "write")])

d.group(R, T2, GW, H2, "Private subnets")
d.column(R, T2, [("Your servers|EC2 and other resources", "data")])
d.notes(R, T2, H2, "Out to the internet through the NAT gateways", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="sign in", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="SSH", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R + 90} {T1 + H1}V{T1 + H1 + 18}H{L + 300}V{T2 - 2}", label="audit log", at=(450, T1 + H1 + 24))

d.save(Path(__file__).with_name("aws.svg"))
