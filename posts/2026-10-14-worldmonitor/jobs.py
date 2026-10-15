"""Queued scenario jobs at worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
Sources: server/worldmonitor/scenario/v1/run-scenario.ts:69-105 (premium request; owner key and queue RPUSH in one
transaction; 202 with jobId and statusUrl after enqueue; a failed transaction returns 502 without a job id);
server/worldmonitor/scenario/v1/scenario-job.ts:22-27 (owner key scenario-owner:<jobId>; owner-scoped result key);
scripts/scenario-worker.mjs:375-383 (startup moves claimed jobs in the processing list back to the pending queue);
scripts/scenario-worker.mjs:415-418 (claims a pending job into processing); scripts/scenario-worker.mjs:465-487
(writes processing, then done or failed result under the owner-scoped key);
server/worldmonitor/scenario/v1/get-scenario-status.ts:138-140 (no owner token: 403); :148 (reads owner key);
:152-154 (missing binding: pending); :155-157 (binding of another owner: 404); :162 (reads result key);
:167-169 (missing result: pending); :171-183 (returns stored status, including processing).
Simulation and deep-forecast use Redis sorted-set queues, not this list; named in a note only
(server/_shared/simulation-queue.ts:122; scripts/seed-forecasts.mjs:13735, 19538).
Company monitoring is an always-on worker outside this picture (scripts/company-monitoring-worker.mjs:4-14).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram, GW

d = Diagram('Queued scenario jobs',
    'A scenario request passes its checks, then the owner key and a pending queue entry are written in one transaction, and the caller gets a job id and status address. '
    'A background worker claims a pending job, records it as processing, and writes done or failed under the owner-scoped result key. '
    'The status route checks premium access and the owner key, then reads the result key. A missing owner key or result reads as pending, so polling can start at once. '
    'Simulation and deep-forecast use sorted-set queues instead.')
d.group(24, 24, GW, 440, 'Request', n=1)
d.column(24, 24, [('Scenario request|POST run-scenario', 'coding'), ('Premium and queue checks|before any write', 'review')], first=64, h=64, gap=18)
d.notes(24, 24, 440, 'Caller gets a job id and status URL.', 'Refused requests write nothing.')
d.group(624, 24, GW, 440, 'Redis records', n=2)
d.column(624, 24, [('Owner key|bound to the caller', 'data'), ('Pending queue|job entry for the worker', 'write')], first=64, h=64, gap=18)
d.notes(624, 24, 440, 'Owner key and queue entry: one transaction.', 'Failed transaction: 502, no job id.')
d.arrow('M576 260H624', label='job stored', at=(600, 250))
d.group(624, 500, GW, 364, 'Worker', n=3)
d.column(624, 500, [('Claim job|pending to processing', 'coding'), ('Write result key|processing, then done or failed', 'coding')], first=64, h=64, gap=18)
d.notes(624, 500, 364, 'Restart moves claimed jobs to pending.', 'Result key is owner-scoped.')
d.arrow('M900 464V500', label='claimed job', at=(900, 482))
d.arrow('M1040 500V464', label='result write', at=(1095, 482))
d.group(24, 500, GW, 364, 'Status', n=4)
d.column(24, 500, [('Client polls|any time after the 202', 'data'), ('Status route|premium, then owner key match', 'review'), ('Reply|pending · processing · done · failed', 'plan')], first=64, h=64, gap=18)
d.notes(24, 500, 364, 'Missing owner key or result: pending.', 'Another job owner gets not found.')
d.arrow('M760 464V482H300V500', label='owner and result read', at=(530, 477))
d.save(Path(__file__).with_suffix('.svg'))
