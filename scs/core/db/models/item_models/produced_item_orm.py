from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from scs.core.db.models.item_models.item_orm import ItemORM


class ProducedItemORM(MappedAsDataclass, ItemORM):
    """
    Represents a produced item within the database.

    This class is a mapped dataclass that extends the functionality of the
    ItemORM to represent a specific type of item, identified as a
    produced item. Used in the database schema with polymorphic identity.

    Attributes:
        __tablename__ (str): Name of the table in the database for
            produced items.
        __mapper_args__ (dict): Mapping arguments defining the polymorphic
            identity for this class.
        id (Mapped[int]): Primary key of the produced item, with a foreign
            key reference to the ItemORM base class.
    """
    __tablename__ = "produced_item"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    id: Mapped[int] = mapped_column(ForeignKey(ItemORM.id), primary_key=True)

    def __hash__(self):
        return hash(self.id)
