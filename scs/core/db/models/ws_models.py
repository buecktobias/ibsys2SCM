from __future__ import annotations

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.base import Base, IdMixin
from scs.core.db.types import DomainSimTime, PeriodTime, SimTime


class WorkstationORM(IdMixin, Base):
    __tablename__ = "workstation"
    labour_cost_1: Mapped[float]
    labour_cost_2: Mapped[float]
    labour_cost_3: Mapped[float]
    labour_overtime_cost: Mapped[float]
    variable_machine_cost: Mapped[float]
    fixed_machine_cost: Mapped[float]
