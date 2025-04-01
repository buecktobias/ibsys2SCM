from __future__ import annotations

from sqlalchemy import ForeignKey, ForeignKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from scs.core.db.models.graph.graph_node import GraphNodeORM


class ItemORM(GraphNodeORM):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(
            primary_key=True
    )
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
            "polymorphic_identity": __tablename__,
    }
    # Here's where the foreign key reference is declared
    __table_args__ = (
            ForeignKeyConstraint(
                    [id], [GraphNodeORM.id],
            ),
    )


class BoughtItemORM(MappedAsDataclass, ItemORM):
    __tablename__ = "bought_item"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    id: Mapped[int] = mapped_column(ForeignKey(ItemORM.id, onupdate="CASCADE"), primary_key=True)
    base_price: Mapped[float]
    discount_amount: Mapped[int]
    mean_order_duration: Mapped[float]
    order_std_dev: Mapped[float]
    base_order_cost: Mapped[float]

    def __hash__(self):
        return hash(self.id)


class ProducedItemORM(MappedAsDataclass, ItemORM):
    __tablename__ = "produced_item"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    id: Mapped[int] = mapped_column(ForeignKey(ItemORM.id), primary_key=True)

    def __hash__(self):
        return hash(self.id)
