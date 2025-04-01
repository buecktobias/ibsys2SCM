from __future__ import annotations

from scs.core.db.models.base import Base
from scs.core.db.models.mixins.periodic_quantity import PeriodMixin


class InventoryItemORM(PeriodMixin, Base):
    __tablename__ = "inventory"
