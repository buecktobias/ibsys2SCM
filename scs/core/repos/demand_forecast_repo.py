from sqlalchemy.orm import Session

from scs.core.db.models.demand_model import DemandForecastItemORM


class DemandForecastRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_forecast_starting_with(self, first_period: int):
        return (
                DemandForecastItemORM
                .get_periodic_item_quantity(self.session)
                .cut_off_periods_lower_than(first_period)
                .with_starting_period()
        )
