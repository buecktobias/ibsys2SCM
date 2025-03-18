import re
from contextlib import contextmanager
from dataclasses import dataclass

from material.graph.nodes.graph_nodes import NodeAggregate, Item, Node, Bought
from material.graph.nodes.process import Process
from material.graph.nodes.production_node_type import ProductionNodeType
from material.graph.production_graph.material_product_graph import MaterialProductGraph
from material.graph.sub_graph import SubGraph

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
        self.class_defs = {}
        self.class_assignments = []

    def add_class_def(self, name: str, fill: str, stroke: str, stroke_width: str, color: str):
        self.class_defs[name] = ClassDef(fill, stroke, stroke_width, color)

    def get_class_defs(self):
        return "\n".join([f"classDef {k} {v}" for k, v in self.class_defs.items()])

    def add_class_assignment(self, node_uid, node_type):
        self.class_assignments.append(f"{node_uid}:::{node_type}")

    def get_class_assignments(self):
        return "\n".join(self.class_assignments)

    def get_mermaid_code(self):
        return "\n".join([self.get_class_defs(), self.get_class_assignments()])


class MermaidStringBuilder:
    def __init__(self, indent_level=0):
        self.lines = []
        self.indent_level = indent_level
        self.indent_str = "    "  # 4 spaces per indent level
        self.style = MermaidStyle()

    def add_line(self, content):
        self.lines.append(f"{self.indent_str * self.indent_level}{content}")

    @contextmanager
    def create_subgraph(self, subgraph_name: str):
        """Creates a subgraph context."""
        self.lines.append(f"{self.indent_str * self.indent_level}subgraph {subgraph_name}")
        self.indent_level += 1
        try:
            yield self
        finally:
            self.indent_level -= 1
            self.lines.append(f"{self.indent_str * self.indent_level}end")

    def add_node(self, node_id: str, label: str):
        """Adds a node to the diagram."""
        self.lines.append(f"{self.indent_str * self.indent_level}{node_id}[\"{label}\"]")

    def add_rounded_node(self, node_id: str, label: str):
        """Adds a rounded node to the diagram."""
        self.lines.append(f"{self.indent_str * self.indent_level}{node_id}((\"{label}\"))")

    def add_arrow(self, from_node: str, to_node: str, label: str = ""):
        """Adds an arrow between two nodes, with an optional label."""
        arrow = f"{from_node} --{label}--> {to_node}" if label else f"{from_node} --> {to_node}"
        self.lines.append(f"{self.indent_str * self.indent_level}{arrow}")

    def add_class_assignment(self, node_uid, node_type):
        self.style.add_class_assignment(node_uid, node_type)

    def add_class_definition(self, name: str, fill: str, stroke: str, stroke_width: str, color: str):
        self.style.add_class_def(name, fill, stroke, stroke_width, color)

    def get_content(self) -> str:
        """Returns the full Mermaid diagram content including styles."""
        return "\n".join(self.lines + [self.style.get_mermaid_code()])


class NxToMermaid:
    def __init__(self, graph):
        self.graph: MaterialProductGraph = graph
        self.mermaid = MermaidStringBuilder()
        self.duplicate_bought_nodes = {}

        self.mermaid.add_line(SETTINGS)
        self.mermaid.add_line("flowchart LR")

    @property
    def nodes(self) -> list[NodeAggregate]:
        return self.graph.child_node_aggregates

    def get_process_nodes(self, nodes) -> list[Process]:
        return [n for n in nodes if isinstance(n, Process)]

    def get_produced_nodes(self, nodes):
        return [n for n in nodes if n.node_type == ProductionNodeType.PRODUCED]

    def add_process_node(self, node: Process):
        self.mermaid.add_class_assignment(node.node_id, node.node_type.value)
        label = (f"<div style='font-size:18px'><b>{node.node_id}</b></div>"
                 f"{node.process_duration}<br/>{node.process_duration}")
        self.mermaid.add_node(node.node_id, label)

    def add_item_node(self, node: Item):
        self.mermaid.add_class_assignment(node.node_id, node.node_type)
        self.mermaid.add_rounded_node(node.node_id, node.node_id)

    def add_subgraph(self, subgraph: SubGraph):
        with self.mermaid.create_subgraph(subgraph.label):
            for node in subgraph.child_node_aggregates:
                self.add_node_aggregate(node)
            for process in subgraph.processes:
                self.add_process_node(process)
                for input_item, _ in process.inputs.items():
                    input_id = self.add_bought_node(input_item)
                    self.mermaid.add_arrow(input_id, process.node_id)
                self.mermaid.add_arrow(process.node_id, process.output.node_id)

    def add_bought_node(self, node: Node):
        if not isinstance(node, Bought):
            return node.node_id
        current_count = self.duplicate_bought_nodes.get(node.node_numerical_id, 0)
        self.duplicate_bought_nodes[node.node_numerical_id] = current_count + 1

        new_id = node.node_id + f"_{current_count}"
        self.mermaid.add_rounded_node(new_id, node.node_id)
        return new_id

    def add_node_aggregate(self, node_aggregate: NodeAggregate):
        if isinstance(node_aggregate, Process):
            self.add_process_node(node_aggregate)
        elif isinstance(node_aggregate, Item):
            if node_aggregate.node_type != ProductionNodeType.BOUGHT:
                self.add_item_node(node_aggregate)
        elif isinstance(node_aggregate, SubGraph):
            self.add_subgraph(node_aggregate)
        else:
            raise ValueError(f"Node type {type(node_aggregate)} not supported.")

    def convert(self):
        for node_aggregate in self.graph.child_node_aggregates:
            self.add_node_aggregate(node_aggregate)

        return self.mermaid.get_content()

    def save_html(self, mermaid_code, graph_name):
        with open(f"diagrams/template.html", encoding="utf-8") as f:
            html = f.read()
        result = re.sub(r"{{\s*mermaidContent\s*}}", mermaid_code, html)
        result = re.sub(r"{{\s*diagram_title\s*}}", graph_name, result)
        with open(f"diagrams/diagram_{graph_name}.html", "w", encoding="utf-8") as f:
            f.write(result)

    def save_mmd(self, diagram_code, graph_name):
        with open(f"diagrams/diagram_{graph_name}.mmd", "w", encoding="utf-8") as f:
            f.write(diagram_code)

    def nx_to_mermaid(self, name: str):
        content = self.convert()
        self.save_mmd(content, name)
        self.save_html(content, name)
