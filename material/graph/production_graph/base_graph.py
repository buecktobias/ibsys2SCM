import abc
import logging
from dataclasses import dataclass, field
from typing import Self

import networkx as nx

from material.core.resource_counter import ResourceCounter
from material.graph.nodes.graph_nodes import StepProduced
from material.graph.nodes.mermaid_node import LabeledGraphNode
from material.graph.nodes.process import Process


class BaseGraph(abc.ABC):
    """
    Abstract base class for nx_graph aggregates.
    """

    def __init__(self, label: str, processes: set[Process], subgraphs: set[Self]):
        self.label = label
        self._processes: set[Process] = processes
        self._subgraphs: set[Self] = subgraphs

    def get_subgraphs(self) -> set[Self]:
        return self._subgraphs

    def create_subgraph(self, label: str) -> Self:
        new_graph = SubGraph(label, set(), set())
        self._subgraphs.add(new_graph)
        return new_graph

    def get_process_by_output(self, step_produced: StepProduced):
        for process in self._processes:
            if (isinstance(process.output, StepProduced)
                    and process.output.parent_produced == step_produced.parent_produced
                    and process.output.step_number == step_produced.step_number):
                return process

    def add_process(self, process: Process):
        self._processes.add(process)
        step_inputs = filter(lambda x: isinstance(x, StepProduced), process.inputs.keys())
        for step_produced in step_inputs:
            previous_process = self.get_process_by_output(step_produced)
            if previous_process:
                step_produced.produced_by_workstation = process.workstation_id

    def get_own_processes(self) -> set[Process]:
        return self._processes

    def get_all_processes(self) -> set[Process]:
        return set(list(self._processes) + [
            process
            for subgraph in self.get_subgraphs()
            for process in subgraph.get_all_processes()
        ])


class SubGraph(BaseGraph):
    pass


class MaterialProductGraph(BaseGraph):
    def __init__(self, label: str, subgraphs: set[SubGraph], processes: set[Process], nx_digraph: nx.DiGraph):
        super().__init__(label, processes, subgraphs)
        self._nx_digraph: nx.DiGraph = nx_digraph


class NxGraphBuilder:
    processes: set[Process] = field(default_factory=set)
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

    def _add_edges(self, from_resources: ResourceCounter, process: Process) -> None:
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
            new_process: Process,
    ) -> Process | None:

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

    def build_from_processes(self, processes: set[Process]) -> nx.DiGraph:
        for process in processes:
            self._add_process_to_nx_graph(process)
        return self.nx_graph


@dataclass
class MaterialProductGraphBuilder:
    label: str
    nx_graph: nx.DiGraph = field(default_factory=nx.DiGraph)
    subgraphs: set[SubGraph] = field(default_factory=set)
    processes: set[Process] = field(default_factory=set)

    def __post_init__(self):
        if not isinstance(self.subgraphs, set):
            raise ValueError("Subgraphs must be a set.")

    def create_subgraph(self, label: str) -> SubGraph:
        new_graph = SubGraph(label, set(), set())
        self.subgraphs.add(new_graph)
        return new_graph

    def create_nx_graph(self) -> nx.DiGraph:
        return NxGraphBuilder().build_from_processes(self.processes)

    def build(self) -> MaterialProductGraph:
        return MaterialProductGraph(
            self.label,
            self.subgraphs,
            self.processes,
            self.create_nx_graph()
        )
