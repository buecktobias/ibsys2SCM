from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from scs.core.db.models.item_models.item_orm import ItemORM


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
