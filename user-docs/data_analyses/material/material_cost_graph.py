import re
import time
from dataclasses import dataclass
from enum import Enum

from graph_setup import create_graph
import networkx as nx
from process_util import Node, Process, get_graphs_nodes

SETTINGS = r"%%{init: {'theme': 'dark'}, 'themeVariables': {'darkMode': true}}%%"

@dataclass
class ClassDef:
    fill: str
    stroke: str
    stroke_width: str
    color: str

    def __str__(self):
        return f"fill:{self.fill},stroke:{self.stroke},stroke-width:{self.stroke_width},color:{self.color}"


class MermaidStyle:
    def __init__(self):
        self.class_defs = {
            "bought": ClassDef("#455A64", "#CFD8DC", "2px", "#CFD8DC"),
            "produced": ClassDef("#263238", "#ECEFF1", "2px", "#ECEFF1"),
            "process": ClassDef("#1C313A", "#B0BEC5", "2px", "#B0BEC5")
        }

        self.class_assignments = []

    def get_class_defs(self):
        return "\n".join([f"classDef {k} {v}" for k, v in self.class_defs.items()])

    def add_class_assignment(self, node):
        self.class_assignments.append(f"{node.id}:::{node.node_type}")

    def get_class_assignments(self):
        return "\n".join(self.class_assignments)

    def get_mermaid_code(self):
        return "\n".join([self.get_class_defs(), self.get_class_assignments()])

class NxToMermaid:
    def __init__(self, graph):
        self.graph = graph
        self.lines = [SETTINGS, "flowchart LR"]
        self.indent = " " * 4
        self.class_assignments = []
        self.subgraphs = {}
        self.nodes = get_graphs_nodes(graph)

    def get_process_nodes(self):
        return filter(lambda n: isinstance(n, Process), self.nodes)

    def get_item_nodes(self):
        return filter(lambda n: not isinstance(n, Process), self.nodes)

    def get_produced_nodes(self):
        return filter(lambda n: n.is_produced, self.nodes)

    def add_node(self, node):
        self.class_assignments.append(self.indent + f'{node.id}:::{node.node_type}')
        label = (f"<div style='font-size:16px'><b>{node.id}</b></div>"
                 f"<small>{node.process_duration} - {node.setup_duration}</small>"
                 )
        self.lines.append(self.indent + f'{node.id}["{label}"]')

    def add_subgraph(self, group, nodes):
        self.lines.append(self.indent + f"subgraph {group}")
        for node in nodes:
            self.add_node(node)
        self.lines.append(self.indent + "end")
        self.lines.append("")

    def add_edge(self, from_node, to_node, attr):
        w = attr.get("weight", "")
        self.lines.append(self.indent + f'{from_node} -->|{w}| {to_node}')

    def add_class_definitions(self):
        self.lines.append(self.indent + "%% Style definitions")
        self.lines.append(self.indent + "classDef bought fill:#455A64,stroke:#CFD8DC,stroke-width:2px,color:#CFD8DC;")
        self.lines.append(self.indent + "classDef produced fill:#263238,stroke:#ECEFF1,stroke-width:2px,color:#ECEFF1;")
        self.lines.append(self.indent + "classDef process fill:#1C313A,stroke:#B0BEC5,stroke-width:2px,color:#B0BEC5;")
        self.lines.extend(self.class_assignments)

    def add_process_nodes(self):
        list(map(self.add_node, self.get_process_nodes()))


    def add_item_nodes(self):
        for node in self.get_produced_nodes():
            self.class_assignments.append(self.indent + f'{node.id}:::{node.node_type}')
            self.lines.append(self.indent + f'{node.id}([{node.id}])')

    def create_subgraphs(self):
        for node in self.get_process_nodes():
            if node.group not in self.subgraphs:
                self.subgraphs[node.group] = []
            self.subgraphs[node.group].append(node)
        return sorted(self.subgraphs.items(), key=lambda x: x[0])

    def convert(self):
        self.add_process_nodes()
        self.add_item_nodes()

        sorted_subgraphs = self.create_subgraphs()

        for group, nodes in sorted_subgraphs:
            self.add_subgraph(group, nodes)

        for from_node, to_node, attr in self.graph.edges(data=True):
            self.add_edge(from_node, to_node, attr)

        self.add_class_definitions()

        return "\n".join(self.lines)



    def save_html(self, mermaid_code):
        with open("template.html") as f:
            html = f.read()

        result = re.sub(r"{{ mermaidContent }}", mermaid_code, html)

        with open("diagram.html", "w", encoding="utf-8") as f:
            f.write(result)

    def save_mmd(self, diagram_code):
        with open("diagram.mmd", "w", encoding="utf-8") as f:
            f.write(diagram_code)

    def nx_to_mermaid(self):
        content = self.convert()
        self.save_mmd(content)
        self.save_html(content)



if __name__ == '__main__':
    NxToMermaid(create_graph()).nx_to_mermaid()

