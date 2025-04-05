from __future__ import annotations

from sqlalchemy.orm import Mapped

from scs.core.db.base import Base
from scs.core.db.mixins.id_mixin import IdMixin


class WorkstationORM(IdMixin, Base):
    __tablename__ = "workstation"
    labour_cost_1: Mapped[float]
    labour_cost_2: Mapped[float]
    labour_cost_3: Mapped[float]
    labour_overtime_cost: Mapped[float]
    variable_machine_cost: Mapped[float]
    fixed_machine_cost: Mapped[float]
