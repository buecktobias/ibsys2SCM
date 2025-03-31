"""changed order models!

Revision ID: c5ee9a4a4401
Revises: 4badac6dd55e
Create Date: 2025-03-30 15:43:35.951861

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from scs.core.db.types import PeriodTime, SimTime

# revision identifiers, used by Alembic.
revision: str = 'c5ee9a4a4401'
down_revision: Union[str, None] = '4badac6dd55e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
            'inventory_result',
            sa.Column('period', PeriodTime(), nullable=False),
            sa.Column('item_id', sa.Integer(), nullable=False),
            sa.Column('quantity', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
            sa.PrimaryKeyConstraint('period', 'item_id')
    )
    op.drop_table('inventory')
    op.add_column('direct_order', sa.Column('penalty', sa.Float(), nullable=False))
    op.add_column('material_order', sa.Column('order_type', sa.String(length=50), nullable=False))
    op.add_column('order', sa.Column('created_at_period', PeriodTime(), nullable=False))
    op.add_column('order', sa.Column('quantity', sa.Integer(), nullable=False))
    op.drop_column('order', 'amount_inv_change')
    op.drop_column('order', 'created_at_id')
    op.drop_column('order', 'creation_cost')
    op.drop_column('order', 'offered_by_us')
    op.drop_column('order', 'offered_to_us')
    op.drop_column('order', 'penalty')
    op.add_column('ws_use_info', sa.Column('period', PeriodTime(), nullable=False))
    op.drop_column('ws_use_info', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ws_use_info', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('ws_use_info', 'period')
    op.add_column(
            'simulation_config',
            sa.Column('simulation_virtual_start', postgresql.TIMESTAMP(), autoincrement=False, nullable=False)
    )
    op.drop_column('simulation_config', 'current_sim_time')
    op.add_column(
            'order',
            sa.Column('expected_execution_at_mean_id', sa.INTEGER(), autoincrement=False, nullable=False)
    )
    op.add_column('order', sa.Column('penalty', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('order', sa.Column('offered_to_us', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column(
            'order',
            sa.Column('expected_execution_at_stdv_id', sa.INTEGER(), autoincrement=False, nullable=False)
    )
    op.add_column('order', sa.Column('offered_by_us', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('order', sa.Column('creation_cost', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('order', sa.Column('created_at_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('order', sa.Column('amount_inv_change', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key(
            'order_expected_execution_at_stdv_id_fkey',
            'order',
            'duration',
            ['expected_execution_at_stdv_id'],
            ['id']
    )
    op.create_foreign_key('order_created_at_id_fkey', 'order', 'time_point', ['created_at_id'], ['id'])
    op.create_foreign_key(
            'order_expected_execution_at_mean_id_fkey',
            'order',
            'time_point',
            ['expected_execution_at_mean_id'],
            ['id']
    )
    op.drop_column('order', 'quantity')
    op.drop_column('order', 'created_at_period')
    op.drop_column('material_order', 'order_type')
    op.add_column('item_production', sa.Column('est_finish_at_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('item_production', sa.Column('est_finish_stdv_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key(
            'item_production_est_finish_at_id_fkey',
            'item_production',
            'time_point',
            ['est_finish_at_id'],
            ['id']
    )
    op.create_foreign_key(
            'item_production_est_finish_stdv_id_fkey',
            'item_production',
            'duration',
            ['est_finish_stdv_id'],
            ['id']
    )
    op.drop_column('direct_order', 'penalty')
    op.create_table(
            'marketplace_buy',
            sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
            sa.ForeignKeyConstraint(['id'], ['order.id'], name='marketplace_buy_id_fkey'),
            sa.PrimaryKeyConstraint('id', name='marketplace_buy_pkey')
    )
    op.create_table(
            'test',
            sa.Column('datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
            sa.Column('datetime2', postgresql.TIME(), autoincrement=False, nullable=True),
            sa.Column('intervaltest', postgresql.INTERVAL(), autoincrement=False, nullable=True)
    )
    op.create_table(
            'time_point',
            sa.Column(
                    'id',
                    sa.INTEGER(),
                    server_default=sa.text("nextval('time_point_id_seq'::regclass)"),
                    autoincrement=True,
                    nullable=False
            ),
            sa.Column('value', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
            sa.PrimaryKeyConstraint('id', name='time_point_pkey'),
            postgresql_ignore_search_path=False
    )
    op.create_table(
            'marketplace_sell',
            sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
            sa.ForeignKeyConstraint(['id'], ['order.id'], name='marketplace_sell_id_fkey'),
            sa.PrimaryKeyConstraint('id', name='marketplace_sell_pkey')
    )
    op.create_table(
            'input_inventory',
            sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
            sa.Column('period_id', sa.INTEGER(), autoincrement=False, nullable=False),
            sa.Column('item_quantities', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
            sa.Column('item_values', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
            sa.ForeignKeyConstraint(['period_id'], ['time_point.id'], name='input_inventory_period_id_fkey'),
            sa.PrimaryKeyConstraint('id', name='input_inventory_pkey')
    )
    op.create_table(
            'inventory',
            sa.Column('period', sa.INTEGER(), autoincrement=False, nullable=False),
            sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=False),
            sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
            sa.ForeignKeyConstraint(['item_id'], ['item.id'], name='inventory_item_id_fkey'),
            sa.PrimaryKeyConstraint('period', 'item_id', name='inventory_pkey')
    )
    op.create_table(
            'duration',
            sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
            sa.Column('value', postgresql.INTERVAL(), autoincrement=False, nullable=False),
            sa.PrimaryKeyConstraint('id', name='duration_pkey')
    )
    op.drop_table('inventory_result')
    # ### end Alembic commands ###
