import re
from dataclasses import dataclass

from graph_setup_p1 import create_graph_p1
from graph_setup_p2 import create_graph_p2
from graph_setup_p3 import create_graph_p3
from production_graph import MaterialProductFlowGraph, Process, NodeType, Node

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
        self.class_assignments.append(f"{node.node_uid}:::{node.node_type}")

    def add_class_assignment_id(self, node_uid, node_type):
        self.class_assignments.append(f"{node_uid}:::{node_type}")

    def get_class_assignments(self):
        return "\n".join(self.class_assignments)

    def get_mermaid_code(self):
        return "\n".join([self.get_class_defs(), self.get_class_assignments()])


class NxToMermaid:
    def __init__(self, graph):
        self.graph: MaterialProductFlowGraph = graph
        self.lines = [SETTINGS, "flowchart LR"]
        self.mermaid_style = MermaidStyle()
        self.indent = " " * 4
        self.subgraphs = {}
        self.node_dict = {node.node_uid: node for node in self.nodes}
        self.duplicate_bought_nodes = {}

    @property
    def nodes(self):
        return self.graph.get_graphs_nodes()

    def get_process_nodes(self) -> list[Process]:
        return [n for n in self.nodes if isinstance(n, Process)]

    def get_produced_nodes(self):
        return [n for n in self.nodes if getattr(n, "node_type", False)]

    def add_process_node(self, node: Process):
        self.mermaid_style.add_class_assignment(node)
        label = (f"<div style='font-size:18px'><b>{node.workstation_id}</b></div>"
                 f"{node.process_duration}<br/>{node.setup_duration}")
        self.lines.append(self.indent + f'{node.node_uid}["{label}"]')

    def add_subgraph(self, group_name, process_nodes):
        self.lines.append(self.indent + f"subgraph {group_name}[<div style='font-size:21px'><b>{group_name}</b><br/></div>]")
        for node in process_nodes:
            self.add_process_node(node)
        self.lines.append(self.indent + "end" + "\n")

    def duplicate_bought_node(self, original_id):
        self.duplicate_bought_nodes[original_id] = self.duplicate_bought_nodes.get(original_id, 0) + 1
        new_id = f"{original_id}_{self.duplicate_bought_nodes[original_id]}"
        original_node = self.node_dict[original_id]
        self.mermaid_style.add_class_assignment_id(new_id, original_node.node_type)
        self.lines.append(self.indent + f'{new_id}([<div style=\'font-size:10px\'>{original_node.node_uid}</div>])')
        return new_id

    def _add_edge(self, from_node, to_node, weight, is_directed=True):
        arrow = "-->" if is_directed else "---"
        if weight == 1:
            self.lines.append(self.indent + f'{from_node} {arrow} {to_node}')
        else:
            self.lines.append(self.indent + f'{from_node} {arrow} |{weight}| {to_node}')

    def add_edge(self, from_node, to_node, attr):
        is_bought_edge = self.node_dict[from_node].node_type == NodeType.BOUGHT
        if is_bought_edge:
            from_node = self.duplicate_bought_node(from_node)
        self._add_edge(from_node, to_node, attr.get("weight"), is_directed=not is_bought_edge)

    def add_process_nodes(self):
        list(map(self.add_process_node, self.get_process_nodes()))

    def add_item_nodes(self):
        for node in self.get_produced_nodes():
            self.mermaid_style.add_class_assignment(node)
            self.lines.append(self.indent + f'{node.node_uid}([<div style=\'font-size:10px\'>{node.node_uid}</div>])')

    def create_subgraphs(self):
        for node in self.get_process_nodes():
            self.subgraphs[node.process_group] = self.subgraphs.get(node.process_group, []) + [node]
        return sorted(self.subgraphs.items(), key=lambda x: x[0])

    def convert(self):
        self.add_process_nodes()
        self.add_item_nodes()
        grouped = self.create_subgraphs()
        for group, nodes in grouped:
            self.add_subgraph(group, nodes)
        for from_node, to_node, attr in self.graph.graph.edges(data=True):
            self.add_edge(from_node, to_node, attr)
        return "\n".join(self.lines)

    def save_html(self, mermaid_code, graph_name):
        with open(f"template.html", encoding="utf-8") as f:
            html = f.read()
        result = re.sub(r"{{\s*mermaidContent\s*}}", mermaid_code, html)
        result = re.sub(r"{{\s*diagram_title\s*}}", graph_name, result)
        with open(f"diagram_{graph_name}.html", "w", encoding="utf-8") as f:
            f.write(result)

    def save_mmd(self, diagram_code, graph_name):
        with open(f"diagram_{graph_name}.mmd", "w", encoding="utf-8") as f:
            f.write(diagram_code)

    def nx_to_mermaid(self, name: str):
        content = self.convert()
        self.save_mmd(content, name)
        self.save_html(content, name)
