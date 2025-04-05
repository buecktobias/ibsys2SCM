from sqlalchemy.orm import Session

from scs.core.db.periodic.demand_forecast_item_orm import DemandForecastItemORM
from scs.core.repos.mixins.period_qty_mixin import PeriodQtyMixin


class DemandForecastRepository(PeriodQtyMixin[DemandForecastItemORM]):
    def __init__(self, session: Session):
        self.session = session

    def get_forecast_starting_with(self, first_period: int):
        return (
                DemandForecastItemORM
                .get_periodic_item_quantity(self.session)
                .cut_off_periods_lower_than(first_period)
                .with_starting_period()
        )
