from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from scs.db.models.base import Base
from scs.db.models.graph_node import GraphNode
from scs.db.models.item import Item
from scs.db.models.mixins.periodic_quantity import PeriodicQuantity
from scs.db.models.mixins.quantity_mapping_mixin import QuantityMappingMixin


class Workstation(Base):
    __tablename__ = "workstation"
    id: Mapped[int] = mapped_column(primary_key=True)
    labour_cost_1: Mapped[float]
    labour_cost_2: Mapped[float]
    labour_cost_3: Mapped[float]
    labour_overtime_cost: Mapped[float]
    variable_machine_cost: Mapped[float]
    fixed_machine_cost: Mapped[float]


class DemandForecast(PeriodicQuantity, Base):
    __tablename__ = "demand_forecast"


class Inventory(PeriodicQuantity, Base):
    __tablename__ = "inventory"


class BoughtItem(MappedAsDataclass, Item):
    __tablename__ = "bought_item"
    __mapper_args__ = {"polymorphic_identity": "bought_item"}

    id: Mapped[int] = mapped_column(ForeignKey("item.id", onupdate="CASCADE"), primary_key=True)
    base_price: Mapped[float]
    discount_amount: Mapped[int]
    mean_order_duration: Mapped[float]
    order_std_dev: Mapped[float]
    base_order_cost: Mapped[float]

    def __hash__(self):
        return hash(self.id)


class ProducedItem(MappedAsDataclass, Item):
    __tablename__ = "produced_item"
    __mapper_args__ = {"polymorphic_identity": "produced_item"}

    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)

    def __hash__(self):
        return hash(self.id)


class MaterialGraphORM(Base):
    __tablename__ = "material_graph"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_graph_id: Mapped[Optional[int]] = mapped_column(
            ForeignKey("material_graph.id", onupdate="CASCADE", ondelete="SET NULL")
    )
    parent_graph: Mapped["MaterialGraphORM"] = relationship(
            back_populates="subgraphs", remote_side=[id], lazy="joined"
    )
    subgraphs: Mapped[list["MaterialGraphORM"]] = relationship(back_populates="parent_graph", lazy="joined")
    processes: Mapped[list["Process"]] = relationship(back_populates="graph", lazy="joined")


