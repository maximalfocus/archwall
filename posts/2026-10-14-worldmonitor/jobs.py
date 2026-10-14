"""Queued scenario jobs at worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
Sources: server/worldmonitor/scenario/v1/run-scenario.ts:69-105 (premium request; owner SET and queue
RPUSH in one transaction; 202 with jobId and statusUrl after enqueue); scripts/scenario-worker.mjs:21-22
(pending and processing queues), 375-380 (startup moves processing jobs back to pending), 415-418
(claims a job from pending into processing), 465-487 (writes processing, then done or failed result);
server/worldmonitor/scenario/v1/get-scenario-status.ts:130-168 (premium and owner checks; missing owner
or result returns pending; otherwise the stored status). Simulation and deep-forecast use queues
too (server/_shared/simulation-queue.ts:122-123; scripts/seed-forecasts.mjs:96-97); named in a note only.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram, GW

d = Diagram('Queued scenario jobs',
    'A scenario request is checked, then stored with an owner record and placed on a pending queue, and the caller gets a job id and status address. '
    'A background worker claims the job from the pending queue, marks it processing, computes it, and records done or failed. '
    'Clients poll the status endpoint at any time; until a worker record exists it reports pending. Simulation and deep-forecast also use queues.')
d.group(24, 24, GW, 440, 'Request', n=1)
d.column(24, 24, [('Scenario request|POST run-scenario', 'coding'), ('Gateway checks|access before queueing', 'review')], first=64, h=64, gap=18)
d.notes(24, 24, 440, 'Caller gets a job id and status URL.', 'Refused requests are not queued.')
d.group(624, 24, GW, 440, 'Queued', n=2)
d.column(624, 24, [('Owner record|written with the job', 'data'), ('Pending queue|waits for a worker', 'write')], first=64, h=64, gap=18)
d.notes(624, 24, 440, 'Owner and queue are written together.', 'Unconfirmed writes fail the request.')
d.arrow('M576 260H624', label='job stored', at=(600, 250))
d.group(624, 500, GW, 364, 'Worker', n=3)
d.column(624, 500, [('Claim job|pending to processing', 'coding'), ('Compute scenario|processing, then result', 'coding')], first=64, h=64, gap=18)
d.notes(624, 500, 364, 'Result: done or failed.', 'Restart returns claimed jobs to pending.')
d.arrow('M900 464V500', label='claimed job', at=(900, 482))
d.group(24, 500, GW, 364, 'Status', n=4)
d.column(24, 500, [('Client polls|any time after the 202', 'data'), ('Status reply|pending · done · failed', 'plan')], first=64, h=64, gap=18)
d.notes(24, 500, 364, 'Pending until a worker record exists.', 'Simulation and deep-forecast use queues too.')
d.arrow('M624 700H576', label='worker record', at=(600, 690))
d.save(Path(__file__).with_suffix('.svg'))
