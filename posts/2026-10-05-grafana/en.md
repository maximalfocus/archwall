Grafana draws charts and sends alerts on data that lives in your own systems. Each time a panel loads, it asks the system that holds the data.

**One program.** The server serves the web app and the APIs, checks every request, keeps dashboards and rules, and runs the queries.

**A panel's data.** The server checks the caller, splits the query by data source and asks them in parallel. Answers come back as data frames.

![](query.svg)

**Plugins.** Data sources, panels and apps are plugins. Most data sources are installed at start, not built in. Unsigned plugins are blocked by default.

![](plugins.svg)

**Dashboards** are JSON, built in the web app or loaded from files or Git.

![](dashboards.svg)

**Storage.** Grafana's own database is a SQLite file by default, or MySQL or Postgres. Dashboards now sit in a newer, versioned store in that same database.

![](storage.svg)

**Alerts.** A scheduler ticks every 10 seconds and runs due rules. Firing alerts go to the built-in Alertmanager.

![](alerting.svg)

It groups them, holds back silenced ones, and sends the rest to 23 kinds of contact point.

![](notify.svg)

**Access.** People sign in with a password, LDAP or single sign-on, and get a role in each organisation. SAML and custom roles are Enterprise.

![](access.svg)

**Sharing.** A link needs sign-in. A snapshot is a copy of the data. Anyone with a public dashboard's link can view it; it runs only its saved queries.

![](sharing.svg)

**Running it.** Start with one server. To grow, run more behind a load balancer, sharing a MySQL or Postgres database.

![](ops.svg)
