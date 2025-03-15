from dataclasses import dataclass
from enum import Enum

import networkx


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


def get_graphs_nodes(graph: networkx.Graph):
    nodes: list[Node] = []
    for node, attr in graph.nodes(data=True):
        node_type: str = attr.get("type")
        if node_type == Type.PROCESS.value:
            nodes.append(Process(node, node_type, attr.get("process_duration"), attr.get("setup_duration")))
        else:
            nodes.append(Node(node, node_type))
    return nodes


def add_process(g, id, pd, sd):
    g.add_node(id, type=Type.PROCESS.value, process_duration=pd, setup_duration=sd)

def add_bought(graph, item_id):
    graph.add_node(item_id, type="bought")

def add_produced(graph, item_id):
    graph.add_node(item_id, type="produced")

def add_item(graph, item_id):
    if "." in item_id:
        raise ValueError(f"Item id cannot contain dots!: {item_id}")
    if "K" in item_id:
        add_bought(graph, item_id)
    elif "E" in item_id:
        add_produced(graph, item_id)
    else:
        raise ValueError(f"Only bought K and produced E is allowed!: {item_id}")

def add_edge(graph, source_id, target_id, weight):
    if source_id not in graph.nodes:
        add_item(graph, source_id)

    if target_id not in graph.nodes:
        add_item(graph, target_id)

    graph.add_edge(source_id, target_id, weight=weight)