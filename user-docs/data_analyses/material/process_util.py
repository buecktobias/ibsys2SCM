from dataclasses import dataclass
from enum import Enum


class Type(Enum):
    BOUGHT = "bought"
    PRODUCED = "produced"
    PROCESS = "process"


@dataclass
class Node:
    id: str

@dataclass
class Process(Node):
    id: str
    process_duration: int
    setup_duration: int

    @property
    def group(self):
        return self.id.split(".")[1]


def get_graphs_nodes(graph):
    nodes = []
    for node, attr in graph.nodes(data=True):
        if attr.get("type") == Type.PROCESS:
            nodes.append(Process(node, attr.get("process_duration"), attr.get("setup_duration")))
        else:
            nodes.append(Node(node))
    return nodes


def add_bought(graph, item_id):
    graph.add_node(item_id, type=Type.BOUGHT.value)

def add_produced(graph, item_id):
    graph.add_node(item_id, type=Type.PRODUCED.value)

def add_item(graph, item_id):
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