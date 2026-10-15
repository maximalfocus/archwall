"""World Monitor build, deployment and observation.
Source commit: a1f94681edb0d82968b7926353e538c4a518a591.
Source paths: .github/workflows/deploy-gate.yml:1-21 (aggregated PR checks);
vercel.json:2-3 (build and ignore commands);
workers/api-cors-preflight/src/index.js:1-6 (CORS preflight and response headers); .github/workflows/railway-registry-sync.yml:45-93;
.github/workflows/convex-deploy.yml; .github/workflows/deploy-worker.yml;
.github/workflows/build-desktop.yml:484-490; .github/workflows/docker-publish.yml:28-48;
.github/workflows/seed-freshness-monitor.yml:125-150;
.github/workflows/live-api-cache-auth.yml; .github/workflows/railway-deploy-drift.yml;
src/main.ts:49-66 (deferred Sentry); src/bootstrap/sentry-init.ts:74-82 (DSN and host gate); vite.config.ts:1081-1120 (PWA cache rules); ARCHITECTURE.md:56-71 (hosting).
This is a catalogue; independent workflows are not a single sequential deployment pipeline.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('Build, deploy and observe',
    'GitHub checks types, code, tests, security, proto generation and stacked merges; Deploy Gate aggregates results for a commit. '
    'Vercel serves the web app and API; Railway runs ingestion; Convex and Cloudflare have separate deployment workflows. '
    'Desktop releases build the Tauri app with its Node sidecar; GHCR publishes container images. '
    'Scheduled probes check data freshness, API cache and authentication, and Railway drift; Sentry reports client faults when a DSN is set. '
    'These are independent checks and deployment surfaces, not one ordered release pipeline.')
for x,y,title in [(24,24,'Change checks'),(624,24,'Cloud deployment'),
                  (24,478,'Distributed builds'),(624,478,'Production observation')]:
    d.group(x,y,552,398,title)
d.column(24,24,[('Types · lint · tests','critic'),('Security · proto · merge checks','review'),
                       ('Deploy Gate|Commit status for PR checks','review')],h=72,gap=26)
d.column(624,24,[('Vercel|Static app · API bundles','coding'),
                        ('Railway|Registry sync · ingestion services','coding'),
                        ('Convex|Durable app backend','coding'),
                        ('Cloudflare Worker|API CORS preflight','coding')],h=60,gap=22)
d.column(24,478,[('Tauri + Node|Desktop release builds','write'),
                        ('Docker images|GHCR publication','write'),
                        ('PWA service worker|Tile cache · network API','write')],h=72,gap=26)
d.column(624,478,[('Health and freshness|Seed age · missing data','critic'),
                        ('Live probes|API access · cache · deploy drift','critic'),
                        ('Sentry|Errors · vitals if DSN set','critic')],h=72,gap=26)
d.save(Path(__file__).with_suffix('.svg'))
