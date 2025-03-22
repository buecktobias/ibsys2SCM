import abc
import logging
import re
import typing
from abc import abstractmethod
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass

import yaml

from material.db.models import MaterialGraphORM, BoughtItem, Process, Item, ProducedItem
from material.graph.util.process_util import get_process_outgoing_to


class MermaidContent(abc.ABC):
    @abstractmethod
    def get_mermaid_content(self):
        pass


@dataclass
class ClassDef(MermaidContent):
    name: str
    fill: str
    stroke: str
    stroke_width: str
    color: str

    def get_mermaid_content(self):
        return (f"classDef {self.name} "
                f"fill:{self.fill},"
                f"stroke:{self.stroke},"
                f"stroke-width:{self.stroke_width},"
                f"color:{self.color}")


class MermaidClass(MermaidContent):
    def __init__(self, class_def: ClassDef):
        self.class_def = class_def
        self.nodes = []

    def assign_node(self, node_uid):
        return self.nodes.append(node_uid)

    def get_mermaid_content(self):
        return f"{self.class_def.get_mermaid_content()}\n class {', '.join(self.nodes)} {self.class_def.name}"


class MermaidStringBuilder(MermaidContent):
    def __init__(self, indent_level=0):
        self._lines = []
        self._indent_level = indent_level
        self._indent_str = "    "  # 4 spaces per indent level

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

    def get_mermaid_content(self):
        return "\n".join(self._lines)


class NxToMermaid:
    def __init__(self, graph):
        self.graph: MaterialGraphORM = graph
        self.mermaid = MermaidStringBuilder()
        self.duplicate_bought_nodes: Counter[BoughtItem] = Counter()
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
        self.class_defs: dict[str, MermaidClass] = {}

    def add_process_node(self, node: Process):
        label = f"<b>{node.workstation_id}</b>"
        self.mermaid.add_node(str(node.id), label)

    def add_produced_item_node(self, produced_item: ProducedItem):
        self.mermaid.add_rounded_node(str(produced_item.item_id), str(produced_item.item_id))

    def add_rounded_styled_node(self, node_id: str, label: str):
        self.mermaid.add_rounded_node(node_id, label)

    def get_unique_bought_node_id(self, node: BoughtItem):
        current_count = self.duplicate_bought_nodes.get(node, 0)
        self.duplicate_bought_nodes[node] = current_count + 1
        return str(node.id) + f"_{current_count}"

    def add_class_assignment(self, node_id: str, class_id: str):
        self.class_defs[class_id].assign_node(node_id)

    def add_class_definition(self, class_def: ClassDef):
        self.class_defs[class_def.name] = MermaidClass(class_def)

    def add_processes(self, processes: typing.Collection[Process]):
        for process in processes:
            self.add_process_node(process)
            for input_item, _ in process.inputs.items():
                input_id = self.get_process_input(processes, input_item)
                self.mermaid.add_arrow(input_id, process.label)
            if isinstance(process.output, StepProduced):
                continue
            self.mermaid.add_arrow(process.label, process.output.label)

    def add_subgraph(self, subgraph: BaseGraph):
        with self.mermaid.create_subgraph(subgraph.label):
            self.add_processes(subgraph.get_own_processes())
            for sub_graph in subgraph.get_subgraphs():
                self.add_subgraph(sub_graph)

    def convert(self):
        for subgraph in self.graph.get_subgraphs():
            self.add_subgraph(subgraph)
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
