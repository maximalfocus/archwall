"""pi-durable: pi-durable: the parts. Source: earendil-works/pi at 7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6; packages/durable/README.md:1-97,103-134,364-409,647-685; src/session/session.ts:690-740. Run: python3 diagram.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram

d = Diagram('pi-durable: the parts', 'The host supplies an application UI, models, extensions and settings. Harness admits input and schedules generation, tool and compaction tasks. Session atomically commits transcripts, task checkpoints, submissions and Chord documents to a selected storage backend. Committed changes feed conversation views and agent events back to the host. Storage choices are memory, Node SQLite, JSONL and Cloudflare Durable Object SQLite. This package is experimental.')
d.pill(24,16,1152,48,"pi-durable · experimental agent runtime")
d.group(24,84,552,380,"Host application")
d.column(24,84,[("UI · API|submit and observe", "coding"),("pi-ai models|provider access", "coding"),("Registry · settings|extensions and run policy", "plan")])
d.group(624,84,552,380,"Harness")
d.column(624,84,[("Submissions · inbox|admit and queue requests", "plan"),("Scheduler|run task phases", "plan"),("Built-in tasks|generation · tools · compaction", "coding")])
d.group(624,500,552,364,"Session")
d.column(624,500,[("Transcripts|conversations and entries", "data"),("Tasks · submissions|checkpoints and outcomes", "data"),("Chord documents|agent · live · app state", "write")])
d.group(24,500,552,364,"Storage · choose a backend")
d.column(24,500,[("Memory|temporary state", "data"),("Node SQLite · JSONL|local persistence", "write"),("Durable Object SQLite|Cloudflare persistence", "write")])
d.arrow("M576 284H622",label="requests",at=(600,272))
d.arrow("M900 464V498",label="commits",at=(900,488))
d.arrow("M624 680H578",label="writes",at=(600,668))
d.arrow("M660 500V482H540V466",label="views · events",at=(600,482))

d.save(Path(__file__).with_name("diagram.svg"))
