import abc
from dataclasses import dataclass

from material.graph.nodes.mermaid_node import LabeledGraphNode
from material.graph.nodes.production_node_type import ProductionNodeType


@dataclass()
class Item(LabeledGraphNode, abc.ABC):
    node_numerical_id: int

    @property
    @abc.abstractmethod
    def node_type(self):
        pass

    @property
    def label(self):
        return (
            f"{self.node_type.value}{self.node_numerical_id}"
        )

    def __hash__(self):
        return hash((self.node_type, self.node_numerical_id))

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.node_numerical_id == other.node_numerical_id and self.node_type == other.node_type


@dataclass()
class Bought(Item):
    """
        base_price=item.base_price, discount_amount=item.discount_amount,
        discount_percentage=item.discount_percentage,
        mean_order_duration_in_periodes=item.mean_order_duration,
        mean_order_standard_deviation_in_periodes=item.mean_order_std_dev
    """
    base_price: float = 0
    discount_amount: int = 0
    discount_percentage: float = 0
    mean_order_duration: float = 0
    mean_order_std_dev: float = 0

    @property
    def node_type(self) -> ProductionNodeType:
        return ProductionNodeType.BOUGHT

    def __hash__(self):
        return hash((self.node_type, self.node_numerical_id))

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.node_numerical_id == other.node_numerical_id and self.node_type == other.node_type


class Produced(Item, abc.ABC):
    def __init__(self, node_numerical_id: int):
        super().__init__(node_numerical_id)

    @property
    def node_type(self) -> ProductionNodeType:
        return ProductionNodeType.PRODUCED

    @property
    def is_primary(self) -> bool:
        return self.node_numerical_id <= 3

    def __hash__(self):
        return hash((self.node_type, self.node_numerical_id))

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.node_numerical_id == other.node_numerical_id and self.node_type == other.node_type


@dataclass
class FullProduced(Produced):
    base_value_price: float = 0

    def __hash__(self):
        return hash((self.node_type, self.node_numerical_id))

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.node_numerical_id == other.node_numerical_id and self.node_type == other.node_type


class StepProduced(Produced):
    def __init__(self, parent_produced: FullProduced, step_number: int):
        super().__init__(parent_produced.node_numerical_id)
        self.parent_produced: FullProduced = parent_produced
        self.step_number = step_number
        self.produced_by_workstation: int | None = None

    @property
    def unique_item_id(self) -> int:
        if not self.produced_by_workstation:
            raise ValueError("Workstation ID not set")
        return self.produced_by_workstation * 10 ** 4 + self.parent_produced.node_numerical_id

    @property
    def label(self) -> str:
        return f"{self.parent_produced.label}_{self.step_number}"

    @property
    def node_type(self) -> ProductionNodeType:
        return ProductionNodeType.PRODUCED

    def __repr__(self):
        return f"{self.label}"

    def __hash__(self):
        return hash((self.parent_produced, self.step_number))

    def __eq__(self, other):
        if not isinstance(other, StepProduced):
            return False
        return self.parent_produced == other.parent_produced and self.step_number == other.step_number
