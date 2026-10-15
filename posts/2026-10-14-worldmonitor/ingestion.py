"""WorldMonitor ingestion and cache.
Source: koala73/worldmonitor@a1f94681edb0d82968b7926353e538c4a518a591.
Evidence: scripts/ais-relay.cjs:3-4,12593-12606,15110 (AIS WebSocket and RSS);
scripts/_bundle-runner.mjs:5-25 (scheduled members, freshness, time budget);
scripts/ais-relay.cjs:12357-12358 (/ais/snapshot served to Vercel only when WS_RELAY_URL is set: server/worldmonitor/maritime/v1/get-vessel-snapshot.ts:176-177; server/_shared/relay.ts:3-7); scripts/_seed-utils.mjs:572-640,1230-1271,2443-2466,2868-2955
(validation, canonical publish, opt-in envelopes, atomic extra-key/meta pair);
consumer-prices-core/src/jobs/publish.ts:139-220 (snapshot freshness gates);
consumer-prices-core/src/db/client.ts:1-17,consumer-prices-core/src/jobs/scrape.ts:343-372,
consumer-prices-core/src/jobs/aggregate.ts:157-178 (PostgreSQL observations and computed indices);
scripts/seed-consumer-prices.mjs:4-15 (core scrape/aggregate/publish owns writes);
api/bootstrap.js:57-58,292-302 (tier registry and Redis GET pipeline);
src/services/bootstrap.ts:128-131 (hydration Map read and eviction);
api/seed-health.js:57-83 (metadata freshness), api/health.js (operational probes).
No cron count, timing defaults, or blanket multi-key atomicity claim.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('Data collection and delivery', 'Railway relays collect streams and RSS. Scheduled seed bundles validate upstream data before publishing Redis keys. Consumer Prices Core stores retailer observations in PostgreSQL and aggregates prices into snapshots. Redis carries canonical data, optional freshness envelopes and seed metadata. Bootstrap batches fast and slow tier reads into a browser hydration cache, while RPC handlers read domain keys. Health checks inspect freshness and service status.')
for x, title in [(24,'Relay'),(416,'Seed bundles'),(808,'Consumer prices')]:
    d.group(x,24,368,368,title)
d.column(24,24,[('AIS WebSocket|RSS proxy','coding'),('Upstream polling|Cached snapshots','coding')],w=308,h=70,gap=36)
d.notes(24,24,368,'Railway service','Snapshots if WS_RELAY_URL is set',w=368)
d.column(416,24,[('Scheduled members|Freshness checks','plan'),('Fetch · validate|Publish keys','coding')],w=308,h=70,gap=36)
d.notes(416,24,368,'Member time budgets','Failed validation keeps old data',w=368)
d.column(808,24,[('Retailer scrape|Price observations','coding'),('PostgreSQL|Price history','write'),('Aggregate prices|Publish snapshots','coding')],w=308,h=64,gap=22)
d.notes(808,24,368,'Fresh data advances seed-meta','Core owns price snapshot writes',w=368)
for x,title in [(24,'Health'),(416,'Upstash Redis'),(808,'Data delivery')]:
    d.group(x,500,368,376,title)
d.column(24,500,[('Seed metadata|Content freshness','critic'),('Service probes|Health endpoints','critic')],w=308,h=70,gap=36)
d.notes(24,500,376,'Checks age and payload presence','Relay status tracks sources',w=368)
d.column(416,500,[('Canonical data|Optional envelopes','write'),('seed-meta keys|Atomic pair helper','write')],w=308,h=70,gap=36)
d.notes(416,500,376,'Envelopes need seed opt-in','Pair helper uses a transaction',w=368)
d.column(808,500,[('Bootstrap tiers|Batched Redis reads','coding'),('Hydration cache|Domain RPC reads','data')],w=308,h=70,gap=36)
d.notes(808,500,376,'Fast and slow tier registry','Hydration values read once',w=368)
d.arrow('M208 392V440H474V500',label='snapshots',at=(335,440))
d.arrow('M600 392V500',label='validated data',at=(600,450))
d.arrow('M992 392V470H726V500',label='price snapshots',at=(905,470))
d.arrow('M416 616H392',label='freshness',at=(404,606))
d.arrow('M784 616H808',label='data',at=(796,606))
d.save(Path(__file__).with_suffix('.svg'))
