"""ABAP Development Tools (ADT) overview, drawn from SAP's posts by Thomas Alexander Ritter
(2025-11-04, read 2026-10-05):
"Behind the Design" https://community.sap.com/t5/technology-blog-posts-by-sap/behind-the-design-how-we-transformed-the-abap-development-tools/ba-p/14258121
and the post it links, "ABAP Development Tools for VS Code: Everything You Need to Know"
https://community.sap.com/t5/technology-blog-posts-by-sap/abap-development-tools-for-vs-code-everything-you-need-to-know/ba-p/14258129
Run: python3 diagram.py

Snake order: 1 the IDEs (top left) -> 2 the shared client layer with no UI (top right) ->
3 the ABAP server (bottom right) -> 4 the two editor renderers (bottom left), back up to the IDEs."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("ABAP Development Tools overview",
            "1 The IDEs: Eclipse runs the ADT plug-ins with their UI; VS Code, from 2026, runs an ADT extension "
            "where objects are edited as files. "
            "2 The shared client layer has no UI: wrappers for the ADT REST APIs, debugger, test runner, ATC, "
            "tracing and support for old releases, 2.9 million lines. Eclipse runs it directly; VS Code reaches it "
            "over LSP through the ADT Language Server. "
            "3 It talks to the ABAP server over RFC or HTTP: one API for every release from SAP NetWeaver "
            "7.3 EHP1 SP04. Objects are stored on the server, which also describes each new editor's UI in ABAP. "
            "4 The client draws those UIs with two renderers, form-based and source-based.")

L, R, W = 24, 624, 552
T1, H1 = 16, 404
T2, H2 = 452, 432

# 1 IDEs
d.group(L, T1, W, H1, "The IDEs", 1)
d.sub(L + 16, 64, 252, 184, "Eclipse")
d.card(L + 32, 120, "ADT plug-ins|with their UI", w=220, h=72, cls="human")
d.sub(L + 284, 64, 252, 184, "VS Code, from 2026")
d.card(L + 300, 120, "ADT extension|edits files", w=220, h=72, cls="human")
d.note(L + W / 2, 354, "Before: SAP GUI and Eclipse only")
d.note(L + W / 2, 382, "VS Code is the first new one")

# 2 shared client layer
d.group(R, T1, W, H1, "Client layer: no UI, shared", 2)
d.card(R + 30, 76, "ADT Language Server|wraps it for VS Code", "coding", w=492, h=64)
for i, t in enumerate(["REST API|wrappers", "Debugger|test runner", "ATC|tracing", "Old releases|still work"]):
    d.card(R + 30 + (i % 2) * 256, 170 + (i // 2) * 88, t, "coding", w=236, h=64)
d.note(R + W / 2, 382, "2.9 million lines, one codebase")

# 1 -> 2
d.arrow("M520 156H650", label="LSP", at=(586, 146))
d.arrow("M142 192V290H622", label="runs", at=(590, 280))

# 3 ABAP server
d.group(R, T2, W, H2, "ABAP server", 3)
d.card(R + 30, T2 + 70, "ADT REST APIs|one API since 7.3 EHP1 SP04", "plan", w=492, h=72)
d.card(R + 30, T2 + 172, "ABAP objects|stored here", "data", w=492, h=64)
d.card(R + 30, T2 + 266, "Editor UI models|written in ABAP", "write", w=492, h=64)
d.note(R + W / 2, T2 + 392, "VS Code reaches the releases Eclipse does")

d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="RFC or HTTP", at=(R + W / 2 + 70, T1 + H1 + 22))

# 4 renderers
d.group(L, T2, W, H2, "Editors: two renderers", 4)
d.card(L + 30, T2 + 96, "Form-based|renderer", "coding", w=230, h=72)
d.card(L + 292, T2 + 96, "Source-based|renderer", "coding", w=230, h=72)
d.card(L + 30, T2 + 236, "Every new object type|drawn by one of the two", w=492, h=64, cls="human")
d.arrow(f"M{L + 145} {T2 + 168}V{T2 + 232}")
d.arrow(f"M{L + 407} {T2 + 168}V{T2 + 232}")
d.note(L + W / 2, T2 + 392, "A new IDE needs 2 editors, not 88")

d.arrow(f"M{R} {T2 + 290}H{L + W + 2}", label="UI model", at=(600, T2 + 278))
d.arrow(f"M{L + W / 2} {T2}V{T1 + H1 + 2}", label="shown in the IDE", at=(L + W / 2 + 90, T1 + H1 + 22))

d.save(Path(__file__).with_name("diagram.svg"))
