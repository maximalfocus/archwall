"""pi-durable: What the host installs. Source: earendil-works/pi at 7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6; packages/durable/README.md:129-169,259-287,293-367; src/tools/index.ts:33-46; src/tool-search/tool-search.ts; src/codemode/codemode.ts. Run: python3 extensions.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram

d = Diagram('What the host installs', 'The host installs named extensions into an in-memory registry. Extensions supply tools, prompt sections, hooks, wrappers and custom tasks. Conversations store names and agent choices, not extension code; reinstall code after restart. Reload replaces an extension in place; already running code keeps its implementation. CodingTools is installed explicitly and uses ExecutionEnv for files and processes. An optional Photon image processor converts and resizes read images. Optional tool-search loads deferred tools for a later model request. Optional codemode takes a host-provided sandbox: scripts discover and call nested tools, and start data plus a result journal let deterministic execution replay after a restart. ')
d.pill(24,16,1152,48,"Extensions are supplied by the host; conversations keep their names")
d.group(24,84,552,380,"Registry and agent choices")
d.column(24,84,[("Install · reload|extension code in the host","coding"),("Tools · sections · tasks|behaviour by selected names","coding"),("Hooks · wrappers|block or adjust calls","review")])
d.notes(24,84,380,"Reinstall code after a restart.","Running code keeps its implementation.")
d.group(624,84,552,380,"CodingTools · install explicitly")
d.column(624,84,[("read · write · edit · bash|files and processes","coding"),("Host ExecutionEnv|Node or custom environment","coding"),("Optional Photon images|convert and resize for read","coding")])
d.group(24,500,552,364,"Optional tool-search extension")
d.column(24,500,[("Deferred tools|not yet offered to the model","data"),("Search → load tools|offer on a later request","plan"),("Tool names loaded|available on the next request","write")])
d.group(624,500,552,364,"Optional codemode extension")
d.column(624,500,[("Host sandbox|script calls nested tools","coding"),("Tool discovery · results|script controls what it returns","plan"),("Start data · result journal|deterministic replay","write")])

d.save(Path(__file__).with_name("extensions.svg"))
