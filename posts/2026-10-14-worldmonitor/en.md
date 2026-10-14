World Monitor turns news, markets, tracking feeds and event records into maps and panels. Railway collects and publishes datasets; Redis shares them across readers. Convex keeps accounts and intelligence history.

Relays, scheduled seed bundles and retailer scrapers have distinct publishing paths. Bootstrap loads cached datasets into the dashboard; health checks expose stale or missing data.

![](ingestion.svg)

Protobuf contracts generate domain clients and routes. The gateway checks access, limits requests and controls response caching. Operational endpoints and MCP have separate entry points.

![](gateway.svg)

AppContext connects loaders, panels and maps. Storage preserves preferences and history. Polling pauses in hidden tabs and catches up when they return.

![](browser.svg)

Analysis and scoring combine signals, while breaking alerts keep RSS and siren channels separate. Browser ML needs its runtime setting or desktop mode. API news summaries need entitlement and provider configuration; browser T5 offers a fallback.

![](intelligence.svg)

Clerk identifies users. Dodo payment events update Convex entitlements. Preferences, notifications, keys and agent access use these account services.

![](accounts.svg)

Tauri runs a Node sidecar with keyring-backed secrets. Cloud-preferred routes and fallback still use hosted APIs. Container builds offer either a frontend proxy or a local API runtime.

![](desktop.svg)

Build checks, cloud deployments and distributed releases have separate workflows. Freshness probes, access checks, deployment audits and Sentry watch production.

![](ops.svg)
