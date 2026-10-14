"""Market quote reads at worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
Sources: server/worldmonitor/market/v1/list-market-quotes.ts:4-9 (seed-first contract),
383 (seed read of market:stocks-bootstrap:v1), 304-322 (per-symbol Redis-cached gap fetch;
not-found negative-cached, transient provider errors not cached via cacheFetcherErrors:false).
Scope: the market-quote read path only; other handlers read seeded keys or caches.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram, GW

d = Diagram('Quote reads: seed first, live fill for gaps',
    'A quote request first reads the fixed market seed snapshot and keeps the requested symbols it has. '
    'Symbols missing from the seed, such as custom tickers, go to a provider one at a time. '
    'Each lookup uses a per-symbol Redis cache; not-found answers are cached briefly and transient errors are not. '
    'The response merges seed hits and live fills in the requested order, and lists a reason for each unavailable symbol.')
d.group(24, 24, GW, 440, 'Request', n=1)
d.column(24, 24, [('Symbol list|default or custom', 'coding'), ('Seed read|market:stocks-bootstrap', 'data')], first=64, h=64, gap=18)
d.notes(24, 24, 440, 'Seed hits keep the requested order.', 'Seed answers the default symbols.')
d.group(624, 24, GW, 440, 'Seed misses', n=2)
d.column(624, 24, [('Missing symbols|custom or dropped', 'plan'), ('Gap cache|per symbol · 5 min Redis', 'write')], first=64, h=64, gap=18)
d.notes(624, 24, 440, 'Not-found answers are cached briefly.', 'Provider errors are not cached.')
d.arrow('M576 260H624')
d.group(624, 500, GW, 364, 'Live fill', n=3)
d.column(624, 500, [('Provider quote|deadline-bounded', 'coding'), ('Outcome|quote · not found · reason', 'data')], first=64, h=64, gap=18)
d.notes(624, 500, 364, 'Rate limits and timeouts are reported.', 'The whole fill shares one deadline.')
d.arrow('M900 464V500')
d.group(24, 500, GW, 364, 'Merged response', n=4)
d.column(24, 500, [('Seed hits + live fills|requested order', 'coding'), ('Unavailable reasons|one per symbol', 'data')], first=64, h=64, gap=18)
d.notes(24, 500, 364, 'Unknown symbols get a reason, not a guess.', 'Hits then fills form one list.')
d.arrow('M624 700H576')
d.save(Path(__file__).with_suffix('.svg'))
