from __future__ import annotations

from scs.core.db.base import Base
from scs.core.db.mixins.period_mixin import PeriodMixin


class InventoryItemORM(PeriodMixin, Base):
    """
    Represents an Inventory Item ORM (Object-Relational Mapping) model.

    Attributes:
        __tablename__ (str): The name of the database table associated with this model.
    """
    __tablename__ = "inventory"
