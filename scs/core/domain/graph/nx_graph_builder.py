import networkx as nx

from scs.core.domain.item_models import GraphNode
from scs.core.domain.process_domain_model import Process


class NxGraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def _add_edge(self, from_node: GraphNode, to_node: GraphNode, weight: int = 1):
        self.graph.add_node(from_node.id)
        self.graph.add_node(to_node.id)
        self.graph.add_edge(from_node.id, to_node.id, weight=weight)

    def build_from_processes(self, processes: list[Process]) -> nx.DiGraph:
        for process in processes:
            for inp, quantity in process.inputs.items():
                self._add_edge(inp, process, weight=quantity)
            self._add_edge(process, process.output)
        return self.graph
