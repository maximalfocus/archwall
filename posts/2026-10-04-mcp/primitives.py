"""What MCP servers offer: tools, resources, prompts, and who decides when each is used.  Drawn from
https://modelcontextprotocol.io/docs/learn/architecture (Primitives, the database example) and
https://modelcontextprotocol.io/specification/2026-07-28/server (control hierarchy), .../server/tools
(human in the loop), .../server/resources (URI), .../server/prompts (slash commands), the spec index
(Security: consent before invoking a tool; Extensions are opt-in on both sides).
Protocol version 2026-07-28, read 2026-10-05.  Run: python3 primitives.py

Snake order: 1 tools (top left) -> 2 resources (top right) -> 3 prompts (bottom right) ->
4 one database server offering all three (bottom left)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

L, R, W = 24, 624, 552
T1, H1 = 16, 412
T2, H2 = 460, 400


def col(x, top, cards, h=64, gap=22, y0=64):
    """One column of wide cards, top to bottom."""
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + y0 + i * (h + gap), lbl, kind, w=492, h=h)


def kind_card(x, top, what, methods, kind):
    """The primitive card, then the two methods the client uses for it."""
    d.card(x + 30, top + 72, what, kind, w=492, h=80)
    d.card(x + 30, top + 176, methods, "data", w=492, h=64)


d = Diagram("What MCP servers offer",
            "1 Tools: the model decides. Functions that act, such as file operations, API calls or database "
            "queries. The client finds them with tools/list and runs one with tools/call. The host asks the user "
            "before a tool runs, and a person should be able to say no. "
            "2 Resources: the app decides. Data for context, such as file contents, database records or API "
            "replies, each with a URI. Found with resources/list, read with resources/read. "
            "3 Prompts: the user decides. Reusable templates such as few-shot examples, often shown as slash "
            "commands or menus. Found with prompts/list, fetched with prompts/get. "
            "4 Example from the docs: one database server offers a tool to run a query, a resource with the "
            "schema, and a prompt with few-shot examples. Optional extensions such as Tasks add more; both "
            "sides must opt in.")

d.group(L, T1, W, H1, "Tools: the model decides", 1)
kind_card(L, T1, "Functions that act|files, APIs, database queries", "tools/list → tools/call", "coding")
d.note(L + W / 2, T1 + 334, "the host asks the user before a tool runs;")
d.note(L + W / 2, T1 + 362, "a person should be able to say no")

d.group(R, T1, W, H1, "Resources: the app decides", 2)
kind_card(R, T1, "Data for context|file contents, records, API replies", "resources/list → resources/read", "data")
d.note(R + W / 2, T1 + 334, "each one has a URI;")
d.note(R + W / 2, T1 + 362, "the app chooses what to attach")

d.group(R, T2, W, H2, "Prompts: the user decides", 3)
kind_card(R, T2, "Reusable templates|e.g. few-shot examples", "prompts/list → prompts/get", "write")
d.note(R + W / 2, T2 + 334, "often shown as slash commands")
d.note(R + W / 2, T2 + 362, "or menu items")

d.group(L, T2, W, H2, "One database server, all three", 4)
col(L, T2, [("Tool|run a query", "coding"), ("Resource|the database schema", "data"),
            ("Prompt|few-shot examples", "write")])

d.note(600, 888, "Optional extensions, such as Tasks for long jobs, add more; both sides must opt in")

d.save(Path(__file__).with_name("primitives.svg"))
