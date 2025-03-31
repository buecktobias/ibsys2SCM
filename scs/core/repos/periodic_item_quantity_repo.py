import collections
from collections import Counter
from typing import Optional

import sqlalchemy
from sqlalchemy import select, Select
from sqlalchemy.orm import Query, Session

from scs.core.db.models.mixins.periodic_quantity import PeriodicQuantityMixin
from scs.core.domain.item_models import ItemDomain
from scs.core.domain.periodic_item_quantities import PeriodicItemQuantity


class PeriodicItemQuantityRepo[T: PeriodicQuantityMixin]:
    def __init__(self, session: Session):
        self.session = session

    def _item_orm_to_domain(self, item_orm: T) -> ItemDomain:
        # Convert ORM object to domain object
        return ItemDomain(
                id=item_orm.id,
        )

    def load_as_counter(self, period: Optional[int] = None) -> Counter[ItemDomain]:
        query: Select[T] = select(T).filter_by(period=period)
        rows: collections.Iterable[T] = self.session.scalars(query).all()
        return Counter({row.item: row.quantity for row in rows})

    @classmethod
    def unique_periods(cls, session: sqlalchemy.orm.Session) -> list[int]:
        # Get all distinct periods
        return list(
                session.scalars(
                        session.query(cls.period)
                        .distinct()
                ).all()
        )

    @classmethod
    def get_periodic_item_quantity(cls, session: sqlalchemy.orm.Session) -> PeriodicItemQuantity:
        # Load all rows and convert them to a PeriodicItemQuantity
        return PeriodicItemQuantity(
                {
                        period: cls.load_as_counter(session, period)
                        for period in cls.unique_periods(session)
                }
        )
