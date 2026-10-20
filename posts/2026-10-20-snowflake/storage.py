"""Snowflake storage types and pruning. Docs snapshot 2026-10-20:
intro-key-concepts.md:61-120; tables-clustering-micropartitions.md:19-42, 69-82.
https://docs.snowflake.com/en/user-guide/intro-key-concepts.md
https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions.md
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('Snowflake storage: table choices and pruning',
    'Snowflake tables store compressed columns in cloud storage as micro-partitions. Their metadata records column ranges and helps prune partitions and columns during a query. Iceberg tables use external cloud storage managed by the customer. Hybrid tables use index-based reads and writes with row locking for transactional workloads.')
d.group(24, 24, 552, 392, 'Snowflake tables')
d.column(24, 24, [('Managed cloud storage', 'write'), ('Columnar micro-partitions', 'write'), ('Range metadata · pruning', 'plan')], first=70)
d.notes(24, 24, 392, 'Columns and partitions can be skipped')
d.group(624, 24, 552, 392, 'Iceberg tables')
d.column(624, 24, [('External cloud storage', 'write'), ('Data · metadata files', 'data')], first=88, h=76, gap=32)
d.notes(624, 24, 392, 'Storage stays outside Snowflake')
d.group(24, 488, 552, 388, 'Hybrid tables')
d.column(24, 488, [('Index-based reads · writes', 'coding'), ('Row locks · constraints', 'review')], first=88, h=76, gap=32)
d.notes(24, 488, 388, 'For transactional workloads')
d.group(624, 488, 552, 388, 'Query work')
d.column(624, 488, [('Virtual warehouse', 'coding'), ('Read matching data', 'data')], first=88, h=76, gap=32)
d.notes(624, 488, 388, 'Storage is separate from compute')
d.save(Path(__file__).with_suffix('.svg'))
