"""ABAP Development Tools (ADT) architecture, drawn from SAP's own posts by the ADT product owner:
https://community.sap.com/t5/technology-blog-posts-by-sap/behind-the-design-how-we-transformed-the-abap-development-tools/ba-p/14258121
(2025-11-04) and SAP Help "ABAP Development Tools - HTTP Access" (RFC by default, HTTP via the adt ICF
service).  Scripts that call the REST APIs directly: jfilak/sapcli (326475f9, "ADT operates over HTTP")
and marcellourbani/abap-adt-api (b73a0a1e, "access to the ADT REST interface").  Run: python3 diagram.py

Three layers top to bottom: the IDE UIs, the shared client layer with no UI, the ABAP server.
On the right, scripts skip both client layers and call the server's REST APIs over HTTP."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("ABAP Development Tools architecture",
            "1 The IDEs: Eclipse runs the ADT plug-ins; VS Code talks over the Language Server Protocol "
            "to the ADT Language Server, which wraps the same Eclipse plug-ins without their UI. "
            "2 The client layer has no UI: wrappers for the ADT REST APIs and client-side tools such as the "
            "debugger, test runner, ATC and tracing, about 2.9 million lines shared by both IDEs. "
            "3 It talks to the ABAP server over RFC or HTTP. The server offers the ADT REST APIs, one API for "
            "every release from SAP NetWeaver 7.3 EHP1 SP04, and the object types: form-based and source-based. "
            "4 Scripts such as sapcli or abap-adt-api skip the client layer and call the REST APIs over HTTP "
            "themselves, so whatever the client layer would do, they write themselves.")

LW = 880  # width of the IDE and client-layer groups; scripts take the column on the right

# 1 IDEs
d.group(24, 16, LW, 288, "IDEs: the UI", 1)
d.sub(40, 64, 300, 224, "Eclipse")
d.card(70, 132, "ADT plug-ins|UI part", w=240, h=72, cls="human")
d.note(56, 262, "16 years of features", "start")
d.sub(356, 64, 532, 224, "VS Code, from 2026")
d.card(372, 132, "ADT extension|file-based", w=200, h=72, cls="human")
d.card(660, 132, "ADT Language|Server", "coding", w=212, h=72)
d.arrow("M572 168H656", label="LSP", at=(614, 158))
d.note(372, 262, "Eclipse plug-ins without their UI", "start")

# 2 client layer, shared
d.group(24, 336, LW, 264, "Client layer: no UI, shared", 2)
for i, t in enumerate(["REST API|wrappers", "Debugger|test runner", "ATC|tracing", "Old releases|kept working"]):
    d.card(48 + i * 212, 396, t, "coding", w=200, h=72)
d.note(464, 522, "2.9 million lines, written once for Eclipse")
d.note(464, 550, "VS Code reuses it through the Language Server")

# arrows into the client layer, drawn after the group so they sit on top
d.arrow("M190 204V332", label="runs", at=(190, 320))
d.arrow("M766 204V332", label="wraps", at=(766, 320))

# 4 scripts: no IDE, no client layer
SX, SW = 928, 248
d.group(SX, 16, SW, 584, "Scripts", 4)
d.card(SX + 20, 132, "Your own|scripts", "coding", w=SW - 40, h=72)
d.note(SX + 104, 300, "sapcli, abap-adt-api")
d.note(SX + 104, 328, "no client layer")

# 3 ABAP server
d.group(24, 632, 1152, 252, "ABAP server", 3)
d.card(340, 688, "ADT REST APIs|one API for 7.3 EHP1 SP04 on", "plan", w=520, h=72)
d.card(272, 796, "Form-based object types", "write", w=300, h=56)
d.card(628, 796, "Source-based object types", "write", w=300, h=56)
d.arrow("M422 760V792")
d.arrow("M778 760V792")
d.arrow("M148 468V724H336", label="RFC or HTTP", at=(148, 618))
d.arrow("M1140 204V724H864", label="HTTP", at=(1140, 618))

d.save(Path(__file__).with_name("diagram.svg"))
