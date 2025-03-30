from __future__ import annotations

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.base import Base
from scs.core.db.types import DomainSimTime, PeriodTime, SimTime


class WorkstationORM(Base):
    __tablename__ = "workstation"
    id: Mapped[int] = mapped_column(primary_key=True)
    labour_cost_1: Mapped[float]
    labour_cost_2: Mapped[float]
    labour_cost_3: Mapped[float]
    labour_overtime_cost: Mapped[float]
    variable_machine_cost: Mapped[float]
    fixed_machine_cost: Mapped[float]


class WSCapaORM(Base):
    __tablename__ = "ws_capa"
    id: Mapped[int] = mapped_column(primary_key=True)
    shifts: Mapped[int] = mapped_column(Integer)
    overtime: Mapped[SimTime] = mapped_column(Integer)
    workstation_id: Mapped[int] = mapped_column(ForeignKey("workstation.id"))

    workstation = relationship("Workstation", back_populates="capa")


class WSUseInfoORM(Base):
    __tablename__ = "ws_use_info"
    period: Mapped[DomainSimTime] = mapped_column(PeriodTime, primary_key=True)
    workstation_id: Mapped[int] = mapped_column(ForeignKey("workstation.id"), primary_key=True)
    setup_events: Mapped[int] = mapped_column(Integer)
    idletime: Mapped[DomainSimTime] = mapped_column(SimTime)
    time_needed: Mapped[DomainSimTime] = mapped_column(SimTime)
    workstation = relationship("Workstation", back_populates="use_info")
