"""ABAP Development Tools (ADT) architecture, drawn from SAP's own posts by the ADT product owner:
https://community.sap.com/t5/technology-blog-posts-by-sap/behind-the-design-how-we-transformed-the-abap-development-tools/ba-p/14258121
(2025-11-04) and SAP Help "ABAP Development Tools - HTTP Access" (RFC by default, HTTP via the adt ICF
service).  Run: python3 diagram.py

Three layers top to bottom: the IDE UIs, the shared client layer with no UI, the ABAP server."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("ABAP Development Tools architecture",
            "1 The IDEs: Eclipse runs the ADT plug-ins directly; VS Code talks over the Language Server Protocol "
            "to the ADT Language Server, which wraps the same Eclipse plug-ins without their UI. "
            "2 The client layer has no UI: wrappers for the ADT REST APIs and client-side tools such as the "
            "debugger, test runner, ATC and tracing, about 2.9 million lines shared by both IDEs. "
            "3 It talks to the ABAP server over RFC or HTTP. The server offers the ADT REST APIs, one API for "
            "every release from SAP NetWeaver 7.3 EHP1 SP04, and the object types: new ones are server-driven, "
            "shown by one form-based and one source-based renderer.")

# 1 IDEs
d.group(24, 16, 1152, 288, "IDEs: the UI", 1)
d.sub(40, 64, 540, 224, "Eclipse")
d.card(190, 132, "ADT plug-ins|UI part", w=240, h=72, cls="human")
d.note(64, 262, "16 years of features", "start")
d.sub(620, 64, 540, 224, "VS Code, from 2026")
d.card(644, 132, "ADT extension|file-based", w=220, h=72, cls="human")
d.card(916, 132, "ADT Language|Server", "coding", w=220, h=72)
d.arrow("M864 168H912", label="LSP", at=(888, 158))
d.note(644, 262, "Eclipse plug-ins without their UI", "start")

# 2 client layer, shared
d.group(24, 336, 1152, 264, "Client layer: no UI, shared", 2)
for i, t in enumerate(["REST API|wrappers", "Debugger|test runner", "ATC|tracing", "Old releases|kept working"]):
    d.card(48 + i * 282, 396, t, "coding", w=258, h=72)
d.note(600, 522, "2.9 million lines, written once for Eclipse")
d.note(600, 550, "VS Code reuses it through the Language Server")

# arrows into the client layer, drawn after the group so they sit on top
d.arrow("M310 204V332", label="runs", at=(310, 320))
d.arrow("M1026 204V332", label="wraps", at=(1026, 320))

# 3 ABAP server
d.group(24, 632, 1152, 252, "ABAP server", 3)
d.card(48, 692, "ADT REST|APIs", "plan", w=258, h=72)
d.sub(400, 676, 760, 108, "")
d.card(424, 700, "Form-based|object types", "write", w=344, h=64)
d.card(792, 700, "Source-based|object types", "write", w=344, h=64)
d.arrow("M306 728H396")
d.note(600, 820, "one API for every release from 7.3 EHP1 SP04")
d.note(600, 848, "new object types: UI described in ABAP")
d.arrow("M177 468V688", label="RFC or HTTP", at=(177, 622))

d.save(Path(__file__).with_name("diagram.svg"))
