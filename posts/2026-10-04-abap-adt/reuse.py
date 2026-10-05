"""Fix 1: reuse the ADT client layer as a language server.  From "Behind the Design", section
"Solution 1: Reusing Our Client Codebase as a Language Server" and its "potential_reuse" figure
(Thomas Alexander Ritter, 2025-11-04, read 2026-10-05):
https://community.sap.com/t5/technology-blog-posts-by-sap/behind-the-design-how-we-transformed-the-abap-development-tools/ba-p/14258121
The "still to do" note is from the linked post "ABAP Development Tools for VS Code: Everything You Need
to Know": https://community.sap.com/t5/technology-blog-posts-by-sap/abap-development-tools-for-vs-code-everything-you-need-to-know/ba-p/14258129
Run: python3 reuse.py

Snake order: 1 option tried in 2018, a TypeScript rewrite (top left) -> 2 the idea from the VS Code Java
extension (top right) -> 3 what SAP built (bottom right) -> 4 what it buys (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("Reusing the client as a language server",
            "1 In 2018 SAP explored a language server in TypeScript, like the community ABAP extensions for "
            "VS Code. It worked, but meant rebuilding the whole client layer and keeping two implementations, so "
            "SAP dropped it. "
            "2 The VS Code Java extension showed another way: it wraps the Eclipse Java tools (JDT) in a language "
            "server, so it is Eclipse running inside VS Code. "
            "3 SAP did the same: VS Code talks LSP to the ADT Language Server, which reuses the Eclipse plug-ins "
            "without their UI and talks RFC or HTTP to the ABAP server, release 7.3 EHP1 SP04 or later. "
            "4 One codebase for Eclipse and VS Code, the same server releases, and 60% of the 2.9 million "
            "lines potentially reused. Still to do: move each tool to LSP and build its UI in VS Code.")

L, R, W = 24, 624, 552
T1, H1 = 16, 404
T2, H2 = 452, 432

# 1 rewrite, rejected
d.group(L, T1, W, H1, "2018: rewrite in TypeScript?", 1)
d.card(L + 30, 80, "TypeScript|language server", "coding", w=492, h=72)
d.card(L + 30, 182, "Rebuild the client|from scratch", w=236, h=72)
d.card(L + 286, 182, "Two codebases|to maintain", w=236, h=72)
d.bad(L + 52, 218)
d.bad(L + 308, 218)
d.note(L + W / 2, 354, "It worked, but not for the long run")
d.note(L + W / 2, 382, "Dropped")

# 2 vscode-java idea
d.group(R, T1, W, H1, "The idea: VS Code Java", 2)
d.card(R + 30, 80, "VS Code Java|extension", "coding", w=492, h=72)
d.card(R + 30, 216, "Eclipse JDT|the Java tools", "coding", w=492, h=72)
d.arrow(f"M{R + W / 2} 152V212", label="wraps", at=(R + W / 2 + 40, 186))
d.note(R + W / 2, 354, "Eclipse running inside VS Code")

d.arrow(f"M{L + W} 116H{R - 2}", label="instead", at=(600, 104))

# 3 what SAP built
d.group(R, T2, W, H2, "What SAP built", 3)
d.card(R + 30, T2 + 60, "VS Code|ADT extension", w=492, h=64, cls="human")
d.card(R + 30, T2 + 166, "ADT Language Server|Eclipse plug-ins, no UI", "coding", w=492, h=72)
d.card(R + 30, T2 + 286, "ABAP server|release 7.3 EHP1 SP04 on", "plan", w=492, h=72)
d.arrow(f"M{R + W / 2} {T2 + 124}V{T2 + 162}", label="LSP", at=(R + W / 2 + 34, T2 + 148))
d.arrow(f"M{R + W / 2} {T2 + 238}V{T2 + 282}", label="RFC or HTTP", at=(R + W / 2 + 70, T2 + 266))

d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="same trick", at=(R + W / 2 + 64, T1 + H1 + 22))

# 4 what it buys
d.group(L, T2, W, H2, "What it buys", 4)
d.card(L + 30, T2 + 60, "One codebase|for Eclipse and VS Code", None, w=492, h=64)
d.card(L + 30, T2 + 146, "Same server releases|as Eclipse", None, w=492, h=64)
d.card(L + 30, T2 + 232, "60% potential reuse|of 2.9 million lines", None, w=492, h=64)
d.note(L + W / 2, T2 + 364, "Still to do: move each tool to LSP")
d.note(L + W / 2, T2 + 392, "and build its UI in VS Code")

d.arrow(f"M{R} {T2 + 202}H{L + W + 2}", label="gives", at=(600, T2 + 190))

d.save(Path(__file__).with_name("reuse.svg"))
