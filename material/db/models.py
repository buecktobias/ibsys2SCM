from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Workstation(SQLModel, table=True):
    """Represents a workstation where processes are executed."""
    workstation_id: int = Field(primary_key=True)
    labour_cost_1: float
    labour_cost_2: float
    labour_cost_3: float
    labour_overtime_cost: float
    variable_machine_cost: float
    fixed_machine_cost: float


class MaterialGraph(SQLModel, table=True):
    """Represents the overall Material Graph containing subgraphs and processes."""
    graph_id: str = Field(primary_key=True)
    name: Optional[str] = None
    parent_graph_id: Optional[str] = Field(default=None, foreign_key="materialgraph.graph_id")

    # Relationships
    subgraphs: List["MaterialGraph"] = Relationship(
        back_populates="parent_graph",
        sa_relationship_kwargs={"remote_side": "MaterialGraph.graph_id"}
    )
    parent_graph: Optional["MaterialGraph"] = Relationship(back_populates="subgraphs")
    processes: List["Process"] = Relationship(back_populates="graph")


class Process(SQLModel, table=True):
    """Represents a manufacturing process."""
    process_id: int = Field(primary_key=True)
    graph_id: str = Field(foreign_key="materialgraph.graph_id")
    workstation_id: int = Field(foreign_key="workstation.workstation_id")
    process_duration: int
    setup_duration: int

    # Relationships
    graph: Optional[MaterialGraph] = Relationship(back_populates="processes")
    inputs: List["ProcessInput"] = Relationship(back_populates="process")
    output: Optional["ProcessOutput"] = Relationship(back_populates="process",
                                                     sa_relationship_kwargs={"uselist": False})


class ProcessInput(SQLModel, table=True):
    """Links processes to their input items."""
    process_id: int = Field(foreign_key="process.process_id", primary_key=True)
    item_id: int = Field(foreign_key="item.item_id", primary_key=True)
    quantity: int

    # Relationships
    process: Optional[Process] = Relationship(back_populates="inputs")
    item: Optional["Item"] = Relationship()


class ProcessOutput(SQLModel, table=True):
    """Represents the single output of a process."""
    process_id: int = Field(foreign_key="process.process_id", primary_key=True)
    item_id: int = Field(foreign_key="produced_item.item_id", primary_key=True)

    # Relationships
    process: Optional[Process] = Relationship(back_populates="output")
    item: Optional["ProducedItem"] = Relationship()


class Item(SQLModel, table=True):
    """Base class for all items (bought or produced)."""
    item_id: int = Field(primary_key=True)


class BoughtItem(SQLModel, table=True):
    """Represents items that are purchased, not produced."""
    item_id: int = Field(foreign_key="item.item_id", primary_key=True)
    base_price: float
    discount: Optional[float] = None
    discount_percentage: Optional[int] = None
    mean_order_duration: Optional[float] = None
    order_std_dev: Optional[float] = None
    base_order_cost: Optional[float] = None


class ProducedItem(SQLModel, table=True):
    """Represents items that are produced through a process."""
    item_id: int = Field(foreign_key="item.item_id", primary_key=True)
    parent_item_id: Optional[int] = Field(default=None, foreign_key="produced_item.item_id")
    sell_price: Optional[float] = None
