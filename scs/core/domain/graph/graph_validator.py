import networkx as nx

from scs.core.db.models import Item
from scs.core.db.models.process_models import ProcessORM
from scs.core.db.models.item_models import BoughtItemORM, ProducedItemORM
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

    def _validate_edges(self):
        for weighted_edge in self.graph.edges:
            if isinstance(weighted_edge.from_node, ProcessORM) and isinstance(weighted_edge.to_node, Item):
                # ProcessORM → ItemORM (output)
                if not isinstance(dst_obj, ProducedItemORM):
                    self.errors.append(f"Invalid output: Process {src} → non‑produced Item {dst}")
                if weight != 1:
                    self.errors.append(f"Output edge weight must be 1: {src} → {dst} (got {weight})")
                if self.graph.out_degree(src) != 1:
                    self.errors.append(
                            f"Process {src} must have exactly one output (out_degree={self.graph.out_degree(src)})"
                    )

            elif isinstance(src_obj, Item) and isinstance(dst_obj, ProcessORM):
                # ItemORM → ProcessORM (input)
                if not (isinstance(src_obj, ProducedItemORM) or isinstance(src_obj, BoughtItemORM)):
                    self.errors.append(f"Invalid input: non‑item source {src} → Process {dst}")
                if weight <= 0:
                    self.errors.append(f"Input edge weight must be >0: {src} → {dst} (got {weight})")

            else:
                self.errors.append(f"Invalid edge direction/type: {src} ({type(src_obj)}) → {dst} ({type(dst_obj)})")
