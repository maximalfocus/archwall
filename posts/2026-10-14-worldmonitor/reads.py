"""Stock and index quote reads at worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
Sources: server/worldmonitor/market/v1/list-market-quotes.ts:383-397 (seed read; error, malformed or
empty seed returns unavailable with no provider call); 417-425 (every symbol seeded: return without
provider call); 296 (missing symbols resolved with forEachWithConcurrency); 263-285 (no configured
provider: notConfigured, no fan-out); 304-322 (per-symbol cachedFetchJson: cache hit returns without
calling the provider, miss calls it); 432-452 (merge loop in requested order, unavailable reasons).
server/_shared/redis.ts:922-940,1029-1040 (cachedFetchJson reads the cache before the fetcher).
Scope: stock and index quotes only; other quote domains are not drawn.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram, GW

d = Diagram('Stock and index quotes: seed first',
    'A stock or index quote request reads the fixed market seed first. A missing or empty seed returns unavailable without calling a provider. '
    'Symbols found in the seed are answered. Only symbols missing from the seed check their per-symbol cache; a cache hit answers without a provider call. '
    'A provider is called only on a cache miss, and only when one is configured. The answer keeps the requested order and gives a reason for each unavailable symbol.')
d.group(24, 24, GW, 440, 'Seed check', n=1)
d.column(24, 24, [('Quote request|stock or index symbols', 'coding'), ('Seed snapshot|market:stocks-bootstrap', 'data')], first=64, h=64, gap=18)
d.notes(24, 24, 440, 'Missing or empty seed: unavailable.', 'No provider call is made.')
d.group(624, 24, GW, 440, 'Seed lookup', n=2)
d.column(624, 24, [('Symbols found|answered from the seed', 'data'), ('Symbols missing|not in the seed', 'plan')], first=64, h=64, gap=18)
d.notes(624, 24, 440, 'All found: answer now, no provider call.', 'Missing symbols continue below.')
d.arrow('M576 260H624', label='seed rows', at=(600, 250))
d.group(624, 500, GW, 364, 'Symbol gaps', n=3)
d.column(624, 500, [('Per-symbol cache|Redis hit answers', 'write'), ('Provider call|cache miss, if configured', 'coding')], first=64, h=64, gap=18)
d.notes(624, 500, 364, 'A cache hit makes no provider call.', 'Provider errors are not cached.')
d.arrow('M900 464V500', label='missing symbols', at=(900, 482))
d.group(24, 500, GW, 364, 'Answer', n=4)
d.column(24, 500, [('Quotes|seed and gap answers', 'coding'), ('Unavailable symbols|one reason each', 'data')], first=64, h=64, gap=18)
d.notes(24, 500, 364, 'Output keeps the requested order.', 'Unknown symbols get a reason.')
d.arrow('M624 700H576', label='gap answers', at=(600, 690))
d.save(Path(__file__).with_suffix('.svg'))
