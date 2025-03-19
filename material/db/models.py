from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey


class Workstation(SQLModel, table=True):
    workstation_id: int = Field(primary_key=True)
    labour_cost_1: float
    labour_cost_2: float
    labour_cost_3: float
    labour_overtime_cost: float
    variable_machine_cost: float
    fixed_machine_cost: float


class Graph(SQLModel, table=True):
    graph_id: str = Field(primary_key=True)
    name: Optional[str] = None
    parent_graph_id: Optional[str] = Field(default=None, foreign_key="graph.graph_id")


class Process(SQLModel, table=True):
    process_id: int = Field(primary_key=True)
    graph_id: str = Field(ForeignKey("graph.graph_id"))
    workstation_id: int = Field(ForeignKey("workstation.workstation_id"))
    process_duration_in_mins: int
    setup_duration_in_mins: int


class ProcessInput(SQLModel, table=True):
    process_id: int = Field(ForeignKey("process.process_id"), primary_key=True)
    item_id: int = Field(ForeignKey("item.item_id"), primary_key=True)
    quantity: int


class ProcessOutput(SQLModel, table=True):
    process_id: int = Field(ForeignKey("process.process_id"), primary_key=True)
    item_id: int = Field(ForeignKey("item.item_id"), primary_key=True)


class Item(SQLModel, table=True):
    item_id: Optional[int] = Field(default=None, primary_key=True)
    type: str = Field(index=True)
    base_price: Optional[float] = None
    discount_amount: Optional[int] = None
    discount_percentage: Optional[float] = None
    mean_order_duration_in_periods: Optional[float] = None
    order_standard_deviation_in_periods: Optional[float] = None
    base_value_price: Optional[float] = None
    sell_price: Optional[float] = None
    parent_item_id: Optional[int] = None
