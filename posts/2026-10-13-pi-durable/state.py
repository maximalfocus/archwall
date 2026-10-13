"""pi-durable: State and owned work. Source: earendil-works/pi at 7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6; packages/durable/README.md:449-509,553-656; src/session/forks.ts; src/harness/task-graph.ts; src/harness/scheduler.ts. Run: python3 state.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram

d = Diagram('State and owned work', 'Immutable entries form a conversation transcript. Forks inherit parent entries through a selected entry and continue independently. Reset changes the model context while retaining older stored entries. Compaction replaces older context with a summary. Typed JSON documents track live progress, inbox, agent configuration, provider identity, usage and application state. Chord delivers committed views and document changes; agent events and the task graph are derived views. Tasks may own child tasks or conversations; waiting and completing states keep ownership structured. Abort proceeds from owned children to parents. Background tasks form a boundary for parent abort and idle waits.')
d.pill(24,16,1152,48,"Stored records describe both the conversation and its work")
d.group(24,84,552,380,"Transcript and context")
d.column(24,84,[("Immutable entries|user · system · assistant · result","data"),("Fork at an entry|child continues independently","write"),("Reset · compaction|new context or older summary","plan")])
d.group(624,84,552,380,"Typed JSON documents")
d.column(624,84,[("Agent · provider|choices and session identity","data"),("Live · inbox · usage|progress · queue · cost","data"),("App documents|change alongside entries","write")])
d.group(24,500,552,364,"Committed observation")
d.column(24,500,[("Chord views · watches|snapshot and changes","data"),("Agent events|messages and tool updates","data"),("Task graph · inspect|owned work and blocked tasks","data")])
d.group(624,500,552,364,"Owned tasks and conversations")
d.column(624,500,[("Child work|tasks or subagent conversations","coding"),("Wait · complete · abort|children settle with their owner","plan"),("background: true|survives parent abort","plan")])
d.arrow("M300 464V498",label="committed entries",at=(300,488))
d.arrow("M660 464V480H540V498",label="document changes",at=(600,480))
d.arrow("M624 740H578",label="task state",at=(600,728))

d.save(Path(__file__).with_name("state.svg"))
