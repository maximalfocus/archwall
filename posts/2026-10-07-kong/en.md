Kong is an open-source API gateway built on Nginx. Apps call Kong, and Kong passes each call on to the right backend. On the way it can check who is calling, limit traffic and log the call.

**One call.** Kong matches a route, runs the plugins for it, picks a backend and sends the answer back. No matching route means a 404.

![](request.svg)

**Plugins** do most of the work. 45 come bundled: auth, traffic limits, rewrites, logs and metrics.

![](plugins.svg)

**Plugin rules.** Loading a plugin doesn't turn it on. Turned on, the most specific setting wins, and higher priority runs first. You can write your own in Lua, or in Go or JavaScript through a plugin server.

![](plugin-rules.svg)

**Picking a backend.** An upstream spreads calls over several targets. Round-robin is the default. Health checks are off until you set them. A failed call is retried, up to 5 times by default.

![](balance.svg)

**Config** goes in through the Admin API, Kong Manager or a file. It lives in Postgres, or in memory with no database (DB-less).

![](config.svg)

**Hybrid mode** (a `role` setting) splits the work. A control plane holds the database and pushes the whole config to data planes, which serve the traffic.

![](hybrid.svg)

**AI plugins** put Kong in front of LLMs. AI Proxy speaks one call shape and translates it for 9 providers. Token logging is off by default.

![](ai.svg)

**Running it.** The `kong` command prepares, starts, reloads and drains a node. The Status API on port 8007 reports health and metrics.

![](ops.svg)
