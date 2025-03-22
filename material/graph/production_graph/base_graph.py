import typing

import matplotlib.pyplot as plt
import networkx as nx
from sqlalchemy import select
from sqlalchemy.orm import Session

from material.db.config import engine
from material.db.models import Process, Item


class DatabaseGraphLoader:
    def __init__(self, session: Session):
        self.session = session

    def load_processes(self):
        return self.session.execute(select(Process)).scalars().all()

    def get_item(self, item_id: int) -> Item:
        item = self.session.get(Item, item_id)
        if item is None:
            raise ValueError(f"Item {item_id} not found")
        return typing.cast(item, Item)


class NxGraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_process_node(self, process: Process) -> str:
        node_id = f"P{process.id}"
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


if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    with SessionLocal() as session:
        loader = DatabaseGraphLoader(session)
        graph = NxGraphBuilder().build_from_database(loader)

    pos = nx.spring_layout(graph, k=1, iterations=200)

    plt.figure(figsize=(20, 20))
    nx.draw_networkx_nodes(graph, pos, node_size=800)
    nx.draw_networkx_edges(graph, pos, width=1.5, alpha=0.7)
    nx.draw_networkx_labels(graph, pos, font_size=10)

    plt.axis("off")
    plt.tight_layout()
    plt.show()
