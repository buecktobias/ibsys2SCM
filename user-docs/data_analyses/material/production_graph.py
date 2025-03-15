from typing import Literal

import networkx as nx
from dataclasses import dataclass
from enum import Enum

class Type(Enum):
    BOUGHT = "K"
    PRODUCED = "E"
    FINAL_PRODUCT = "P"
    PROCESS = "PR"

@dataclass
class Node:
    node_uid: str

@dataclass
class Item(Node):
    node_type: Type
    node_id : int
    def __init__(self, node_id, node_type):
        self.node_id = node_id
        self.node_type = node_type

    @property
    def node_uid(self):
        return self.node_type.value + str(self.node_id)

@dataclass
class Process(Node):
    process_group: Literal["A", "B", "C", "D", "E", "F", "G", "H", "w", "x", "y", "z"]
    workstation_id: int
    process_duration: int
    setup_duration: int
    def __init__(self, workstation_id, process_group, process_duration, setup_duration):
        self.workstation_id = workstation_id
        self.process_group = process_group
        self.process_duration = process_duration
        self.setup_duration = setup_duration

    @property
    def node_uid(self):
        return f"{self.workstation_id}.{self.process_group}"


class MaterialProductionFlowGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_process(self, id, pd, sd):
        self.graph.add_node(id, type=Type.PROCESS, process_duration=pd, setup_duration=sd)

    def add_bought(self, item_id):
        self.graph.add_node(item_id, type=Type.BOUGHT)

    def add_produced(self, item_id):
        self.graph.add_node(item_id, type=Type.PRODUCED)

    def add_item(self, item_id):
        if "." in item_id:
            raise ValueError(f"Item id cannot contain dots!: {item_id}")
        if "K" in item_id:
            self.add_bought(item_id)
        elif "E" in item_id:
            self.add_produced(item_id)
        else:
            raise ValueError(f"Only bought K and produced E is allowed!: {item_id}")

    def add_edge(self, source_id, target_id, weight):
        if source_id not in self.graph.nodes:
            self.add_item(source_id)
        if target_id not in self.graph.nodes:
            self.add_item(target_id)
        self.graph.add_edge(source_id, target_id, weight=weight)

    def get_graphs_nodes(self):
        nodes = []
        for node, attr in self.graph.nodes(data=True):
            node_type = attr.get("type")
            if node_type == Type.PROCESS.value:
                workstation_id, process_group = node.split(".")
                nodes.append(Process(workstation_id, process_group, attr.get("process_duration"), attr.get("setup_duration")))
            else:
                nodes.append(Item(node, node_type))
        return nodes
