"""Which plugin runs, and in what order: write or pick, load, scope, order.
Snake order: 1 write or pick (top left) -> 2 load (top right) -> 3 scope (bottom right) -> 4 order (bottom left).
Drawn from Kong/kong at commit 8927af6 (README.md, kong.conf.default, kong/constants.lua, kong/db/dao/plugins.lua,
kong/runloop/plugins_iterator.lua, kong/plugins/*/handler.lua).
Run: python3 plugin-rules.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Which plugin runs, and in what order",
            "In: a plugin, bundled or your own. "
            "1 Write or pick: 45 plugins come bundled, for auth, limits, logs and more; you can write your own "
            "in Lua with the Plugin Development Kit, or in Go or JavaScript through plugin servers set with the "
            "pluginserver_names setting. Wasm filters need the setting wasm = on, which is off by default. "
            "2 Load: the plugins setting, bundled by default, only loads the code; a plugin entity turns it on; "
            "Kong will not start if a configured plugin is not loaded. "
            "3 Scope: a plugin can be set globally or for a route, a service, a consumer or a mix of them; "
            "for each call the most specific of 8 levels wins, route plus service plus consumer first and "
            "global last. "
            "4 Order: plugins run by PRIORITY, higher first, in each phase from rewrite and access to "
            "header_filter, body_filter and log; for example correlation-id 100001, key-auth 1250, "
            "rate-limiting 910 and syslog 4. pre-function runs Lua snippets near the start and "
            "post-function near the end.")

d.pill(L, 16, GW, 48, "In: a plugin, bundled or your own")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Write or pick", 1)
d.column(L, T1, [("45 bundled plugins|auth · limits · logs …", "coding"),
                 ("Your own in Lua|with the Plugin Development Kit", "coding"),
                 ("Go or JavaScript|config: pluginserver_names", "coding")])
d.notes(L, T1, H1, "Wasm filters: config wasm = on (default off)", "")

d.group(R, T1, GW, H1, "Load", 2)
d.column(R, T1, [("plugins = bundled|config: loads the code only", "plan"),
                 ("Plugin entity|turns it on · Admin API or file", "plan"),
                 ("Configured but not loaded|Kong will not start", "review")])

d.group(R, T2, GW, H2, "Scope", 3)
d.column(R, T2, [("Route + service + consumer|the most specific wins", "plan"),
                 ("8 levels|route · service · consumer · mixes", "plan"),
                 ("Global|used when nothing closer is set", "plan")])

d.group(L, T2, GW, H2, "Order", 4)
d.column(L, T2, [("Higher PRIORITY first|correlation-id 100001", "coding"),
                 ("key-auth 1250|before rate-limiting 910", "coding"),
                 ("Each phase in turn|rewrite · access · … · log", "coding")])
d.notes(L, T2, H2, "pre-function runs early · post-function late", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="code", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="enabled", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="chosen", at=(600, T2 + 164))

d.save(Path(__file__).with_name("plugin-rules.svg"))
