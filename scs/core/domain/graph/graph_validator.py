import networkx as nx

from scs.core.domain.graph.edge_models import ProcessInputEdge
from scs.core.domain.production_graph import ProductionGraph


class GraphValidator:
    def __init__(self, graph: ProductionGraph):
        self.graph = graph
        self.errors: list[str] = []

    def _get_node_obj(self, node_id: int):
        return self.graph.get_node_by_id(node_id)

    def validate(self) -> None:
        self.errors.clear()
        self._validate_cycle()
        self._validate_connectedness()
        self._validate_edges()

        if self.errors:
            raise ValueError("\n".join(self.errors))

    def _validate_cycle(self):
        if not nx.is_directed_acyclic_graph(self.graph.nx_graph):
            cycle = nx.find_cycle(self.graph, orientation="original")
            formatted = " → ".join(f"{u}->{v}" for u, v, _ in cycle)
            self.errors.append(f"Graph contains cycle: {formatted}")

    def _validate_connectedness(self):
        for node in self.graph.node_ids:
            if self.graph.nx_graph.degree(node) == 0:
                self.errors.append(f"Isolated node: {node}")

    def __validate_input_edge(self, input_edge: ProcessInputEdge):
        if (out_degree := self.graph.out_degree(input_edge.from_node)) != 1:
            raise RuntimeError(
                    f"Process {input_edge.from_node} must have exactly one output"
                    f" (out_degree={out_degree})"
            )

    def _validate_edges(self):
        incoming_edges = [
                edge for edge in self.graph.edges if isinstance(edge, ProcessInputEdge)
        ]
        all([self.__validate_input_edge(incoming_edge) for incoming_edge in incoming_edges])
