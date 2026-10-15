"""WorldMonitor runtime and deployment choices.
Source: koala73/worldmonitor@a1f94681edb0d82968b7926353e538c4a518a591.
Evidence: docs/architecture.mdx:26 (deployment overview; verify with code);
src-tauri/src/main.rs:94-150,251,330-370,459-496,1648
(OS keyring vault, native bearer-auth loopback proxy, secret sync, enabled fallback);
src/services/runtime.ts:368-435 (API fetch interception; key/retry gated fallback);
src-tauri/sidecar/local-api-server.mjs:769-804,886-899
(selected cloud-preferred routes; Docker disables cloud fallback);
docker/Dockerfile:runtime stage (nginx assets, default API_UPSTREAM);
docker/nginx.conf.template:108 (configured upstream proxy);
Dockerfile:1-7,82-112 (nginx plus Node handlers), docker/supervisord.conf:7-23;
docker-compose.yml:16-35,75-98,106-135
(root image app, relay, Redis REST, Redis; mandatory service secrets and optional keys).
No claim that frontend-only Docker includes Node or Redis. No claim that all
sidecar routes work offline, or that Docker performs public cloud fallback.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from archdiagram import Diagram

d=Diagram('Desktop and Docker choices','Tauri wraps the dashboard. Native Rust owns the operating-system keyring and authenticates loopback calls to a Node sidecar. The sidecar runs local handlers and uses selected cloud-preferred routes or gated fallback. The frontend Docker image serves static assets through nginx and proxies APIs to its configured upstream. The root Docker image combines nginx and Node, with Compose wiring Redis REST, Redis and an AIS relay. Docker mode disables public-cloud fallback; provider keys are optional.')
for x,title in [(24,'Tauri desktop'),(416,'Frontend Docker'),(808,'Full Docker stack')]:
    d.group(x,24,368,852,title)
for y,label,kind in [(100,'Dashboard|API fetch patch','coding'),(260,'Native Rust|OS keyring vault','write'),(420,'Node sidecar|Local handlers','coding'),(650,'Cloud API|Selected routes','coding')]:
    d.card(54,y,label,kind,w=308,h=72)
d.arrow('M208 172V260',label='native IPC',at=(208,217))
d.arrow('M208 332V420',label='loopback + token',at=(208,377))
d.arrow('M208 492V650',label='preferred / fallback',at=(208,571))
d.notes(24,24,852,'Fallback checks keys and retry safety','Rust syncs configured secrets',w=368)
for y,label,kind in [(100,'Built frontend|Static assets','data'),(330,'nginx|API proxy','coding'),(650,'API_UPSTREAM|Cloud or custom','coding')]:
    d.card(446,y,label,kind,w=308,h=72)
d.arrow('M600 172V330',label='serve assets',at=(600,251))
d.arrow('M600 402V650',label='API requests',at=(600,527))
d.notes(416,24,852,'docker/Dockerfile','API_UPSTREAM is configurable',w=368)
for y,label,kind in [(100,'nginx + Node|Local API handlers','coding'),(330,'Redis REST|Redis store','write'),(650,'AIS relay|Provider feeds','coding')]:
    d.card(838,y,label,kind,w=308,h=72)
d.arrow('M992 172V330',label='cache reads / writes',at=(992,251))
d.arrow('M1146 136H1160V527H990V610H1160V686H1146',label='relay requests',at=(1060,527))
d.arrow('M838 686H822V366H838',label='cached data',at=(822,447))
d.notes(808,24,852,'Root Dockerfile + Compose','Provider keys optional · no cloud fallback',w=368)
d.save(Path(__file__).with_suffix('.svg'))
