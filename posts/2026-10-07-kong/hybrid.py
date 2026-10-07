"""Hybrid mode: one control plane with the database pushes the whole config to data planes that run without one.
Snake order: 1 control plane (top left) -> 2 package the config (top right) -> 3 data planes receive (bottom right) -> 4 serve traffic (bottom left).
Drawn from Kong/kong at commit 8927af6 (kong.conf.default HYBRID MODE and declarative_config; kong/conf_loader/parse.lua;
kong/clustering/control_plane.lua, data_plane.lua, config_helper.lua, compat/init.lua; kong/constants.lua).
Run: python3 hybrid.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Hybrid mode",
            "In: an admin changes the config on the control plane. Hybrid mode is a setting: role, "
            "which is traditional by default. "
            "1 Control plane, role = control_plane: it needs the Admin API and a database, "
            "and listens for data planes on cluster port 8005. "
            "2 Package the config: it exports the whole config with a hash, fits it to each data plane's "
            "version (same major version, data plane minor version not newer), and compresses it with gzip, "
            "at most 16 MB by default. "
            "3 Data planes receive it, role = data_plane: over a WebSocket secured with mutual TLS, "
            "using a shared certificate by default or certificates from a CA (pki); they must run with "
            "database = off and load the config into LMDB, Kong's local config store. "
            "4 Serve traffic: data planes proxy calls on ports 8000 and 8443, ping the control plane every "
            "30 seconds with their config hash, and can start from a declarative config file when no "
            "cached config exists yet.")

d.pill(L, 16, GW, 48, "In: an admin changes the config")
d.arrow(f"M{L + GW / 2} 64V{T1 - 2}")

d.group(L, T1, GW, H1, "Control plane", 1)
d.column(L, T1, [("Admin API|required here", "plan"),
                 ("Postgres|a database is required", "data"),
                 ("Cluster port 8005|data planes connect here", "review")])
d.notes(L, T1, H1, "Setting: role = control_plane", "")

d.group(R, T1, GW, H1, "Package the config", 2)
d.column(R, T1, [("Export the whole config|with a hash", "write"),
                 ("Fit each data plane|same major · minor not newer", "review"),
                 ("Compress with gzip|up to 16 MB by default", "write")])

d.group(R, T2, GW, H2, "Data planes receive", 3)
d.column(R, T2, [("Secure link|WebSocket over mutual TLS", "review"),
                 ("No database|database = off is required", "data"),
                 ("Load into LMDB|Kong's local config store", "data")])
d.notes(R, T2, H2, "Certificates: shared (default) or pki", "")

d.group(L, T2, GW, H2, "Serve traffic", 4)
d.column(L, T2, [("Proxy calls|ports 8000 · 8443", "coding"),
                 ("Ping every 30 s|sends its config hash", "data"),
                 ("Fallback config file|used if no cached config yet", "data")])
d.notes(L, T2, H2, "Setting: role = data_plane", "")

d.arrow(f"M{L + GW} {T1 + 200}H{R - 2}", label="on change", at=(600, T1 + 188))
d.arrow(f"M{R + 430} {T1 + H1}V{T2 - 2}", label="push", at=(R + 430, T1 + H1 + 24))
d.arrow(f"M{R} {T2 + 176}H{L + GW + 2}", label="new config", at=(600, T2 + 164))

d.save(Path(__file__).with_name("hybrid.svg"))
