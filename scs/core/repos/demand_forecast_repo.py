from sqlalchemy import select
from sqlalchemy.orm import Session

from scs.core.db.models.demand_model import DemandForecastItemORM


class DemandForecastRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_forecast_for(self, period: int, item_id: int) -> float:
        """
        Get the forecasted demand for a specific period and item.
        :param period: The period for which to get the forecast.
        :param item_id: The ID of the item for which to get the forecast.
        :return: The forecasted demand.
        """
        forecast = self.session.scalar(
                select(DemandForecastItemORM).where(DemandForecastItemORM.period == period)
        ).get_periodic_item_quantity()

        if forecast:
            return forecast.quantity
        else:
            return 0.0
