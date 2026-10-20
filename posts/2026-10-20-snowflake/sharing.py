"""Snowflake secure sharing. Docs snapshot 2026-10-20:
data-sharing-intro.md:17-70; intro-key-concepts.md:140-155, 273-278.
https://docs.snowflake.com/en/user-guide/data-sharing-intro.md
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from archdiagram import Diagram

d = Diagram('Snowflake sharing: access without a data copy',
    'A provider selects database objects and grants them to a share, then adds consumer accounts. The consumer creates a read-only database from that share and grants users access through roles. Snowflake services and metadata expose the provider data without transferring a copy between accounts. The consumer uses its own virtual warehouse to query the shared data.')
d.group(24, 24, 552, 386, 'Provider account')
d.column(24, 24, [('Select database objects', 'data'), ('Grant to share', 'review'), ('Add consumer accounts', 'plan')], first=66)
d.group(624, 24, 552, 386, 'Services · metadata')
d.column(624, 24, [('Share definition', 'data'), ('Access control', 'review')], first=88, h=76, gap=30)
d.notes(624, 24, 386, 'No data copied between accounts')
d.group(624, 494, 552, 382, 'Consumer account')
d.column(624, 494, [('Read-only database', 'data'), ('Own virtual warehouse', 'coding')], first=80, h=76, gap=30)
d.notes(624, 494, 382, 'Roles control reader access')
d.group(24, 494, 552, 382, 'Provider data')
d.column(24, 494, [('Shared source objects', 'write')], first=100, h=82)
d.notes(24, 494, 382, 'Provider keeps the data')
d.arrow('M576 242H624', label='grants', at=(600, 224))
d.arrow('M900 410V494', label='share access', at=(900, 455))
d.arrow('M624 690H576', label='reads source', at=(600, 670))
d.save(Path(__file__).with_suffix('.svg'))
