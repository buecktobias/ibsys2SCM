import abc
import re
import typing
from abc import abstractmethod
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass

import networkx as nx
import yaml

from material.db.models.models import MaterialGraphORM, BoughtItem, Process, ProducedItem


class VisualizationMaterialGraph:
    def __init__(self, orm_node: MaterialGraphORM, nx_graph: nx.DiGraph):
        self.id = orm_node.id
        self.name = orm_node.name
        self.processes = []
        for process in orm_node.processes:
            process_node_id = f"{process.id}"
            if nx_graph.has_node(process_node_id):
                self.processes.append(process)
        self.subgraphs = [
            VisualizationMaterialGraph(child, nx_graph)
            for child in orm_node.subgraphs
        ]


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
    def __init__(self, graph: VisualizationMaterialGraph):
        self.graph: VisualizationMaterialGraph = graph
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
        self._unique_nodes: set[str] = set()

    def _add_process_node(self, node: Process):
        label = f"<b>{node.workstation_id}</b>"
        node_id = str(node.id)
        if node_id not in self._unique_nodes:
            self._unique_nodes.add(node_id)
            self.mermaid.add_node(node_id, label)
        return node_id

    def _add_produced_item_node(self, produced_item: ProducedItem):
        node_id = "E" + str(produced_item.item_id)
        if node_id not in self._unique_nodes:
            self._unique_nodes.add(node_id)
            self.mermaid.add_rounded_node(node_id, node_id)
        return node_id

    def __get_unique_bought_node_id(self, node: BoughtItem):
        current_count = self.duplicate_bought_nodes.get(node, 0)
        self.duplicate_bought_nodes[node] = current_count + 1
        return "K" + str(node.item_id) + f"{current_count}"

    def _add_bought_item_node(self, bought_item: BoughtItem):
        node_id = self.__get_unique_bought_node_id(bought_item)
        self.mermaid.add_rounded_node(node_id, str(bought_item.item_id))
        return node_id

    def add_item(self, item):
        if item.is_bought():
            return self._add_bought_item_node(item.bought)
        elif item.is_produced():
            return self._add_produced_item_node(item.produced)
        raise ValueError(f"Item type {type(item)} not recognized")

    def add_class_assignment(self, node_id: str, class_id: str):
        self.class_defs[class_id].assign_node(node_id)

    def add_class_definition(self, class_def: ClassDef):
        self.class_defs[class_def.name] = MermaidClass(class_def)

    def add_processes(self, processes: typing.Collection[Process]):
        for process in processes:
            self._add_process_node(process)
            for input_item in process.inputs:
                input_item_id = self.add_item(input_item.item)
                self.mermaid.add_arrow(input_item_id, str(process.id))
            output_item_id = self.add_item(process.output.item)
            self.mermaid.add_arrow(str(process.id), output_item_id)

    def add_subgraph(self, subgraph: VisualizationMaterialGraph):
        with self.mermaid.create_subgraph(subgraph.name):
            self.add_processes(subgraph.processes)
            for sub_graph in subgraph.subgraphs:
                self.add_subgraph(sub_graph)

    def get_mermaid_content(self):
        for subgraph in self.graph.subgraphs:
            self.add_subgraph(subgraph)
        return self.mermaid.get_mermaid_content()

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
        content = self.get_mermaid_content()
        self.save_mmd(content, name)
        self.save_html(content, name)
