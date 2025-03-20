from typing import Optional
from sqlmodel import SQLModel, Field


class Workstation(SQLModel, table=True):
    """Represents a workstation where processes are executed."""
    __table_args__ = {"extend_existing": True}
    workstation_id: int = Field(primary_key=True)
    labour_cost_1: float
    labour_cost_2: float
    labour_cost_3: float
    labour_overtime_cost: float
    variable_machine_cost: float
    fixed_machine_cost: float


class Item(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}  # Allow redefinition

    """Base class for all items (bought or produced)."""
    item_id: int = Field(primary_key=True)


class BoughtItem(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}  # Allow redefinition

    """Represents items that are purchased, not produced."""
    item_id: int = Field(foreign_key="item.item_id", primary_key=True)
    base_price: float
    discount_amount: Optional[int] = None
    mean_order_duration: Optional[float] = None
    order_std_dev: Optional[float] = None
    base_order_cost: Optional[float] = None


class ProducedItem(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}  # Allow redefinition

    """Represents items that are produced through a process."""
    item_id: int = Field(foreign_key="item.item_id", primary_key=True)


class MaterialGraph(SQLModel, table=True):
    """Represents the overall Material Graph containing subgraphs and processes."""
    __table_args__ = {"extend_existing": True}  # Allow redefinition

    graph_id: int = Field(primary_key=True)
    name: Optional[str] = None
    parent_graph_id: Optional[str] = Field(default=None, foreign_key="materialgraph.graph_id")


class Process(SQLModel, table=True):
    """Represents a manufacturing process."""
    __table_args__ = {"extend_existing": True}  # Allow redefinition

    process_id: int = Field(primary_key=True)
    graph_id: str = Field(foreign_key="materialgraph.graph_id")
    workstation_id: int
    process_duration: int
    setup_duration: int


class ProcessInput(SQLModel, table=True):
    """Links processes to their input items."""
    __table_args__ = {"extend_existing": True}  # Allow redefinition

    process_id: int = Field(foreign_key="process.process_id", primary_key=True)
    item_id: int = Field(foreign_key="item.item_id", primary_key=True)
    quantity: int


class ProcessOutput(SQLModel, table=True):
    """Represents the single output of a process."""
    __table_args__ = {"extend_existing": True}  # Allow redefinition

    process_id: int = Field(foreign_key="process.process_id", primary_key=True)
    item_id: int = Field(foreign_key="item.item_id", primary_key=True)
