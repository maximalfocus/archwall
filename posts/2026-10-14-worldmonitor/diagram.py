"""World Monitor overview, source commit a1f94681edb0d82968b7926353e538c4a518a591.
Source: https://github.com/koala73/worldmonitor/tree/a1f94681edb0d82968b7926353e538c4a518a591
ARCHITECTURE.md:56-71 deployment; scripts/ais-relay.cjs; scripts/_seed-utils.mjs;
server/gateway.ts; convex/schema.ts; src/main.ts:652; src/services/runtime.ts.
The diagram shows logical data movement, not a serial deployment dependency.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('World Monitor: from sources to a shared picture',
    'External news, markets, conflict, climate, ships and aircraft feed Railway relay and seed jobs. '
    'Upstash Redis holds shared datasets and freshness metadata; Convex holds account state and intelligence history. '
    'Vercel APIs and the desktop Node sidecar serve the browser or desktop maps, panels and analysis, '
    'and API, CLI, SDK and MCP consumers. Configured AI providers enrich intelligence. '
    'The remaining figures explain ingestion, gateway, browser, intelligence, accounts, desktop and operations.')
d.group(24, 24, 552, 386, 'Sources and collection')
d.column(24, 24, [('News · markets · events', 'data'), ('Ships · aircraft · climate', 'data'),
                       ('Railway relay · seed jobs', 'coding')], first=66)
d.notes(24, 24, 386, 'RSS / WebSocket / HTTP / price scrapers')
d.group(624, 24, 552, 386, 'Shared stores')
d.column(624, 24, [('Upstash Redis|Datasets · cache · freshness', 'write'),
                       ('Convex|Accounts · intelligence history', 'write')], first=80, h=76, gap=32)
d.group(624, 494, 552, 382, 'Serving and runtime')
d.column(624, 494, [('Vercel|Domain APIs · operational routes', 'coding'),
                        ('Desktop Node sidecar|Local handlers · cloud fallback', 'coding')], first=66, h=76, gap=30)
d.notes(624, 494, 382, 'Contracts · access checks · rate limits')
d.group(24, 494, 552, 382, 'People and software')
d.column(24, 494, [('Browser / desktop|Map · panels · analysis', 'coding'),
                       ('External clients|SDK · CLI · MCP', 'coding')], first=66, h=76, gap=30)
d.notes(24, 494, 382, 'AI enrichment uses configured providers')
d.arrow('M576 285H624', label='datasets', at=(600, 267))
d.arrow('M900 410V494', label='data · state', at=(900, 455))
d.arrow('M624 632H576', label='results', at=(600, 617))
d.arrow('M576 755H624', label='requests', at=(600, 739))
d.save(Path(__file__).with_suffix('.svg'))
