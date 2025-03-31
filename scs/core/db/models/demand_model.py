from __future__ import annotations

from scs.core.db.models.base import Base
from scs.core.db.models.mixins.periodic_quantity import PeriodicQuantityMixin


class DemandForecastItemORM(PeriodicQuantityMixin, Base):
    __tablename__ = "demand_forecast"
