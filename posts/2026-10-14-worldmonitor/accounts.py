"""WorldMonitor identity, payments, durable state and shared access.
scripts/_seed-history.mjs:12-15 (history seeding skipped when Convex, relay secret or OpenRouter config is missing).
Source: koala73/worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
src/services/clerk.ts:876-881: Clerk session JWT retrieval.
server/auth-session.ts:56-60,259-262: JWKS and JWT verification.
api/user-prefs.ts:27-30,305-341: verified edge API reads/writes Convex preferences.
api/notification-channels.ts:7-9,25-32: Clerk validation and Convex relay.
convex/http.ts:1204-1301: preferences, followed-country and entitlement relays.
convex/schema.ts:115-245: durable preferences, channels, alert rules, followed countries.
api/create-checkout.ts:131,216: authenticated edge checkout to Convex relay.
convex/payments/checkout.ts:404-411: Dodo checkout creation tied to user metadata.
convex/payments/webhookHandlers.ts:39-81,228-252,309-317: verify signature, process events.
convex/entitlements.ts:25-88: user and gateway entitlement queries.
server/_shared/entitlement-check.ts:551-668: Redis entitlement cache and Convex fallback.
api/mcp/auth.ts:6,28,425-440: OAuth bearer and user API key authentication.
api/mcp/dispatch.ts:105-117: MCP tool reads directly from Upstash caches.
api/mcp/registry/rpc-tools.ts:1173-1179: signed MCP call into a domain API route.
server/gateway.ts:1497-2104,2424-2441: identity admission and domain handler execution.
convex/intelHistory.ts:11-30: seeder-ingested durable intelligence timeline/search.
convex/schema.ts:1880-1913: intelligence rows and semantic vector index.
Scope: account and intelligence persistence are distinct from operational Redis cache.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('Accounts, durable state and access', 'Clerk signs in dashboard users. Edge APIs verify session JWTs and persist preferences, followed countries, notification settings and subscription state in Convex. Dodo checkout sends signed payment webhooks that update subscription records. External agents use API keys or MCP OAuth; MCP domain tools can call the same domain handlers through authenticated requests. Redis caches access rights while Convex holds durable records. Separately, seeders append intelligence events and vectors to Convex for timeline and semantic search; they are skipped when their config is missing.')

d.group(24, 24, 368, 400, 'Dashboard identity')
d.column(24,24,[('Clerk sign-in|session JWT', 'coding'),('Edge account APIs|verify JWT with JWKS','review'),('Preferences + alerts|read / write requests','coding')],w=308,gap=28)
d.arrow('M208 152V180', label='JWT', at=(259,170))
d.arrow('M208 244V272', label='user identity', at=(294,262))
d.note(208,378,'Account routes relay to Convex.')

d.group(416,24,368,400,'Convex app state')
d.column(416,24,[('User preferences|per dashboard variant','write'),('Followed countries|notification rules + channels','write'),('Subscription records|plan + payment status','write'),('Access rights|entitlement queries','plan')],w=308,h=60,gap=14,first=64)
d.arrow('M392 280H416',label='sync',at=(404,267))

d.group(808,24,368,400,'Convex history')
d.column(808,24,[('Seeders|events + embeddings','coding'),('Intelligence history|durable rows + vector index','write'),('Timeline + search|chronology / similarity','coding')],w=308,gap=28)
d.arrow('M992 152V180',label='append',at=(1060,170))
d.arrow('M992 244V272',label='query',at=(1050,262))
d.note(992,378,'Skipped when its config is missing.')

d.group(24,500,368,364,'Payment flow')
d.column(24,500,[('Edge checkout API|verified signed-in user','review'),('Convex → Dodo|create checkout session','coding'),('Signed Dodo webhook|verify then update records','review')],w=308,h=60,gap=36,first=60)
d.arrow('M208 620V656',label='checkout',at=(280,644))
d.arrow('M208 716V752',label='payment event',at=(285,740))
d.arrow('M208 424V500',label='user request',at=(208,467))
d.arrow('M392 750H404V460H600V424',label='subscription update',at=(505,450))

d.group(416,500,368,364,'External agents')
d.column(416,500,[('SDK / CLI / MCP client|API key / MCP OAuth','coding'),('REST / MCP entry|resolve caller identity','review'),('MCP domain tools|authenticated HTTP calls','coding')],w=308,h=60,gap=36,first=60)
d.arrow('M600 620V656',label='credentials',at=(688,644))
d.arrow('M600 716V752',label='tool request',at=(685,740))
d.note(600,837,'MCP also has direct cache tools.')

d.group(808,500,368,364,'Domain access')
d.column(808,500,[('Redis entitlement cache|Convex fallback on miss','data'),('Shared domain gateway|access checks + limits','review'),('Domain handlers|execute admitted requests','coding')],w=308,h=60,gap=36,first=60)
d.arrow('M992 620V656',label='access rights',at=(1073,644))
d.arrow('M992 716V752',label='admitted call',at=(1070,740))
d.note(992,837,'Redis is a cache; Convex stores records.')
d.arrow('M784 680H808',label='call',at=(796,667))
d.arrow('M808 590H796V470H700V424',label='read rights',at=(732,460))
d.save(Path(__file__).with_suffix('.svg'))
