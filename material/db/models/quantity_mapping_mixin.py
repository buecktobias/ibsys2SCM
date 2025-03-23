from typing import Optional

from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, declared_attr

from material.core.resource_counter import ItemCounter
from material.db.models.base import Base
from material.db.models.item import Item


class QuantityMappingMixin:
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(default=0)

    @declared_attr
    def item(self):
        return relationship(
            Item,
            lazy="joined"
        )

    @classmethod
    def load_as_counter(cls, session: Session, period: Optional[int] = None) -> ItemCounter:
        query = session.query(cls)
        query = cls.get_period_filter(query, period)
        rows = query.all()
        return ItemCounter({row.item: row.quantity for row in rows})

    @classmethod
    def get_period_filter(cls, query, period: int):
        return query
