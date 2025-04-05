from __future__ import annotations

from scs.core.db.base import Base
from scs.core.db.mixins.period_mixin import PeriodMixin
from scs.core.db.mixins.quantity_mixin import QuantityMixin


class DemandForecastItemORM(PeriodMixin, QuantityMixin, Base):
    """
    Represents the ORM model for the demand forecast.

    This class maps to the 'demand_forecast' table in the database and extends the
    functionality provided by PeriodMixin, QuantityMixin, and Base classes. It is
    used for storing and managing demand forecast data along with associated period
    information and quantity details.

    Attributes:
        __tablename__ (str): Name of the table in the database represented by this
            ORM model, which is "demand_forecast".
    """
    __tablename__ = "demand_forecast"
