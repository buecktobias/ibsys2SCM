from sqlalchemy import select
from sqlalchemy.orm import Session

from scs.core.db.models.item_models import BoughtItemORM
from scs.core.domain.entities import BoughtItemDomain


class BoughtItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> BoughtItemDomain:
        bi: BoughtItemORM = self.session.scalars(
                select(BoughtItemORM).filter(BoughtItemORM.id == id)
        ).one()
        return BoughtItemDomain(
                id=bi.id,
                base_price=bi.base_price,
                discount_amount=bi.discount_amount,
                mean_order_duration=bi.mean_order_duration,
                order_std_dev=bi.order_std_dev,
                base_order_cost=bi.base_order_cost
        )
