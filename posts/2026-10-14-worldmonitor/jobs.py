"""Queued scenario jobs at worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
Sources: server/worldmonitor/scenario/v1/run-scenario.ts:69-105 (premium request; owner record and queue RPUSH in one
transaction; 202 with jobId and statusUrl after enqueue); scripts/scenario-worker.mjs:375-383 (startup moves claimed
jobs in the processing list back to the pending queue); scripts/scenario-worker.mjs:415-418 (claims a pending job into
processing); scripts/scenario-worker.mjs:465-487 (writes processing, then done or failed result);
server/worldmonitor/scenario/v1/get-scenario-status.ts:130-157 (premium and caller checks; owner record must match the
caller, other owners get not found); server/worldmonitor/scenario/v1/get-scenario-status.ts:159-183 (missing record reads
as pending; returns the stored status, including processing). Simulation and deep-forecast use queues too
(server/_shared/simulation-queue.ts:122-123; scripts/seed-forecasts.mjs:96-97); named in a note only.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram, GW

d = Diagram('Queued scenario jobs',
    'A scenario request is checked, then the owner record and a pending queue entry are written together, and the caller gets a job id and status address. '
    'A background worker claims a pending job, records it as processing, and then records done or failed. '
    'The status route checks premium access and that the caller owns the job before it reads the record. '
    'A missing record reads as pending, so polling can start at once. Simulation and deep-forecast also use queues.')
d.group(24, 24, GW, 440, 'Request', n=1)
d.column(24, 24, [('Scenario request|POST run-scenario', 'coding'), ('Owner and queue|one transaction', 'data')], first=64, h=64, gap=18)
d.notes(24, 24, 440, 'Caller gets a job id and status URL.', 'Refused requests are not queued.')
d.group(624, 24, GW, 440, 'Queued', n=2)
d.column(624, 24, [('Owner record|binds the job to the caller', 'data'), ('Pending queue|waits for a worker', 'write')], first=64, h=64, gap=18)
d.notes(624, 24, 440, 'Written in the same transaction.', 'Unconfirmed writes fail the request.')
d.arrow('M576 260H624', label='job stored', at=(600, 250))
d.group(624, 500, GW, 364, 'Worker', n=3)
d.column(624, 500, [('Claim job|pending to processing', 'coding'), ('Record result|processing, then done or failed', 'coding')], first=64, h=64, gap=18)
d.notes(624, 500, 364, 'Restart moves claimed jobs to pending.', 'Processing is recorded before compute.')
d.arrow('M900 464V500', label='claimed job', at=(900, 482))
d.group(24, 500, GW, 364, 'Status', n=4)
d.column(24, 500, [('Client polls|any time after the 202', 'data'), ('Status route|premium and owner check', 'review'), ('Reply|pending · processing · done · failed', 'plan')], first=64, h=64, gap=18)
d.notes(24, 500, 364, 'Missing record reads as pending.', 'Other callers get not found.')
d.arrow('M624 700H576', label='record read', at=(600, 690))
d.save(Path(__file__).with_suffix('.svg'))
