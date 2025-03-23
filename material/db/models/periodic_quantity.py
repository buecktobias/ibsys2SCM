import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

from material.db.models.periodic_item_quantity import PeriodicItemQuantity
from material.db.models.quantity_mapping_mixin import QuantityMappingMixin


class PeriodicQuantity(QuantityMappingMixin):
    period: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    def get_period_filter(cls, query, period: int):
        return query.filter_by(period=period)

    @classmethod
    def unique_periods(cls, session: sqlalchemy.orm.Session) -> list[int]:
        # Get all distinct periods
        return list(session.scalars(
            session.query(cls.period)
            .distinct()
        ).all())

    @classmethod
    def get_periodic_item_quantity(cls, session: sqlalchemy.orm.Session) -> PeriodicItemQuantity:
        # Load all rows and convert them to a PeriodicItemQuantity
        return PeriodicItemQuantity({
            period: cls.load_as_counter(session, period)
            for period in cls.unique_periods(session)
        })