class Process(GraphNode):
    __tablename__ = "process"
    __mapper_args__ = {"polymorphic_identity": "process"}
    __table_args__ = (CheckConstraint("process_duration >= 0"), CheckConstraint("setup_duration >= 0"))

    id: Mapped[int] = mapped_column(
            ForeignKey("graph_node.id", onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True
    )
    graph_id: Mapped[int] = mapped_column(
            ForeignKey("material_graph.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    workstation_id: Mapped[int] = mapped_column(
            ForeignKey("workstation.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    process_duration: Mapped[int]
    setup_duration: Mapped[int]

    graph: Mapped[MaterialGraphORM] = relationship(back_populates="processes", lazy="joined")
    inputs: Mapped[list["ProcessInput"]] = relationship(back_populates="process", lazy="joined")
    workstation: Mapped[Workstation] = relationship(lazy="joined")
    output: Mapped["ProcessOutput"] = relationship(back_populates="process", uselist=False, lazy="joined")


class ProcessInput(QuantityMappingMixin, Base):
    __tablename__ = "process_input"
    __table_args__ = (CheckConstraint("quantity >= 1"),)
    process_id: Mapped[int] = mapped_column(
            ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    process: Mapped[Process] = relationship(back_populates="inputs", lazy="joined")


class ProcessOutput(Base):
    __tablename__ = "process_output"
    process_id: Mapped[int] = mapped_column(
            ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
            ForeignKey("item.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )

    item: Mapped[Item] = relationship(lazy="joined")
    process: Mapped[Process] = relationship(back_populates="output", lazy="joined")


```python
from __future__ import annotations
import datetime
from sqlalchemy import Column, Integer, DateTime, Interval, Boolean, String, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class SimulationConfig(Base):
    __tablename__ = "simulation_config"
    id: Mapped[int] = mapped_column(primary_key=True)
    simulation_virtual_start: Mapped[datetime.datetime] = mapped_column(DateTime)

class TimePoint(Base):
    __tablename__ = "time_point"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[datetime.datetime] = mapped_column(DateTime)

    @property
    def in_total_minutes(self) -> int:
        return int(self.value.timestamp() / 60)

    def in_periods(self) -> int:
        return self.in_total_minutes

    def in_period_day_minute(self) -> dict:
        total = self.in_total_minutes
        day = total // (24 * 60)
        rem = total % (24 * 60)
        hour = rem // 60
        minute = rem % 60
        return {"period": day, "day": day, "hour": hour, "minute": minute}

class Duration(Base):
    __tablename__ = "duration"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[datetime.timedelta] = mapped_column(Interval)

    @property
    def in_total_minutes(self) -> int:
        return int(self.value.total_seconds() / 60)

    def in_periods(self) -> int:
        return self.in_total_minutes

    def in_period_day_minute(self) -> dict:
        total = self.in_total_minutes
        day = total // (24 * 60)
        rem = total % (24 * 60)
        hour = rem // 60
        minute = rem % 60
        return {"period": day, "day": day, "hour": hour, "minute": minute}

class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_kind: Mapped[str] = mapped_column(String(50))
    created_at_id: Mapped[int] = mapped_column(ForeignKey("time_point.id"))
    expected_execution_at_mean_id: Mapped[int] = mapped_column(ForeignKey("time_point.id"))
    expected_execution_at_stdv_id: Mapped[int] = mapped_column(ForeignKey("duration.id"))
    was_executed: Mapped[bool] = mapped_column(Boolean)
    offered_to_us: Mapped[bool] = mapped_column(Boolean)
    offered_by_us: Mapped[bool] = mapped_column(Boolean)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    amount_inv_change: Mapped[int] = mapped_column(Integer)
    cash_flow_per_item: Mapped[int] = mapped_column(Integer)
    penalty: Mapped[int] = mapped_column(Integer)
    creation_cost: Mapped[int] = mapped_column(Integer)

    created_at = relationship("TimePoint", foreign_keys=[created_at_id])
    expected_execution_at_mean = relationship("TimePoint", foreign_keys=[expected_execution_at_mean_id])
    expected_execution_at_stdv = relationship("Duration", foreign_keys=[expected_execution_at_stdv_id])
    item = relationship("Item")

    __mapper_args__ = {
        "polymorphic_on": order_kind,
        "polymorphic_identity": "order"
    }

class BuyOrder(Order):
    __abstract__ = True
    def __init__(self, **kwargs: any) -> None:
        kwargs.setdefault("offered_by_us", False)
        kwargs.setdefault("offered_to_us", True)
        super().__init__(**kwargs)

class SellOrder(Order):
    __abstract__ = True
    def __init__(self, **kwargs: any) -> None:
        kwargs.setdefault("offered_by_us", True)
        kwargs.setdefault("offered_to_us", False)
        super().__init__(**kwargs)

class NormalOrder(SellOrder):
    __tablename__ = "normal_order"
    id: Mapped[int] = mapped_column(ForeignKey("order.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "normal_order"}

class DirectOrder(SellOrder):
    __tablename__ = "direct_order"
    id: Mapped[int] = mapped_column(ForeignKey("order.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "direct_order"}

class MaterialOrder(BuyOrder):
    __tablename__ = "material_order"
    id: Mapped[int] = mapped_column(ForeignKey("order.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "material_order"}

class MarketPlaceBuy(BuyOrder):
    __tablename__ = "marketplace_buy"
    id: Mapped[int] = mapped_column(ForeignKey("order.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "marketplace_buy"}

class MarketPlaceSell(SellOrder):
    __tablename__ = "marketplace_sell"
    id: Mapped[int] = mapped_column(ForeignKey("order.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "marketplace_sell"}

class ItemProduction(Base):
    __tablename__ = "item_production"
    id: Mapped[int] = mapped_column(primary_key=True)
    producing_item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    est_finish_at_id: Mapped[int] = mapped_column(ForeignKey("time_point.id"))
    est_finish_stdv_id: Mapped[int] = mapped_column(ForeignKey("duration.id"))

    producing_item = relationship("Item")
    est_finish_at = relationship("TimePoint", foreign_keys=[est_finish_at_id])
    est_finish_stdv = relationship("Duration", foreign_keys=[est_finish_stdv_id])

class WSCapa(Base):
    __tablename__ = "ws_capa"
    id: Mapped[int] = mapped_column(primary_key=True)
    shifts: Mapped[int] = mapped_column(Integer)
    overtime: Mapped[int] = mapped_column(Integer)
    workstation_id: Mapped[int] = mapped_column(ForeignKey("workstation.id"))

    workstation = relationship("Workstation", back_populates="capa")

class WSUseInfo(Base):
    __tablename__ = "ws_use_info"
    id: Mapped[int] = mapped_column(primary_key=True)
    workstation_id: Mapped[int] = mapped_column(ForeignKey("workstation.id"))
    setup_events: Mapped[int] = mapped_column(Integer)
    idletime: Mapped[int] = mapped_column(Integer)
    time_needed: Mapped[int] = mapped_column(Integer)

    workstation = relationship("Workstation", back_populates="use_info")

class InputInventory(Base):
    __tablename__ = "input_inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    period_id: Mapped[int] = mapped_column(ForeignKey("time_point.id"))
    period = relationship("TimePoint")
    item_quantities: Mapped[dict] = mapped_column(JSON)
    item_values: Mapped[dict] = mapped_column(JSON)

class PTimeFormat:
    def __init__(self, period: int, day: int, hour: int, minute: int):
        self.period = period
        self.day = day
        self.hour = hour
        self.minute = minute

class TimePointBuilder:
    @staticmethod
    def from_minutes(minutes: int) -> TimePoint:
        dt = datetime.datetime.fromtimestamp(minutes * 60)
        return TimePoint(value=dt)
    @staticmethod
    def from_periods(periods: int) -> TimePoint:
        dt = datetime.datetime.fromtimestamp(periods * 60)
        return TimePoint(value=dt)

class TimeDurationBuilder:
    @staticmethod
    def from_minutes(minutes: int) -> Duration:
        td = datetime.timedelta(minutes=minutes)
        return Duration(value=td)
    @staticmethod
    def from_periods(periods: int) -> Duration:
        td = datetime.timedelta(minutes=periods)
        return Duration(value=td)