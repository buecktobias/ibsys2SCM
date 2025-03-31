from __future__ import annotations

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.models.base import Base
from scs.core.db.models.mixins.periodic_quantity import PeriodicQuantityMixin
from scs.core.db.types import DomainSimTime, PeriodTime


class InventoryItemORM(PeriodicQuantityMixin, Base):
    __tablename__ = "inventory"
