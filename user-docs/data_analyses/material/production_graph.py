import networkx as nx
from dataclasses import dataclass
from enum import Enum

class Type(Enum):
    BOUGHT = "bought"
    PRODUCED = "produced"
    PROCESS = "process"

@dataclass
class Node:
    id: str
    node_type: str

    @property
    def is_produced(self):
        return self.node_type == Type.PRODUCED.value

@dataclass
class Process(Node):
    process_duration: int
    setup_duration: int

    @property
    def group(self):
        return self.id.split(".")[1]

    @property
    def workstation(self):
        return self.id.split(".")[0]

class MaterialProductionFlowGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_process(self, id, pd, sd):
        self.graph.add_node(id, type=Type.PROCESS.value, process_duration=pd, setup_duration=sd)

    def add_bought(self, item_id):
        self.graph.add_node(item_id, type=Type.BOUGHT.value)

    def add_produced(self, item_id):
        self.graph.add_node(item_id, type=Type.PRODUCED.value)

    def add_item(self, item_id):
        if "." in item_id:
            raise ValueError(f"Item id cannot contain dots!: {item_id}")
        if "K" in item_id:
            self.add_bought(item_id)
        elif "E" in item_id:
            self.add_produced(item_id)
        elif 'P' in item_id:
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
                nodes.append(Process(node, node_type, attr.get("process_duration"), attr.get("setup_duration")))
            else:
                nodes.append(Node(node, node_type))
        return nodes
