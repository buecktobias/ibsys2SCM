import abc
from dataclasses import dataclass

from material.graph.production_node_type import ProductionNodeType


@dataclass(frozen=True)
class Node(abc.ABC):
    @property
    @abc.abstractmethod
    def node_type(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def node_uid(self):
        raise NotImplementedError


@dataclass(frozen=True)
class Item(Node):
    node_id: int
    _node_type: ProductionNodeType

    @property
    def node_type(self):
        return self._node_type

    @property
    def node_uid(self):
        return str(self.node_id)

    @staticmethod
    def from_node_id(node_id):
        if node_id[0] not in ["K", "E"]:
            raise ValueError(f"Node id must start with K or E: {node_id}")
        numerical_id = int(node_id[1:])
        return Item(numerical_id, ProductionNodeType.PRODUCED if "E" in node_id else ProductionNodeType.BOUGHT)


@dataclass(frozen=True)
class StepItem(Item):
    step_number: int

    @property
    def node_uid(self):
        return f"{self.node_id}_{self.step_number}"


@dataclass(frozen=True)
class Process(Node):
    workstation_id: int
    process_duration: int
    setup_duration: int
    inputs: dict[Item, int] = None
    output: Item = None

    @property
    def node_type(self):
        return ProductionNodeType.PROCESS

    @property
    def node_uid(self):
        input_str = "_".join([
            f"{material}_{quantity}" for material, quantity in sorted(self.inputs.items(), key=lambda x: x[0].node_id)
        ])
        return f"{self.workstation_id}_{self.setup_duration}_{self.process_duration}_{input_str}__{self.output.node_id}"
