"""Stock and index quote reads at worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
Sources: server/worldmonitor/market/v1/list-market-quotes.ts:47 (seed key market:stocks-bootstrap:v1);
server/worldmonitor/market/v1/list-market-quotes.ts:383-397 (seed read; error, malformed or
empty seed returns unavailable with no provider call); server/worldmonitor/market/v1/list-market-quotes.ts:417-425
(every requested symbol seeded: return without provider call); server/worldmonitor/market/v1/list-market-quotes.ts:263-285
(provider admission: no configured provider gives notConfigured with no cache read; unsupported symbols get notFound;
symbols over the per-request limit get budget); server/worldmonitor/market/v1/list-market-quotes.ts:304-322
(per-symbol cachedFetchJson, reached only for admitted symbols); server/_shared/redis.ts:1031-1034 (cache hit returns
without calling the fetcher, so no provider call); server/worldmonitor/market/v1/list-market-quotes.ts:432-452
(answers merged in requested order with one reason per unavailable symbol).
Scope: stock and index quotes only; other quote domains are not drawn.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram, GW

d = Diagram('Stock and index quotes: seed first',
    'A stock or index quote request reads the fixed market seed first. An invalid or empty seed returns unavailable without calling a provider. '
    'Symbols found in the seed are answered. Missing symbols must first be admitted: a provider has to be configured, support the symbol and fit the per-request limit. '
    'Only admitted symbols check their per-symbol cache, and a cache hit answers without a provider call. A provider is called only on a cache miss. '
    'The answer keeps the requested order and gives a reason for each unavailable symbol.')
d.group(24, 24, GW, 440, 'Seed check', n=1)
d.column(24, 24, [('Quote request|stock or index symbols', 'coding'), ('Seed snapshot|market:stocks-bootstrap:v1', 'data')], first=64, h=64, gap=18)
d.notes(24, 24, 440, 'Invalid or empty seed: unavailable.', 'All symbols found: answer now.')
d.group(624, 24, GW, 440, 'Seed lookup', n=2)
d.column(624, 24, [('Symbols found|answered from the seed', 'data'), ('Symbols missing|not in the seed', 'plan')], first=64, h=64, gap=18)
d.notes(624, 24, 440, 'Found symbols stay in the answer.', 'Missing symbols go on below.')
d.arrow('M576 260H624', label='seed rows', at=(600, 250))
d.group(624, 500, GW, 364, 'Missing symbols', n=3)
d.column(624, 500, [('Provider admitted|configured and supported', 'review'), ('Per-symbol cache|hit answers, no call', 'write'), ('Provider call|cache miss only', 'coding')], first=64, h=64, gap=18)
d.notes(624, 500, 364, 'Not admitted: unavailable, no cache read.', 'Provider errors are not cached.')
d.arrow('M900 464V500', label='missing symbols', at=(900, 482))
d.group(24, 500, GW, 364, 'Answer', n=4)
d.column(24, 500, [('Quotes|seed and fetched answers', 'coding'), ('Unavailable symbols|one reason each', 'data')], first=64, h=64, gap=18)
d.notes(24, 500, 364, 'Output keeps the requested order.', 'Unknown symbols get a reason.')
d.arrow('M624 700H576', label='answers', at=(600, 690))
# Seed hits go straight to the answer; the route runs through the gap between the two rows.
d.arrow('M760 464V482H300V500', label='found symbols', at=(530, 477))
d.save(Path(__file__).with_suffix('.svg'))
