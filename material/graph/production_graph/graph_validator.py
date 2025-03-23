import networkx as nx

from material.db.models.item import Item
from material.db.models.models import Process


class GraphValidator:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.errors: list[str] = []

    def _get_node_obj(self, node_id: str):
        return self.graph.nodes[node_id]["data"]

    def validate(self) -> None:
        self.errors.clear()
        self._validate_cycle()
        self._validate_connectedness()
        self._validate_edges()

        if self.errors:
            raise ValueError("\n".join(self.errors))

    def _validate_cycle(self):
        if not nx.is_directed_acyclic_graph(self.graph):
            cycle = nx.find_cycle(self.graph, orientation="original")
            # cycle is a list of (src, dst, dir) tuples
            formatted = " → ".join(f"{u}->{v}" for u, v, _ in cycle)
            self.errors.append(f"Graph contains cycle: {formatted}")

    def _validate_connectedness(self):
        for node in self.graph.nodes:
            if self.graph.degree(node) == 0:
                self.errors.append(f"Isolated node: {node}")

    def _validate_edges(self):
        for src, dst, data in self.graph.edges(data=True):
            weight = data.get("weight", 1)
            src_obj = self._get_node_obj(src)
            dst_obj = self._get_node_obj(dst)

            if isinstance(src_obj, Process) and isinstance(dst_obj, Item):
                # Process → Item (output)
                if not dst_obj.is_produced():
                    self.errors.append(f"Invalid output: Process {src} → non‑produced Item {dst}")
                if weight != 1:
                    self.errors.append(f"Output edge weight must be 1: {src} → {dst} (got {weight})")
                if self.graph.out_degree(src) != 1:
                    self.errors.append(
                        f"Process {src} must have exactly one output (out_degree={self.graph.out_degree(src)})")

            elif isinstance(src_obj, Item) and isinstance(dst_obj, Process):
                # Item → Process (input)
                if not (src_obj.is_produced() or src_obj.is_bought()):
                    self.errors.append(f"Invalid input: non‑item source {src} → Process {dst}")
                if weight <= 0:
                    self.errors.append(f"Input edge weight must be >0: {src} → {dst} (got {weight})")

            else:
                self.errors.append(f"Invalid edge direction/type: {src} ({type(src_obj)}) → {dst} ({type(dst_obj)})")
