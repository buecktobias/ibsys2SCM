from typing import Optional

from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Workstation(Base):
    __tablename__ = "workstation"
    id: Mapped[int] = mapped_column(primary_key=True)
    labour_cost_1: Mapped[float]
    labour_cost_2: Mapped[float]
    labour_cost_3: Mapped[float]
    labour_overtime_cost: Mapped[float]
    variable_machine_cost: Mapped[float]
    fixed_machine_cost: Mapped[float]


class Item(Base):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(primary_key=True)

    bought: Mapped["BoughtItem"] = relationship("BoughtItem", back_populates="item", uselist=False)
    produced: Mapped["ProducedItem"] = relationship("ProducedItem", back_populates="item", uselist=False)

    def is_bought(self) -> bool:
        return self.bought is not None

    def is_produced(self) -> bool:
        return self.produced is not None


class BoughtItem(Base):
    __tablename__ = "bought_item"
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    base_price: Mapped[float]
    discount_amount: Mapped[int]
    mean_order_duration: Mapped[float]
    order_std_dev: Mapped[float]
    base_order_cost: Mapped[float]

    item: Mapped[Item] = relationship("Item", back_populates="bought", uselist=False)


class ProducedItem(Base):
    __tablename__ = "produced_item"
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )

    item: Mapped[Item] = relationship("Item", back_populates="produced", uselist=False)


class MaterialGraphORM(Base):
    __tablename__ = "material_graph"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_graph_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("material_graph.id", onupdate="CASCADE", ondelete="SET NULL")
    )
    parent_graph: Mapped["MaterialGraphORM"] = relationship(back_populates="subgraphs", remote_side=[id])
    subgraphs: Mapped[list["MaterialGraphORM"]] = relationship(back_populates="parent_graph")
    processes: Mapped[list["Process"]] = relationship(back_populates="graph")


class Process(Base):
    __tablename__ = "process"
    __table_args__ = (CheckConstraint("process_duration >= 0"), CheckConstraint("setup_duration >= 0"))
    id: Mapped[int] = mapped_column(primary_key=True)
    graph_id: Mapped[int] = mapped_column(
        ForeignKey("material_graph.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    workstation_id: Mapped[int] = mapped_column(
        ForeignKey("workstation.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    process_duration: Mapped[int]
    setup_duration: Mapped[int]
    graph: Mapped[MaterialGraphORM] = relationship(back_populates="processes")
    inputs: Mapped[list["ProcessInput"]] = relationship(back_populates="process")
    workstation: Mapped[Workstation] = relationship()
    output: Mapped["ProcessOutput"] = relationship(back_populates="process", uselist=False)


class ProcessInput(Base):
    __tablename__ = "process_input"
    __table_args__ = (CheckConstraint("quantity >= 1"),)
    process_id: Mapped[int] = mapped_column(
        ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(default=1)
    item: Mapped[Item] = relationship()
    process: Mapped[Process] = relationship(back_populates="inputs")


class ProcessOutput(Base):
    __tablename__ = "process_output"
    process_id: Mapped[int] = mapped_column(
        ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    item: Mapped[Item] = relationship()
    process: Mapped[Process] = relationship(back_populates="output")
