"""Add polymorphic item and process models

Revision ID: 25dffe600017
Revises: 53b35ad43cab
Create Date: 2025-03-25 00:49:43.821959

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '25dffe600017'
down_revision: Union[str, None] = '53b35ad43cab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply inheritance modifications."""

    # Step 1: Add `graph_node` base table (if not exists)
    op.create_table(
            "graph_node",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("type", sa.String(50), nullable=False),  # Polymorphic discriminator
    )

    # Step 2: Alter `item` to inherit from `graph_node`
    op.add_column("item", sa.Column("type", sa.String(50)))  # For polymorphism

    op.alter_column("bought_item", "item_id", new_column_name="id")

    op.alter_column("produced_item", "item_id", new_column_name="id")

    # Step 6: Assign polymorphic identities in item and in graph_node table
    op.execute(
            """
                UPDATE item SET type = 'produced_item' WHERE id IN (SELECT id FROM produced_item);
                UPDATE item SET type = 'bought_item' WHERE id IN (SELECT id FROM bought_item);
                """
    )

    # Add all ids to graph_node
    op.execute(
            """
                    INSERT INTO graph_node (id, type)
                    SELECT id, type FROM item;
                """
    )

    op.execute(
            """
                    INSERT INTO graph_node (id, type)
                    SELECT id, 'process' FROM process;
                    """
    )

    # Step 7: Set up polymorphic constraints
    op.alter_column("item", "type", existing_type=sa.String(50), nullable=False)

    # Step 8: Set foreign key constraints (cascading behavior)
    op.create_foreign_key("fk_bought_item_item", "bought_item", "item", ["id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("fk_produced_item_item", "produced_item", "item", ["id"], ["id"], ondelete="CASCADE")

    op.create_foreign_key("fk_item_graph_node", "item", "graph_node", ["id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("fk_item_graph_node", "process", "graph_node", ["id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    """Revert changes."""

    # Step 1: Drop foreign keys
    op.drop_constraint("fk_bought_item_item", "bought_item", type_="foreignkey")
    op.drop_constraint("fk_produced_item_item", "produced_item", type_="foreignkey")

    # Step 2: Remove `type` columns
    op.drop_column("item", "type")
    op.drop_column("process", "type")

    # Step 3: Remove `graph_node` inheritance
    op.drop_column("item", "id")
    op.drop_column("process", "id")

    # Step 4: Drop `graph_node` table (if empty)
    op.execute("DELETE FROM graph_node WHERE id NOT IN (SELECT id FROM item UNION SELECT id FROM process);")
    op.drop_table("graph_node")

    # Step 5: Revert `bought_item` and `produced_item`
    op.drop_column("bought_item", "item_id")
    op.drop_column("produced_item", "item_id")
