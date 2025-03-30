from __future__ import annotations

import dataclasses
import datetime

from sqlalchemy import Integer, TypeDecorator


@dataclasses.dataclass(frozen=True)
class DomainSimTime:
    value: datetime.timedelta

    @property
    def period(self) -> int:
        return self.value.days // 5

    @property
    def day(self) -> int:
        return self.value.days % 5

    @property
    def hour(self) -> int:
        return self.value.seconds // 3600

    @property
    def minute(self) -> int:
        return (self.value.seconds // 60) % 60

    def total_seconds(self) -> int:
        return int(self.value.total_seconds())

    @staticmethod
    def from_string(value: str) -> DomainSimTime:
        period, day, hour, minute = map(int, value.split("-"))
        return DomainSimTime(
                value=datetime.timedelta(
                        days=day + period * 5,
                        hours=hour,
                        minutes=minute,
                )
        )

    @staticmethod
    def from_periods(period: int):
        return DomainSimTime(
                value=datetime.timedelta(
                        days=period * 5,
                )
        )

    def __str__(self):
        return f"{self.period}-{self.day}-{self.hour}-{self.minute}"


class SimTime(TypeDecorator):
    impl = Integer

    def process_bind_param(self, value: DomainSimTime | None, dialect) -> int | None:
        if isinstance(value, DomainSimTime):
            return int(value.total_seconds() // 60)

    def process_result_value(self, value: int, dialect) -> DomainSimTime | None:
        if value is not None:
            return DomainSimTime(datetime.timedelta(minutes=value))


class PeriodTime(TypeDecorator):
    impl = Integer

    def process_bind_param(self, value: DomainSimTime | None, dialect) -> int | None:
        if isinstance(value, DomainSimTime):
            return value.period

    def process_result_value(self, value: int | None, dialect) -> DomainSimTime | None:
        if value is not None:
            return DomainSimTime.from_periods(value)
