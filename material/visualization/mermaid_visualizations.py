import re
import typing
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass
import yaml
from material.graph.nodes.graph_nodes import Item, Node, Bought, Produced, StepProduced, NodeAggregate
from material.graph.nodes.process import Process
from material.graph.production_graph.material_product_graph import MaterialProductGraph
from material.graph.sub_graph import SubGraph
from material.graph.util.process_util import get_process_outgoing_to


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
        self._lines = []
        self._indent_level = indent_level
        self._indent_str = "    "  # 4 spaces per indent level
        self.style = MermaidStyle()

    def init_mermaid(self, settings: dict[str, str | dict], diagram_type: str):
        self.add_lines(self.create_settings_lines(settings))
        self.add_line(diagram_type)
        self._indent_level += 1

    def create_settings_lines(self, settings: dict[str, str]) -> list[str]:
        return ["---"] + yaml.dump(settings).split("\n") + ["---"] + [""]

    def add_line(self, content):
        self._lines.append(f"{self._indent_str * self._indent_level}{content}")

    def add_lines(self, contents: list[str]):
        for content in contents:
            self.add_line(content)

    @contextmanager
    def create_subgraph(self, subgraph_name: str, direction="TB"):
        """Creates a subgraph context."""
        self.add_line(f"subgraph {subgraph_name}")
        self.add_line(f"direction {direction}")
        self._indent_level += 1
        try:
            yield self
        finally:
            self._indent_level -= 1
            self.add_line("end")

    def add_node(self, node_id: str, label: str):
        """Adds a node to the diagram."""
        self.add_line(f"{node_id}[\"{label}\"]")

    def add_rounded_node(self, node_id: str, label: str):
        """Adds a rounded node to the diagram."""
        self.add_line(f"{node_id}(({label}))")

    def add_arrow(self, from_node: str, to_node: str, label: str = ""):
        """Adds an arrow between two nodes, with an optional label."""
        arrow = f"{from_node} --{label}--> {to_node}" if label else f"{from_node} --> {to_node}"
        self.add_line(f"{arrow}")

    def add_class_assignment(self, node_uid, node_type):
        self.style.add_class_assignment(node_uid, node_type)

    def add_class_definition(self, name: str, fill: str, stroke: str, stroke_width: str, color: str):
        self.style.add_class_def(name, fill, stroke, stroke_width, color)

    def get_content(self) -> str:
        """Returns the full Mermaid diagram content including styles."""
        return "\n".join(self._lines + [self.style.get_mermaid_code()])


class NxToMermaid:
    def __init__(self, graph):
        self.graph: MaterialProductGraph = graph
        self.mermaid = MermaidStringBuilder()
        self.duplicate_bought_nodes: Counter[Bought] = Counter()
        settings = {
            "title": "Material Flow",
            "config": {
                "theme": "dark",
                "themeVariables": {"darkMode": True},
                "flowchart": {
                    "curve": "linear",
                    "defaultRenderer": "elk",
                },
            }
        }
        self.mermaid.init_mermaid(settings, "flowchart LR")

    def add_process_node(self, node: Process):
        self.mermaid.add_class_assignment(node.node_id, node.node_type.value)
        label = f"<b>{node.node_id}</b>"
        self.mermaid.add_node(node.node_id, label)

    def add_item_node(self, node: Item):
        self.mermaid.add_class_assignment(node.node_id, node.node_type.value)
        self.mermaid.add_rounded_node(node.node_id, node.node_id)

    def get_unique_bought_node_id(self, node: Bought):
        current_count = self.duplicate_bought_nodes.get(node, 0)
        self.duplicate_bought_nodes[node] = current_count + 1
        return node.node_id + f"_{current_count}"

    def get_process_input(self, processes: typing.Collection[Process], input_item: Node):
        if isinstance(input_item, Bought):
            input_id = self.get_unique_bought_node_id(input_item)
            self.mermaid.add_rounded_node(input_id, input_item.node_id)
            self.mermaid.add_class_assignment(input_id, input_item.node_type.value)
        elif isinstance(input_item, Produced):
            input_id = input_item.node_id
            self.add_item_node(input_item)
        elif isinstance(input_item, StepProduced):
            outgoing_to_list: list[Process] = get_process_outgoing_to(processes, input_item)
            input_id = outgoing_to_list[0].node_id if len(outgoing_to_list) == 1 else input_item.node_id
        else:
            raise ValueError(f"Node type {type(input_item)} not supported.")

        return input_id

    def add_processes(self, processes: typing.Collection[Process]):
        for process in processes:
            self.add_process_node(process)
            for input_item, _ in process.inputs.items():
                input_id = self.get_process_input(processes, input_item)
                self.mermaid.add_arrow(input_id, process.node_id)
            if isinstance(process.output, StepProduced):
                continue
            self.mermaid.add_arrow(process.node_id, process.output.node_id)

    def add_subgraph(self, subgraph: SubGraph):
        with self.mermaid.create_subgraph(subgraph.label):
            self.add_processes(subgraph.processes)
            for node_aggregate in subgraph.child_node_aggregates:
                if isinstance(node_aggregate, SubGraph):
                    self.add_subgraph(node_aggregate)

    def add_node_aggregate(self, node_aggregate: NodeAggregate):
        if isinstance(node_aggregate, SubGraph):
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
