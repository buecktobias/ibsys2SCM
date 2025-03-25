import abc
import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Self

import networkx as nx
import base62

from material.initialize_db.graph.nodes.domainprocess import DomainProcess
from material.initialize_db.graph.nodes.graph_nodes import DomainStepProduced, DomainItem
from material.initialize_db.graph.nodes.mermaid_node import LabeledGraphNode


class BaseGraph(abc.ABC):
    """
    Abstract base class for nx_graph aggregates.
    """

    def __init__(self, label: str, graph_id: int | None, processes: set[DomainProcess], subgraphs: set[Self]):
        self.label = label
        self._processes: set[DomainProcess] = processes
        self._subgraphs: set[Self] = subgraphs
        self.graph_id = graph_id or self._calc_numerical_id()

    def get_subgraphs(self) -> set[Self]:
        return self._subgraphs

    def create_subgraph(self, label: str) -> Self:
        new_graph = SubGraph(label, None, set(), set())
        self._subgraphs.add(new_graph)
        return new_graph

    def get_process_by_output(self, step_produced: DomainStepProduced):
        for process in self._processes:
            if (isinstance(process.output, DomainStepProduced)
                    and process.output.parent_produced == step_produced.parent_produced
                    and process.output.step_number == step_produced.step_number):
                return process

    def add_process(self, process: DomainProcess):
        self._processes.add(process)
        process.graph_id = self.unique_numerical_id
        step_inputs = filter(lambda x: isinstance(x, DomainStepProduced), process.inputs.keys())
        for step_produced in step_inputs:
            previous_process = self.get_process_by_output(step_produced)
            if previous_process:
                step_produced.produced_by_workstation = process.workstation_id

    def get_own_processes(self) -> set[DomainProcess]:
        return self._processes

    def get_all_processes(self) -> set[DomainProcess]:
        return set(list(self._processes) + [
            process
            for subgraph in self.get_subgraphs()
            for process in subgraph.get_all_processes()
        ])

    def _calc_numerical_id(self):
        base62_label = re.sub(r'[^A-Za-z\d]+', '', self.label)
        return base62.decode(base62_label) % 10 ** 7

    @property
    def unique_numerical_id(self):

        return self.graph_id


class SubGraph(BaseGraph):
    pass


class DomainMaterialProductGraph(BaseGraph):
    def __init__(self, label: str, graph_id: int | None, subgraphs: set[SubGraph], processes: set[DomainProcess],
                 nx_digraph: nx.DiGraph):
        super().__init__(label, graph_id, processes, subgraphs)
        self._nx_digraph: nx.DiGraph = nx_digraph


class NxGraphBuilder:
    processes: set[DomainProcess] = field(default_factory=set)
    nx_graph: nx.DiGraph = field(default_factory=nx.DiGraph)

    def _get_all_nodes(self):
        nodes: set[LabeledGraphNode] = set()
        for process in self.processes:
            nodes.add(process)
            nodes.add(process.output)
            for input_node in process.inputs:
                nodes.add(input_node)
        return nodes

    def _has_node(self, node: LabeledGraphNode):
        return node in self._get_all_nodes()

    def _add_to_networkx(self, node: LabeledGraphNode) -> None:
        self.nx_graph.add_node(node, data=node)

    def _add_node(self, node: LabeledGraphNode) -> None:
        logging.info(f"Adding node {node} to child aggregates.")
        self._add_to_networkx(node)

    def _add_edges(self, from_resources: Counter[DomainItem], process: DomainProcess) -> None:
        """
        Adds edges to the nx_graph from input resources to the process and from the process to the _output item.
        """
        for item, quantity in from_resources.items():
            if not self._has_node(item):
                logging.info(f"Item {item} not found in subgraph; adding it.")
                self._add_node(item)
            self._add_edge(item, process, weight=quantity)
            logging.debug(f"Added edge from {item} to {process} with weight {quantity}.")
        self._add_edge(process, process.output)

    def _add_process_to_nx_graph(
            self,
            new_process: DomainProcess,
    ) -> DomainProcess | None:

        if self._has_node(new_process) or new_process in self.processes:
            logging.warning(f"Node {new_process} already exists in the nx_graph! Skipping addition.")
            return None

        self._add_node(new_process.output)
        self._add_node(new_process)
        self._add_edges(new_process.inputs, new_process)

        self._add_edge(new_process, new_process.output)
        logging.debug(f"Added edge from {new_process} to {new_process.output} with weight 1.")

        return new_process

    def _add_edge(self, source_node: LabeledGraphNode, target_node: LabeledGraphNode, weight: int = 1) -> None:
        self._add_edge(source_node, target_node, weight)

    def build_from_processes(self, processes: set[DomainProcess]) -> nx.DiGraph:
        for process in processes:
            self._add_process_to_nx_graph(process)
        return self.nx_graph


@dataclass
class MaterialProductGraphBuilder:
    label: str
    graph_id: int | None = None
    nx_graph: nx.DiGraph = field(default_factory=nx.DiGraph)
    subgraphs: set[SubGraph] = field(default_factory=set)
    processes: set[DomainProcess] = field(default_factory=set)

    def __post_init__(self):
        if not isinstance(self.subgraphs, set):
            raise ValueError("Subgraphs must be a set.")

    def create_subgraph(self, label: str) -> SubGraph:
        new_graph = SubGraph(label, None, set(), set())
        self.subgraphs.add(new_graph)
        return new_graph

    def create_nx_graph(self) -> nx.DiGraph:
        return NxGraphBuilder().build_from_processes(self.processes)

    def build(self) -> DomainMaterialProductGraph:
        return DomainMaterialProductGraph(
            self.label,
            self.graph_id,
            self.subgraphs,
            self.processes,
            self.create_nx_graph()
        )


@dataclass
class ResourceCounterBuilder[T]:
    counter: Counter[T] = field(default_factory=Counter)

    def add(self, node: LabeledGraphNode, count: int = 1) -> Self:
        self.counter[node] += count
        return self

    def add_items(self, items: list[DomainItem], count: int = 1) -> Self:
        for item in items:
            self.counter[item] += count
        return self

    def build(self):
        return self.counter
