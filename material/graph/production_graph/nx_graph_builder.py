import networkx as nx

from material.db.models import Process, Item
from material.graph.production_graph.database_graph_loader import DatabaseGraphLoader


class NxGraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_process_node(self, process: Process) -> str:
        node_id = f"{process.id}"
        self.graph.add_node(node_id, data=process)
        return node_id

    def add_item_node(self, item: Item) -> str:
        node_id = f"{item.id}"
        self.graph.add_node(node_id, data=item)
        return node_id

    def add_edge(self, src: str, dst: str, weight: int = 1):
        self.graph.add_edge(src, dst, weight=weight)

    def build_from_database(self, loader: DatabaseGraphLoader) -> nx.DiGraph:
        for process in loader.load_processes():
            proc_node = self.add_process_node(process)

            for inp in process.inputs:
                item_node = self.add_item_node(inp.item)
                self.add_edge(item_node, proc_node, weight=inp.quantity)

            if process.output:
                item_node = self.add_item_node(process.output.item)
                self.add_edge(proc_node, item_node)

        return self.graph
