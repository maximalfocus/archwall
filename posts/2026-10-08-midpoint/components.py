"""midPoint's parts: the clients above the Model API, the IDM model, and the subsystems below it.
A map of parts, not steps: clients call the model through the Model API; the model uses provisioning
and the repository; schema, tasks and security are shared services.
The architecture page still lists a generic (multi-database) repository; the code at this commit has only
the native PostgreSQL one (repo/repo-sqale), and docs/repository says generic support was removed in 4.10.
Drawn from Evolveum/midpoint at commit 160887ba (pom.xml modules, gui/, model/, provisioning/, repo/, infra/,
docs/repository, docs/smart-integrations, docs/tasks/task-manager) and Evolveum/docs at 907aa8d
(midpoint/architecture/index.adoc).
Run: python3 components.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, C3, CW3  # noqa: E402

d = Diagram("midPoint's parts",
            "Clients, above the Model API, change most from one deployment to the next: the admin GUI, a web "
            "UI built with Apache Wicket; the REST API, the Model API over the network, in JSON, XML or YAML; "
            "and your own code. They call the IDM model through the Model API. "
            "The IDM model is where every change passes and policies are enforced: mappings, roles and "
            "policy rules; approvals and cases; certification, reports and notifications; and smart "
            "integration, AI suggestions for mappings and correlation from an outside service, which needs "
            "the smartIntegration setting. "
            "The model reads and writes accounts through provisioning and stores objects in the repository. "
            "Provisioning keeps shadows that link users to accounts and talks to apps through ConnId "
            "connectors, or built-in manual and asynchronous ones (the asynchronous connector is experimental); "
            "it stores the shadows in the repository. "
            "The repository is native PostgreSQL, the only database since midPoint 4.10; the audit trail "
            "goes to its own tables or to a log. "
            "Shared services: the schema (Prism, written in XSD), tasks run by the Quartz scheduler, "
            "and security, which checks authorizations.")

# Clients: above the Model API.
d.group(24, 16, 1152, 196, "Clients · above the Model API")
for x, (label, kind) in zip((54, 430, 806), [("Admin GUI|web UI · Apache Wicket", "coding"),
                                             ("REST API|JSON · XML · YAML", "coding"),
                                             ("Your own code|custom services · UIs", "coding")]):
    d.card(x, 70, label, kind, w=340)
d.note(600, 186, "Changes a lot from one deployment to the next")

d.arrow("M600 212V274", label="Model API", at=(600, 250))

# The IDM model.
d.group(24, 276, 1152, 236, "IDM model · every change passes here")
for x, (label, kind) in zip((45, 322, 599, 876), [("Identity logic|mappings · roles · policies", "plan"),
                                                  ("Approvals|cases · work items", "review"),
                                                  ("More modules|certification · reports …", "critic"),
                                                  ("Smart integration|AI hints · needs config", "plan")]):
    d.card(x, 330, label, kind, w=257)
d.note(600, 444, "Changes in config, not in code")

# Below the model.
x1, x2, x3 = C3
d.arrow(f"M{x1 + CW3 / 2} 512V590", label="reads · writes accounts", at=(x1 + CW3 / 2, 552))
d.arrow(f"M{x2 + CW3 / 2} 512V590", label="stores objects", at=(x2 + CW3 / 2, 552))

d.group(x1, 592, CW3, 292, "Provisioning")
d.column(x1, 592, [("Shadows|link users to accounts", "data"),
                   ("Connectors|ConnId · manual · async", "coding")], w=CW3 - 60)
d.notes(x1, 592, 292, "Talks to HR · directories · apps", "Async connector: experimental", w=CW3)

d.group(x2, 592, CW3, 292, "Repository")
d.column(x2, 592, [("Native PostgreSQL|the only database", "write"),
                   ("Audit trail|own tables or a log", "data")], w=CW3 - 60)
d.notes(x2, 592, 292, "Generic databases: gone in 4.10", w=CW3)

d.group(x3, 592, CW3, 292, "Shared services")
d.column(x3, 592, [("Schema|Prism · written in XSD", "data"),
                   ("Tasks|Quartz scheduler", "coding"),
                   ("Security|checks authorizations", "review")], w=CW3 - 60)

d.save(Path(__file__).with_name("components.svg"))
