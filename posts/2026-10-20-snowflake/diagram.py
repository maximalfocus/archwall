"""Snowflake platform map. Snowflake docs snapshot 2026-10-20:
intro-key-concepts.md:41-57, 77-85, 124-155, 273-278, 299-314.
https://docs.snowflake.com/en/user-guide/intro-key-concepts.md
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('Snowflake: shared data, separate compute',
    'Clients send SQL and management requests to cloud services. Cloud services authenticate, manage metadata, plan queries and dispatch work. Independent virtual warehouses execute against shared storage. Loading writes Snowflake tables; shares expose selected objects to other accounts through services and metadata without copying data.')
d.group(24, 24, 552, 386, 'People and tools')
d.column(24, 24, [('Snowsight · CLI · drivers', 'coding'), ('Apps · APIs · connectors', 'coding')], first=82, h=76, gap=30)
d.notes(24, 24, 386, 'SQL · account management')
d.group(624, 24, 552, 386, 'Cloud services')
d.column(624, 24, [('Identity · access control', 'review'), ('Metadata · catalog', 'data'), ('Parse · optimize · dispatch', 'plan')], first=67)
d.group(624, 494, 552, 382, 'Independent compute')
d.column(624, 494, [('Virtual warehouse A|Queries · loads', 'coding'), ('Virtual warehouse B|Other workloads', 'coding')], first=70, h=76, gap=30)
d.notes(624, 494, 382, 'Each warehouse has its own compute')
d.group(24, 494, 552, 382, 'Data and collaboration')
d.column(24, 494, [('Snowflake tables|Cloud object storage', 'write'), ('Iceberg · hybrid tables', 'write'), ('Shares to other accounts', 'data')], first=62)
d.arrow('M576 240H624', label='requests', at=(600, 220))
d.arrow('M900 410V494', label='plans', at=(900, 456))
d.arrow('M624 682H576', label='reads · writes', at=(600, 663))
d.save(Path(__file__).with_suffix('.svg'))
