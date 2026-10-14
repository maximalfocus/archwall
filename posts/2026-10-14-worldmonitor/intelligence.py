"""Intelligence paths at worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
Sources: server/worldmonitor/intelligence/v1/get-risk-scores.ts:752-790 (server reads its own Redis keys, not browser clusters); src/app/data-loader.ts:113,2227-2269 (browser geo convergence and clustering); src/services/rss.ts:341-354,399-407; src/services/clustering.ts:51-112;
src/app/data-loader.ts:2227-2269; src/services/threat-classifier.ts:84-92;
src/services/geo-convergence.ts:38-83; src/services/signal-aggregator.ts:1-5;
server/worldmonitor/intelligence/v1/get-risk-scores.ts:872-878,1245-1280,
1328-1385,1587-1601,1694-1706; scripts/ais-relay.cjs:6087-6120;
server/worldmonitor/infrastructure/v1/list-temporal-anomalies.ts:265-267,327-347;
src/services/summarization.ts:112-137,202-247,320-402;
src/App.ts:2457-2476; src/workers/ml.worker.ts:174-238;
src/services/breaking-news-alerts.ts:54-57,193-237,252-310,313-340.
Scope: selected intelligence mechanisms, not every specialty domain product.
Server owns risk computation; Railway warm-pings that RPC, not a second scorer.
Summarization provider ordering is scoped to normal mode; beta has a warm-local
first path. Optional browser ML is configured on web and available on desktop.
Sentiment and NER are worker capabilities, not claimed mandatory news stages.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from archdiagram import Diagram

d=Diagram('From observations to signals and summaries',
 'In the browser, news items receive keyword threat labels and locations, then word-overlap clustering with '
 'optional semantic refinement. Cached physical and news observations also feed server country '
 'and strategic risk, geographic correlations and seasonal-count anomalies. Risk health checks '
 'source coverage; anomalies require enough baseline samples. Optional local ML supplies '
 'embeddings, sentiment and named entities. Summary requests use configured entitled APIs '
 'Ollama then OpenRouter in normal mode, followed by available browser T5; beta can try '
 'already-loaded local T5 first. RSS breaking alerts and OREF sirens form distinct notification inputs.')
d.group(24,70,552,400,'Browser news interpretation')
d.column(24,70,[('RSS / feed digest|headlines + article context','data'),('Keyword classification|threat level + category','critic'),('Location extraction|map markers + country context','coding'),('News clustering|word overlap + optional vectors','coding')],first=56,h=58,gap=14,w=492)
d.notes(24,70,400,'Clustering: analysis worker or local fallback.','Optional API reclassification requires entitlement.')
d.group(624,70,552,400,'Server scores and browser signals')
d.column(624,70,[('Redis observations|news · conflict · cyber · more','data'),('Server country + strategic risk|baselines + observed activity','critic'),('Geographic correlations|browser · signal overlap','critic'),('Temporal anomalies|counts vs seasonal baseline','critic')],first=56,h=58,gap=14,w=492)
d.notes(624,70,400,'Risk health tracks source coverage.','Anomalies need enough baseline samples.')
d.group(24,540,552,336,'Optional AI and summaries')
d.column(24,540,[('Optional browser ML|embeddings · sentiment · entities','coding'),('Configured entitled API chain|Ollama → OpenRouter','coding'),('Browser T5 summary fallback|when its worker is available','write')],first=56,h=58,gap=14,w=492)
d.notes(24,540,336,'Normal summaries: APIs then browser T5.','Beta: loaded local T5 gets the first try.')
d.group(624,540,552,336,'Breaking alert delivery')
d.column(624,540,[('RSS critical / high items|recency + importance filters','review'),('OREF sirens|dedicated real-time input','data'),('Banner + notifications|dedupe · channel-specific gates','write')],first=56,h=58,gap=14,w=492)
d.notes(624,540,336,'RSS and sirens keep distinct origins.','RSS cooldown does not gate sirens.')
d.arrow('M300 470V540',label='summary input',at=(300,510))
d.arrow('M550 470V505H900V540',label='RSS alert items',at=(724,510))
d.save(Path(__file__).with_suffix('.svg'))
