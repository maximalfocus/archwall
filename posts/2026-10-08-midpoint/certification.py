"""midPoint access certification: define a campaign, review a stage, close the stage, carry out the decisions.
Snake order: 1 define (top left) -> 2 review a stage (top right) -> 3 close the stage (bottom right, back to 2 for the
next stage) -> 4 carry it out (bottom left).
Drawn from Evolveum/midpoint at commit 160887ba (docs/certification/index.adoc, ad-hoc-certification.adoc,
automated-campaign-scheduling.adoc, reports/index.adoc; infra/schema/.../common-certification-3.xsd;
model/certification-impl AccCertResponseComputationHelper.java and outcomeStrategies/*;
infra/schema/.../CertCampaignTypeUtil.java isRemediationAutomatic).
Where the XSD says the campaign-level default is oneDenyDenies, the code uses allMustAccept; the code wins.
Run: python3 certification.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Access certification in midPoint",
            "In: a campaign template, started by hand, by a scheduled task, or by a policy rule for an ad-hoc "
            "campaign. "
            "1 Define: the scope picks the objects and what to certify on them, such as users and their roles, "
            "with a filter; each pair is one case. Reviewers are the object's manager, the target's owner and "
            "the like, with a default reviewer as fallback. Each stage has a duration and an outcome rule. "
            "2 Review a stage: reviewers decide each case: accept, revoke or reduce, or not decided or "
            "delegate; a case with no decision is no response. Before the deadline midPoint can notify and "
            "escalate. "
            "3 Close the stage: the stage outcome by default is one accept accepts. Revoke and reduce stop the "
            "review; accepted and undecided cases go on to the next stage. Across stages the default is all "
            "must accept. "
            "4 Carry it out: with automated remediation midPoint removes revoked access; otherwise it is "
            "report only and an admin acts. Unresolved cases can be reiterated, run again by hand unless a delay is set. "
            "Reports cover definitions, campaigns, cases and work items.")

d.pill(L, 16, GW, 48, "In: a template · by hand · a schedule · a policy rule")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Define", 1)
d.column(L, T1, [("Scope|e.g. users × their roles", "plan"),
                 ("Reviewers|manager · owner · default", "plan"),
                 ("Stages|duration · outcome rule", "plan")])
d.notes(L, T1, H1, "Each user × role pair is one case", "")

d.group(R, T1, GW, H1, "Review a stage", 2)
d.column(R, T1, [("Keep or not|accept · revoke · reduce", "review"),
                 ("Can't say|not decided · delegate", "review"),
                 ("No answer|no response", "data")])
d.notes(R, T1, H1, "Before the deadline: notify · escalate", "")

d.group(R, T2, GW, H2, "Close the stage", 3)
d.column(R, T2, [("Stage outcome|default: one accept accepts", "critic"),
                 ("Stop here|revoke · reduce", "critic"),
                 ("Go on|accepted · undecided", "plan")])
d.notes(R, T2, H2, "Across stages, default: all must accept", "")

d.group(L, T2, GW, H2, "Carry it out", 4)
d.column(L, T2, [("Automated remediation|removes revoked access", "coding"),
                 ("Report only|otherwise · an admin acts", "write"),
                 ("Reiterate|unresolved cases · run again", "plan"),
                 ("Reports|campaigns · cases · work items", "data")], h=60, gap=14, first=60)

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="cases", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="decisions", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R + 120} {T2}V{T1 + H1 + 2}", back=True, label="next stage", at=(R + 120, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="outcomes", at=(600, T2 + 164))

d.save(Path(__file__).with_name("certification.svg"))
