"""/idd-issue: file exactly one implementation-ready issue, and only when asked to.
Drawn from maximalfocus/idd-skills at commit f905928 (skills/idd-issue/SKILL.md,
skills/idd-plan/references/conventions.md N-1, CONSTITUTION.md Article 5).
Run: python3 issue.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram  # noqa: E402

d = Diagram("idd-issue",
            "You ask to file, create or open one issue. "
            "1 Pin it down: which repository, from --repo, a URL or this checkout; search open and closed issues "
            "and stop with the existing one if it is a likely duplicate; gather only the evidence needed and "
            "invent no paths or labels. Ask one question only if scope or behaviour is really unclear. "
            "2 Draft it small: a title that states the outcome, with no type prefix, number or IDs; the problem "
            "and its evidence; testable acceptance criteria; and non-goals only if they prevent confusion. "
            "3 Gate before creating: one coherent issue, small enough for one run; claims backed by evidence, "
            "with criteria enough to judge when it is done; and it fits the product model, or names a new concept "
            "or special case as a design decision. Nothing private goes in: no credentials, account names or "
            "home paths. "
            "4 Create once and read back: gh issue create with the body from a file; if the result is unclear, "
            "search before any retry; then read the issue back and check its repository, title, body and OPEN "
            "state. A request to draft or suggest creates nothing; /idd-auto may file its one next issue.")

L, R, W = 24, 624, 552
T1, H1 = 84, 380
T2, H2 = 500, 364
CW, CH, GAP = 492, 64, 16


def column(x, top, cards, gap=GAP):
    for i, (lbl, kind) in enumerate(cards):
        d.card(x + 30, top + 64 + i * (CH + gap), lbl, kind, w=CW, h=CH)


def notes(x, top, h, a, b):
    d.note(x + W / 2, top + h - 52, a)
    d.note(x + W / 2, top + h - 26, b)


d.pill(L, 16, W, 48, "You ask to file, create or open one issue")
d.arrow(f"M{L + W / 2} 64V{T1 - 2}")

d.group(L, T1, W, H1, "Pin it down", 1)
column(L, T1, [("Which repo?|--repo, a URL, or this checkout", "plan"),
               ("Search open and closed issues|duplicate? stop, return it", "review"),
               ("Only the evidence needed|no made-up paths or labels", "review")])
notes(L, T1, H1, "One question, only if scope", "or behaviour is really unclear")

d.group(R, T1, W, H1, "Draft it small", 2)
column(R, T1, [("Title: the outcome|no type prefix, number or IDs", "write"),
               ("Problem and evidence", "write"),
               ("Acceptance criteria|each one testable", "write"),
               ("Non-goals|only if they prevent confusion", "write")])

d.group(R, T2, W, H2, "Gate before creating", 3)
column(R, T2, [("One coherent issue|small enough for one run", "review"),
               ("Claims backed by evidence|criteria enough to judge done", "review"),
               ("Fits the product model|or names a design decision", "critic")])
notes(R, T2, H2, "Nothing private: no credentials,", "account names or home paths")

d.group(L, T2, W, H2, "Create once, read back", 4)
column(L, T2, [("gh issue create|body from a file", "write"),
               ("Unclear result?|search before any retry", "review"),
               ("Read it back|repo, title, body, OPEN", "review")])

d.arrow(f"M{L + W} {T1 + 200}H{R - 2}", label="unique", at=(600, T1 + 188))
d.arrow(f"M{R + W / 2} {T1 + H1}V{T2 - 2}", label="draft", at=(R + W / 2 + 36, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + W + 2}", label="passes", at=(600, T2 + 164))

d.note(600, 888, "Draft or suggest creates nothing; /idd-auto may file its one next issue")

d.save(Path(__file__).with_name("issue.svg"))
