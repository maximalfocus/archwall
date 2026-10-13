"""pi-durable: Storage backends and ownership. Source: earendil-works/pi at 7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6; packages/durable/README.md:657-691; docs/spec.md:5103-5181; src/storage/sqlite/node.ts:184-192; src/storage/jsonl/storage.ts:257,510-543. Run: python3 storage.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram

d = Diagram('Storage backends and ownership', 'The host chooses a storage implementation. Memory is temporary and stores detached copies. Node SQLite stores records and document bases plus deltas; a SQL transaction is a Session commit. Its WAL and synchronous NORMAL settings cover process crashes, while a recent commit may be lost on host or power failure. Cloudflare uses the SQLite storage of a Durable Object with its transactions. JSONL writes prepared sidecars and then a main commit marker; recovery keeps confirmed records. JSONL fsync is optional and does not promise an acknowledged tail survives power failure. It also retains history in memory. A storage has one process owner and no cross-process locking. Custom backends and environments can use shared conformance tests.')
d.pill(24,16,1152,48,"One process owns a store; no cross-process locking")
d.group(24,84,552,380,"Memory · temporary")
d.column(24,84,[("Detached copies|records and documents","data"),("In-process state|lost when the process ends","data")])
d.group(624,84,552,380,"Node SQLite · local database")
d.column(624,84,[("Rows · bases · deltas|one SQL transaction per commit","write"),("WAL · NORMAL|process-crash persistence","write")])
d.notes(624,84,380,"A recent commit may be lost on power or host failure.")
d.group(24,500,552,364,"JSONL · local files")
d.column(24,500,[("Sidecars → main marker|only confirmed writes recover","write"),("History in memory|grows with stored history","data"),("Optional fsync|tail may still be lost on power loss","write")])
d.group(624,500,552,364,"Cloudflare · custom adapters")
d.column(624,500,[("Durable Object SQLite|storage transactions","write"),("Portable storage cores|SQL facade or FileSystem","coding"),("Shared conformance tests|storage and ExecutionEnv","review")])

d.save(Path(__file__).with_name("storage.svg"))
