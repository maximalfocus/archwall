"""What the first ADT for VS Code release covers.  From "ABAP Development Tools for VS Code: Everything You
Need to Know" (Thomas Alexander Ritter, 2025-11-04, read 2026-10-05), sections "Primary focus will be support
for the ABAP Cloud Development Model", "Scope of the First Release", "First Release Targeted at Early
Adopters", "... gradually catch up ... one Client Release at a Time" and "Same Backend Support":
https://community.sap.com/t5/technology-blog-posts-by-sap/abap-development-tools-for-vs-code-everything-you-need-to-know/ba-p/14258129
(linked from "Behind the Design").  Run: python3 release.py

Snake order: 1 the focus, ABAP Cloud (top left) -> 2 the first release, RAP UI services (top right) ->
3 what still needs Eclipse (bottom right) -> 4 how VS Code catches up (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("First VS Code release",
            "1 The focus is the ABAP Cloud development model; the goal is every developer flow in it. Classic "
            "models such as Dynpro and Web Dynpro are not planned. "
            "2 The first release, for early adopters, targets RAP UI services: around 12+ object types, enough "
            "to build one from scratch, with class and interface editors and the basic develop, test and debug "
            "flow. "
            "3 For many other tasks developers still switch to ADT for Eclipse. "
            "4 VS Code catches up one client release at a time: each tool moves to LSP and gets a VS Code UI. "
            "The Eclipse plug-in took 16 years to reach its scope. The plan is to support the same server "
            "releases as Eclipse, down to SAP NetWeaver 7.3 EHP1 SP04.")

L, R, W = 24, 624, 552
T1, H1 = 16, 404
T2, H2 = 452, 432

# 1 focus
d.group(L, T1, W, H1, "Focus: ABAP Cloud", 1)
d.card(L + 30, 80, "ABAP Cloud|every developer flow", "plan", w=492, h=72)
d.card(L + 30, 182, "Dynpro, Web Dynpro|not planned", w=492, h=72)
d.bad(L + 70, 218)
d.note(L + W / 2, 354, "the goal, not the first release")

# 2 first release
d.group(R, T1, W, H1, "First release: RAP UI services", 2)
d.card(R + 30, 80, "Build a RAP UI service|from scratch", "coding", w=492, h=72)
d.card(R + 30, 182, "Around 12+|object types", None, w=236, h=72)
d.card(R + 286, 182, "Develop, test|debug", "coding", w=236, h=72)
d.note(R + W / 2, 354, "class and interface editors included")
d.note(R + W / 2, 382, "for early adopters")

d.arrow(f"M{L + W} 116H{R - 2}", label="starts with", at=(600, 104))

# 3 still Eclipse
d.group(R, T2, W, H2, "Still in Eclipse", 3)
d.card(R + 30, T2 + 130, "Many other tasks|switch to ADT for Eclipse", w=492, h=72, cls="human")

d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="everything else", at=(R + W / 2 + 84, T1 + H1 + 22))

# 4 catch up
d.group(L, T2, W, H2, "Catching up", 4)
d.card(L + 30, T2 + 70, "Each client release|moves more tools to LSP", "coding", w=492, h=72)
d.card(L + 30, T2 + 172, "Plan: same server releases|down to 7.3 EHP1 SP04", "plan", w=492, h=72)
d.note(L + W / 2, T2 + 364, "Eclipse took 16 years")
d.note(L + W / 2, T2 + 392, "to reach today's scope")

d.arrow(f"M{R} {T2 + 166}H{L + W + 2}", label="moves over", at=(600, T2 + 154))

d.save(Path(__file__).with_name("release.svg"))
