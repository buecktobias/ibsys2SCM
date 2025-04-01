from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from scs.core.db.models.item_models.item_orm import ItemORM


class ProducedItemORM(MappedAsDataclass, ItemORM):
    __tablename__ = "produced_item"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    id: Mapped[int] = mapped_column(ForeignKey(ItemORM.id), primary_key=True)

    def __hash__(self):
        return hash(self.id)
