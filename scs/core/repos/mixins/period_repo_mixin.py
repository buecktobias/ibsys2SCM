import abc
import collections
import typing
from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from scs.core.db.models.mixins.periodic_quantity import PeriodMixin


class PeriodRepoMixin[T: PeriodMixin](abc.ABC):
    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_period(self, period: int) -> collections.Iterable[T]:
        return self.session.execute(
                select(T).filter_by(period=period)
        ).scalars().all()

    def unique_periods(self) -> Iterable[int]:
        all_ts: Iterable[T] = self.session.execute(select(T)).scalars().all()
        return {typing.cast(int, row.period) for row in all_ts}
