"""WorldMonitor contract and domain gateway.
Source: koala73/worldmonitor a1f94681edb0d82968b7926353e538c4a518a591.
proto/worldmonitor/seismology/v1/service.proto:9-15: HTTP-annotated service contract.
proto/buf.gen.yaml:14-46: TS client/server and OpenAPI generation.
api/seismology/v1/[rpc].ts:1-10: generated routes + handwritten handler in edge gateway.
src/services/generated-rpc-clients.ts:69-77: browser-generated client loading.
server/gateway.ts:1171-1186: CORS preflight and origin rejection.
server/gateway.ts:1497-2104: credential admission and entitlements.
server/gateway.ts:2123-2318: endpoint/user/IP rate limits.
server/gateway.ts:2424-2447: handler execution and error boundary.
server/gateway.ts:2484-2538: successful GET/HEAD-body cache policy, privacy and CDN guard.
server/gateway.ts:2551-2562: optional jmespath projection precedes ETag.
server/gateway.ts:2610-2624: body-derived ETag and conditional 304.
Scope: generated domain RPC routes; operational routes and MCP use separate entry points.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('Contracts and the API gateway', 'HTTP-annotated protobuf services generate TypeScript clients, server routes and OpenAPI. Browser clients send requests through a shared domain gateway. It checks origins, credentials and entitlements, limits requests and invokes handwritten handlers. Successful GET or HEAD bodies receive cache policy, optional JSON projection and ETag validation. Operational APIs and MCP have separate entry points.')
d.group(24, 24, 552, 400, 'Contract and generation')
d.card(54, 88, 'Protobuf services|HTTP paths + types', 'data', w=492)
d.arrow('M300 152V174', label='Buf + sebuf', at=(420,168))
d.card(54, 174, 'Generated TypeScript|clients + server routes', 'write', w=492)
d.card(54, 264, 'Generated OpenAPI|API reference', 'write', w=492)
d.note(300, 378, 'Handlers remain handwritten.')

d.group(624, 24, 552, 400, 'Request entry points')
d.card(654, 88, 'Browser services|generated TS clients', 'coding', w=492)
d.card(654, 184, 'Domain HTTP routes|api/<domain>/v1/[rpc]', 'coding', w=492)
d.card(654, 280, 'Shared gateway|generated routes + handlers', 'coding', w=492)
d.arrow('M900 152V184', label='HTTP requests', at=(1000,175))
d.arrow('M900 248V280', label='route adapter', at=(1000,271))
d.note(900, 388, 'Operational APIs and MCP have separate entries.')
d.arrow('M576 120H624', label='client', at=(600,107))

d.group(624, 500, 552, 364, 'Domain request checks')
d.column(624, 500, [('CORS + origin|preflight or admit', 'review'), ('Credentials + entitlements|resolve caller access', 'review'), ('Rate limits|endpoint + caller', 'review'), ('Route + handler|execute or report error', 'coding')], h=60, gap=14, first=60)
for y in (620,694,768):
    d.arrow(f'M900 {y}V{y+14}')
d.arrow('M900 424V500', label='domain request', at=(900,467))

d.group(24, 500, 552, 364, 'Response policy')
d.card(54, 560, 'Cache policy|public / private / no-store', 'plan', w=492)
d.card(54, 654, 'Optional JSON projection|?jmespath=expression', 'coding', w=492)
d.card(54, 748, 'ETag comparison|unchanged → 304', 'plan', w=492)
d.arrow('M300 624V654', label='body', at=(380,645))
d.arrow('M300 718V748', label='response bytes', at=(410,739))
d.note(300, 841, 'Successful GET / HEAD responses with a body.')
d.arrow('M624 812H600V592H576', label='result', at=(600,730))
d.save(Path(__file__).with_suffix('.svg'))
