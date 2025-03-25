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
    __tablename__ = "_demand_forecast"


class Inventory(PeriodicQuantity, Base):
    __tablename__ = "inventory"


class BoughtItem(MappedAsDataclass, Item):
    __tablename__ = "bought_item"
    __mapper_args__ = {"polymorphic_identity": "bought_item"}

    id: Mapped[int] = mapped_column(ForeignKey("item.id", onupdate="CASCADE"), primary_key=True)
    type: Mapped[str] = mapped_column(String(50), default="bought_item", init=False)
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
    type: Mapped[str] = mapped_column(String(50), default="produced_item", init=False)

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
