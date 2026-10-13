"""pi-durable: Commit before publication. Source: earendil-works/pi at 7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6; packages/durable/docs/spec.md:1922-1935; src/session/session.ts:690-740; src/harness/scheduler.ts:288-310; src/harness/tool.ts:163-185; README.md:697-719. Run: python3 durability.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram

d = Diagram('Commit before publication', 'An external effect is surrounded by durable commits: first record its intent, then call a model or tool outside the Session transaction, then record the outcome and publish committed state. On reopening, surviving running tasks become pending at their stored checkpoint; it dispatches nothing. Resume, a submission or a wait starts the scheduler. An interrupted tool reruns only when its stored and current policies both say replay safe; otherwise it produces an interrupted error. Replay-safe external effects need their own idempotency. A storage failure closes the Harness; reopen consistent committed storage to recover.')
d.pill(24,16,1152,48,"External work sits between durable commits")
for x,n,title,label,kind in [(24,1,"Commit intent","Task checkpoint|what will run","write"),(416,2,"Perform effect","Model or tool|outside the transaction","coding"),(808,3,"Commit outcome","State → storage → UI|publish after success","write")]:
    d.group(x,84,368,280,title,n)
    d.card(x+30,154,label,kind,w=308)
d.arrow("M392 248H414",label="intent stored",at=(404,236))
d.arrow("M784 248H806",label="result",at=(796,236))
d.group(24,410,1152,454,"After a process restart")
d.card(54,492,"Reopen storage|running → pending","plan",w=288)
d.card(430,492,"Resume scheduler|stored task checkpoint","plan",w=320)
d.arrow("M342 524H428",label="recover",at=(386,512))
d.card(54,644,"Tool replay: safe|stored AND current policy","review",w=288)
d.card(430,644,"Rerun tool|make effects idempotent","coding",w=320)
d.arrow("M590 556V596H198V642",label="check policy",at=(394,596))
d.arrow("M342 676H428",label="both safe",at=(386,664))
d.card(806,644,"Otherwise interrupted|return an error result","write",w=320)
d.arrow("M198 708V746H966V710",label="not both safe",at=(788,746))
d.notes(24,410,454,"Storage failure closes the Harness; reopen to recover.","Replay safety is a tool contract, not a guarantee against duplicate external effects.",w=1152)

d.save(Path(__file__).with_name("durability.svg"))
