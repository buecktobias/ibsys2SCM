from typing import Optional

from sqlalchemy import ForeignKey
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


class BoughtItem(Base):
    __tablename__ = "bought_item"
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    base_price: Mapped[float]
    discount_amount: Mapped[int]
    mean_order_duration: Mapped[float]
    order_std_dev: Mapped[float]
    base_order_cost: Mapped[float]


class ProducedItem(Base):
    __tablename__ = "produced_item"
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)


class MaterialGraph(Base):
    __tablename__ = "material_graph"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_graph_id: Mapped[int | None] = mapped_column(ForeignKey("material_graph.id"))

    parent_graph: Mapped["MaterialGraph"] = relationship(back_populates="subgraphs", remote_side=[id])
    subgraphs: Mapped[list["MaterialGraph"]] = relationship(back_populates="parent_graph")

    processes: Mapped[list["Process"]] = relationship(back_populates="graph")


class Process(Base):
    __tablename__ = "process"

    id: Mapped[int] = mapped_column(primary_key=True)
    graph_id: Mapped[int] = mapped_column(ForeignKey("material_graph.id"))
    workstation_id: Mapped[int] = mapped_column(ForeignKey("workstation.id"))
    process_duration: Mapped[int]
    setup_duration: Mapped[int]

    graph: Mapped[MaterialGraph] = relationship(back_populates="processes")
    inputs: Mapped[list["ProcessInput"]] = relationship(back_populates="process")
    output: Mapped["ProcessOutput"] = relationship(back_populates="process", uselist=False)


class ProcessInput(Base):
    __tablename__ = "process_input"

    process_id: Mapped[int] = mapped_column(ForeignKey("process.id"), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    quantity: Mapped[int]
    item: Mapped[Item] = relationship()

    process: Mapped[Process] = relationship(back_populates="inputs")


class ProcessOutput(Base):
    __tablename__ = "process_output"
    process_id: Mapped[int] = mapped_column(ForeignKey("process.id"), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    item: Mapped[Item] = relationship()

    process: Mapped[Process] = relationship(back_populates="output")
