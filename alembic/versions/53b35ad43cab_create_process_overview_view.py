"""Create process_overview view

Revision ID: 53b35ad43cab
Revises: 8cf12efb3775
Create Date: 2025-03-22 13:32:08.634219

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '53b35ad43cab'
down_revision: Union[str, None] = '8cf12efb3775'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    create view public.process_overview (process_id, graph_label, workstation_id, input_item_ids, output_item_id) as
SELECT p.id                                      AS process_id,
       graph.name                                AS graph_label,
       p.workstation_id,
       array_agg(pi.item_id ORDER BY pi.item_id) AS input_item_ids,
       po.item_id                                AS output_item_id
FROM process p
         LEFT JOIN process_input pi ON p.id = pi.process_id
         LEFT JOIN process_output po ON p.id = po.process_id
         LEFT JOIN material_graph graph ON p.graph_id = graph.id
GROUP BY p.id, graph.name, p.workstation_id, po.item_id;

alter table public.process_overview
    owner to postgres;


    """)

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("drop view public.process_overview;")
    pass
