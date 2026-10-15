"""Browser composition at worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
Sources: src/main.ts:650-654; src/App.ts:1521-1625,2416-2422,2457-2476,
2593-2603,2881-2885,2998-3030; src/app/app-context.ts:74-103;
src/config/variant.ts:7,33-58,51-54; src/app/data-loader.ts:993-994;
src/components/MapContainer.ts:732-743; src/services/storage.ts:28-54;
src/utils/panel-storage.ts:25-47; src/workers/analysis.worker.ts:74-120;
src/services/ml-worker.ts:260,551; src/app/refresh-scheduler.ts:135-159,174-199;
src/app/event-handlers.ts:853-867. Variant defaults: src/config/index.ts:66-75.
Local inference is expanded in intelligence.svg. Individual panels and map
layers are catalog details; routing, desktop and backend have separate figures.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('From shared data to the dashboard',
    'App starts storage and language services, hydrates bootstrap data, and shares mutable AppContext '
    'with layout and data-loading managers. Variants choose defaults. Panels and lazy map renderers '
    'show the resulting data. Local storage preserves preferences and history; workers move analysis '
    'off the UI thread. Refresh pauses in hidden tabs and staggers stale work when they return.')
for x, title in [(24, 'Startup'), (416, 'Shared application'), (808, 'Visible dashboard')]:
    d.group(x, 70, 368, 382, title)
d.column(24,70,[('main.ts → App.init', 'coding'),('Storage + language', 'coding'),('Bootstrap|fast + background slow', 'data')],w=308)
d.notes(24,70,382,'Fast tier precedes layout.','Slow tier feeds visible data.',w=368)
d.column(416,70,[('Variant config|panels · layers · defaults', 'plan'),('AppContext|data + UI references', 'data'),('Layout + data loaders|near-viewport loading', 'coding')],w=308)
d.notes(416,70,382,'Web: subdomain; localhost stored or build.','Desktop: stored choice / build.',w=368)
d.column(808,70,[('Panels|news · markets · signals', 'write'),('Flat map|deck.gl / mobile SVG', 'write'),('Optional globe|globe.gl', 'write')],w=308)
d.notes(808,70,382,'MapContainer loads its renderer','after painting a stable shell.',w=368)
d.arrow('M360 452V475H448V452',label='hydrated data',at=(404,480))
d.arrow('M752 452V475H840V452',label='view data',at=(796,480))
for x, title in [(24, 'Browser storage'), (416, 'Background workers'), (808, 'Refresh loop')]:
    d.group(x,522,368,354,title)
d.column(24,522,[('localStorage|preferences + panel layout', 'write'),('IndexedDB|baselines + snapshots', 'write')],w=308)
d.notes(24,522,354,'Preferences restore the view.','Baselines and snapshots persist.',w=368)
d.column(416,522,[('Analysis worker|clustering + correlation', 'coding'),('Optional ML worker|web setting / desktop', 'coding')],w=308)
d.notes(416,522,354,'Messages return computed results.','Local AI starts in background.',w=368)
d.column(808,522,[('RefreshScheduler|per-source poll lanes', 'plan'),('Visibility events|pause + stale catch-up', 'plan')],w=308)
d.notes(808,522,354,'In-flight guard bounds overlap.','Catch-up starts in staggered order.',w=368)
d.arrow('M208 522V452',label='saved state',at=(208,490))
d.arrow('M600 452V522',label='jobs / results',at=(600,490))
d.arrow('M992 522V452',label='fresh data',at=(992,490))
d.save(Path(__file__).with_suffix('.svg'))
