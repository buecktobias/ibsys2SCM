"""Add unique constraint + index to process_input

Revision ID: 8cf12efb3775
Revises: 
Create Date: 2025-03-22 11:51:05.478237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8cf12efb3775'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'bought_item', 'item_id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False
        )
    op.alter_column(
        'bought_item', 'base_price',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
        )
    op.alter_column(
        'bought_item', 'discount_amount',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        nullable=False
        )
    op.alter_column(
        'bought_item', 'mean_order_duration',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
        )
    op.alter_column(
        'bought_item', 'order_std_dev',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
        )
    op.alter_column(
        'bought_item', 'base_order_cost',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
        )
    op.create_foreign_key(None, 'bought_item', 'item', ['item_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.alter_column(
        'item', 'id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True
        )
    op.alter_column(
        'material_graph', 'id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True
        )
    op.alter_column(
        'material_graph', 'name',
        existing_type=sa.TEXT(),
        type_=sa.String(),
        nullable=False
        )
    op.alter_column(
        'material_graph', 'parent_graph_id',
        existing_type=sa.TEXT(),
        type_=sa.Integer(),
        existing_nullable=True
        )
    op.create_foreign_key(
        None,
        'material_graph',
        'material_graph',
        ['parent_graph_id'],
        ['id'],
        onupdate='CASCADE',
        ondelete='SET NULL'
        )
    op.alter_column(
        'process', 'id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True
        )
    op.alter_column(
        'process', 'graph_id',
        existing_type=sa.TEXT(),
        type_=sa.Integer(),
        nullable=False
        )
    op.alter_column(
        'process', 'workstation_id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        nullable=False
        )
    op.alter_column(
        'process', 'process_duration_minutes',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        nullable=False
        )
    op.alter_column(
        'process', 'setup_duration_minutes',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        nullable=False
        )
    op.create_foreign_key(
        None,
        'process',
        'workstation',
        ['workstation_id'],
        ['id'],
        onupdate='CASCADE',
        ondelete='CASCADE'
        )
    op.create_foreign_key(
        None,
        'process',
        'material_graph',
        ['graph_id'],
        ['id'],
        onupdate='CASCADE',
        ondelete='CASCADE'
        )
    op.alter_column(
        'process_input', 'process_id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False
        )
    op.alter_column(
        'process_input', 'item_id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False
        )
    op.alter_column(
        'process_input', 'quantity',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        nullable=False
        )
    op.create_foreign_key(None, 'process_input', 'item', ['item_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(
        None,
        'process_input',
        'process',
        ['process_id'],
        ['id'],
        onupdate='CASCADE',
        ondelete='CASCADE'
        )
    op.alter_column(
        'process_output', 'process_id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False
        )
    op.alter_column(
        'process_output', 'item_id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False
        )
    op.create_foreign_key(None, 'process_output', 'item', ['item_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(
        None,
        'process_output',
        'process',
        ['process_id'],
        ['id'],
        onupdate='CASCADE',
        ondelete='CASCADE'
        )
    op.alter_column(
        'produced_item', 'item_id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False
        )
    op.create_foreign_key(None, 'produced_item', 'item', ['item_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.alter_column(
        'workstation', 'id',
        existing_type=sa.BIGINT(),
        type_=sa.Integer(),
        existing_nullable=False,
        autoincrement=True
        )
    op.alter_column(
        'workstation', 'labour_cost_1',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
        )
    op.alter_column(
        'workstation', 'labour_cost_2',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
        )
    op.alter_column(
        'workstation', 'labour_cost_3',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
        )
    op.alter_column(
        'workstation', 'labour_overtime_cost',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
        )
    op.alter_column(
        'workstation', 'variable_machine_cost',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
        )
    op.alter_column(
        'workstation', 'fixed_machine_cost',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'workstation', 'fixed_machine_cost',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
        )
    op.alter_column(
        'workstation', 'variable_machine_cost',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
        )
    op.alter_column(
        'workstation', 'labour_overtime_cost',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
        )
    op.alter_column(
        'workstation', 'labour_cost_3',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
        )
    op.alter_column(
        'workstation', 'labour_cost_2',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
        )
    op.alter_column(
        'workstation', 'labour_cost_1',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
        )
    op.alter_column(
        'workstation', 'id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True
        )
    op.drop_constraint(None, 'produced_item', type_='foreignkey')
    op.alter_column(
        'produced_item', 'item_id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False
        )
    op.drop_constraint(None, 'process_output', type_='foreignkey')
    op.drop_constraint(None, 'process_output', type_='foreignkey')
    op.alter_column(
        'process_output', 'item_id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False
        )
    op.alter_column(
        'process_output', 'process_id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False
        )
    op.drop_constraint(None, 'process_input', type_='foreignkey')
    op.drop_constraint(None, 'process_input', type_='foreignkey')
    op.alter_column(
        'process_input', 'quantity',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        nullable=True
        )
    op.alter_column(
        'process_input', 'item_id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False
        )
    op.alter_column(
        'process_input', 'process_id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False
        )
    op.drop_constraint(None, 'process', type_='foreignkey')
    op.drop_constraint(None, 'process', type_='foreignkey')
    op.alter_column(
        'process', 'setup_duration_minutes',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        nullable=True
        )
    op.alter_column(
        'process', 'process_duration_minutes',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        nullable=True
        )
    op.alter_column(
        'process', 'workstation_id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        nullable=True
        )
    op.alter_column(
        'process', 'graph_id',
        existing_type=sa.Integer(),
        type_=sa.TEXT(),
        nullable=True
        )
    op.alter_column(
        'process', 'id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True
        )
    op.drop_constraint(None, 'material_graph', type_='foreignkey')
    op.alter_column(
        'material_graph', 'parent_graph_id',
        existing_type=sa.Integer(),
        type_=sa.TEXT(),
        existing_nullable=True
        )
    op.alter_column(
        'material_graph', 'name',
        existing_type=sa.String(),
        type_=sa.TEXT(),
        nullable=True
        )
    op.alter_column(
        'material_graph', 'id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True
        )
    op.alter_column(
        'item', 'id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True
        )
    op.drop_constraint(None, 'bought_item', type_='foreignkey')
    op.alter_column(
        'bought_item', 'base_order_cost',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
        )
    op.alter_column(
        'bought_item', 'order_std_dev',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
        )
    op.alter_column(
        'bought_item', 'mean_order_duration',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
        )
    op.alter_column(
        'bought_item', 'discount_amount',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        nullable=True
        )
    op.alter_column(
        'bought_item', 'base_price',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
        )
    op.alter_column(
        'bought_item', 'item_id',
        existing_type=sa.Integer(),
        type_=sa.BIGINT(),
        existing_nullable=False
        )
    # ### end Alembic commands ###
