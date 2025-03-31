import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

from scs.core.db.models.item_models import ItemORM


class QuantityMixin:
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(default=0)

    @declared_attr
    def item(self) -> Mapped[ItemORM]:
        return relationship(
                ItemORM,
                lazy="joined"
        )


class PeriodicQuantityMixin(QuantityMixin):
    period: Mapped[int] = mapped_column(primary_key=True)
