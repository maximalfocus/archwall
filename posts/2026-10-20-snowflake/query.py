"""Snowflake query execution. Docs snapshot 2026-10-20:
intro-key-concepts.md:41-49, 124-155; warehouses-overview.md:251-288;
tables-clustering-micropartitions.md:69-82.
https://docs.snowflake.com/en/user-guide/intro-key-concepts.md
https://docs.snowflake.com/en/user-guide/warehouses-overview.md
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('Snowflake query: plan, execute, return',
    'A client sends a SQL statement to cloud services. Services authenticate and control access, parse and optimize the query, then dispatch it. An independent virtual warehouse executes the work using local data portions and shared persisted storage. For Snowflake tables, micro-partition metadata helps prune irrelevant partitions and columns. The warehouse produces the query output and results return to the client. Warehouses can auto-resume and auto-suspend when configured.')
d.pill(365, 16, 470, 52, 'Client sends SQL')
d.group(24, 84, 552, 380, 'Cloud services', 1)
d.column(24, 84, [('Authenticate · authorize', 'review'), ('Parse · optimize', 'plan'), ('Dispatch query', 'plan')], first=66)
d.group(624, 84, 552, 380, 'Virtual warehouse', 2)
d.column(624, 84, [('Independent compute cluster', 'coding'), ('Parallel query workers', 'coding')], first=78, h=76, gap=30)
d.notes(624, 84, 380, 'Queues when capacity is used')
d.group(624, 500, 552, 364, 'Snowflake table data', 3)
d.column(624, 500, [('Micro-partition metadata', 'data'), ('Compressed column data', 'write')], first=72, h=76, gap=30)
d.notes(624, 500, 364, 'Prune partitions and columns')
d.group(24, 500, 552, 364, 'Result', 4)
d.column(24, 500, [('Rows return|to the client', 'data')], first=100, h=82)
d.notes(24, 500, 364, 'Warehouse can pause when idle')
d.arrow('M600 68V76H300V84')
d.arrow('M576 300H624', label='plan', at=(600, 281))
d.arrow('M900 464V500', label='reads', at=(900, 487))
d.arrow('M624 440H600V682H576', label='query output', at=(600, 663))
d.arrow('M24 700H12V40H365', back=True, label='result', at=(170, 29))
d.save(Path(__file__).with_suffix('.svg'))
