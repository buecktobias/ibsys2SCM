from __future__ import annotations

import logging

from sqlalchemy import ForeignKey, ForeignKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from scs.core.db.models.graph_models import GraphNode


class Item(GraphNode):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(
            primary_key=True
    )
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
            "polymorphic_identity": "item",
    }
    # Here's where the foreign key reference is declared
    __table_args__ = (
            ForeignKeyConstraint(
                    ["id"], ["graph_node.id"],
            ),
    )

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __repr__(self):
        logging.warning(f"Item {self.id} is neither bought nor produced")
        return f"Item({self.id})"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class BoughtItemORM(MappedAsDataclass, Item):
    __tablename__ = "bought_item"
    __mapper_args__ = {"polymorphic_identity": "bought_item"}

    id: Mapped[int] = mapped_column(ForeignKey("item.id", onupdate="CASCADE"), primary_key=True)
    base_price: Mapped[float]
    discount_amount: Mapped[int]
    mean_order_duration: Mapped[float]
    order_std_dev: Mapped[float]
    base_order_cost: Mapped[float]

    def __hash__(self):
        return hash(self.id)


class ProducedItemORM(MappedAsDataclass, Item):
    __tablename__ = "produced_item"
    __mapper_args__ = {"polymorphic_identity": "produced_item"}

    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)

    def __hash__(self):
        return hash(self.id)
