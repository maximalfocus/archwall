"""Queued scenario jobs at worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
Sources: server/worldmonitor/scenario/v1/run-scenario.ts:69-105 (owner SET and RPUSH in one
transaction; 202 Accepted with statusUrl; 502 if unconfirmed); scripts/scenario-worker.mjs:3-13,21-24
(always-on worker, BLMOVE dequeue, 30 s block, 24 h result TTL); server/worldmonitor/scenario/v1/get-scenario-status.ts:148-162 (owner then result read). Registry: scripts/railway-services.json:353-355.
Simulation and deep-forecast queues exist too (server/_shared/simulation-queue.ts:122-123;
scripts/seed-forecasts.mjs:96-97); they are described in the post text, not drawn.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram, GW

d = Diagram('Queued scenario jobs',
    'A user scenario request is checked at the gateway, then stored with an owner record and pushed to a Redis queue in one transaction. '
    'It returns 202 Accepted with a status URL. An always-on Railway scenario worker takes the next job, computes the scenario and writes the result with a 24 hour lifetime. '
    'The client polls the status endpoint, which reads the owner record and then the result. Simulation and deep-forecast also use Redis queues.')
d.group(24, 24, GW, 440, 'Request', n=1)
d.column(24, 24, [('Scenario request|POST run-scenario', 'coding'), ('Gateway checks|access and limits', 'review')], first=64, h=64, gap=18)
d.notes(24, 24, 440, 'Accepted jobs return 202 Accepted.', 'Refusals keep 403, 429 or 502.')
d.group(624, 24, GW, 440, 'Queue', n=2)
d.column(624, 24, [('Owner record|SET with 24 h TTL', 'data'), ('Job queue|RPUSH, one transaction', 'write')], first=64, h=64, gap=18)
d.notes(624, 24, 440, 'Both writes must confirm.', 'An unconfirmed write returns 502.')
d.arrow('M576 260H624')
d.group(624, 500, GW, 364, 'Worker', n=3)
d.column(624, 500, [('scenario-worker|always-on Railway service', 'coding'), ('computeScenario|BLMOVE dequeue', 'coding')], first=64, h=64, gap=18)
d.notes(624, 500, 364, 'Waits up to 30 seconds for a job.', 'Writes the result with a 24 h TTL.')
d.arrow('M900 464V500')
d.group(24, 500, GW, 364, 'Status', n=4)
d.column(24, 500, [('get-scenario-status|owner, then result', 'coding'), ('Client polls|statusUrl from the 202', 'data')], first=64, h=64, gap=18)
d.notes(24, 500, 364, 'Pending until the worker writes.', 'Simulation and deep-forecast use queues too.')
d.arrow('M624 700H576')
d.save(Path(__file__).with_suffix('.svg'))
