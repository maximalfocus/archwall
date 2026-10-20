"""Snowflake loading paths. Docs snapshot 2026-10-20:
data-load-overview.md:18-23, 76-115; intro-key-concepts.md:77-85.
https://docs.snowflake.com/en/user-guide/data-load-overview.md
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('Snowflake loading: three paths into tables',
    'Files in internal or external stages can be loaded in bulk by COPY INTO using a chosen virtual warehouse, or continuously by Snowpipe using Snowflake-provided serverless compute. Snowpipe Streaming writes rows directly without a file stage. Loaded Snowflake table data is stored in compressed columnar micro-partitions in cloud storage.')
d.group(24, 24, 552, 380, 'Files in cloud storage')
d.column(24, 24, [('Internal stage', 'data'), ('External stage', 'data')], first=80, h=76, gap=30)
d.notes(24, 24, 380, 'Files wait in a stage')
d.group(624, 24, 552, 380, 'File loading choices')
d.column(624, 24, [('COPY INTO|Chosen warehouse', 'coding'), ('Snowpipe|Serverless compute', 'coding')], first=80, h=76, gap=30)
d.notes(624, 24, 380, 'Batch or continuous file arrival')
d.group(624, 492, 552, 384, 'Table storage')
d.column(624, 492, [('Snowflake tables', 'write'), ('Compressed columns|Micro-partitions', 'write')], first=80, h=76, gap=30)
d.group(24, 492, 552, 384, 'Direct row stream')
d.column(24, 492, [('Producer · Kafka connector', 'coding'), ('Snowpipe Streaming|No file stage', 'coding')], first=80, h=76, gap=30)
d.notes(24, 492, 384, 'Rows go straight to a table')
d.arrow('M576 220H624', label='staged files', at=(600, 202))
d.arrow('M900 404V492', label='loaded rows', at=(900, 449))
d.arrow('M576 682H624', label='rows', at=(600, 662))
d.save(Path(__file__).with_suffix('.svg'))
