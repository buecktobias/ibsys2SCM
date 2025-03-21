from typing import cast

import networkx as nx
from sqlmodel import Session, select

from material.db.models import Process, ProcessInput, ProcessOutput


class DatabaseGraphLoader:
    """
    Loads processes and related data from the database.
    """

    def __init__(self, session: Session):
        self.session = session

    def load_processes(self):
        """Returns all Process records from the DB."""
        return self.session.exec(select(Process)).all()

    def load_process_inputs(self, process_id: int):
        stmt = select(ProcessInput).where(ProcessInput. == process_id)
        return self.session.exec(stmt).all()

    def load_process_output(self, process_id: int):
        stmt: Select[ProcessOutput] = cast(Select[ProcessOutput],
                                           select(ProcessOutput).where(ProcessOutput.process_id == process_id))
        return self.session.exec(stmt).first()

    def get_item(self, item_id: int):
        """Retrieves an Item by its ID."""
        return self.session.get(Item, item_id)


class NxGraphBuilder:
    """
    Builds a networkx directed graph from processes and items.
    Each node stores the actual model instance in its 'data' attribute.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_process_node(self, process: Process) -> str:
        node_id = f"P{process.id}"
        # Do not hardcode type; simply store the model instance.
        self.graph.add_node(node_id, data=process)
        return node_id

    def add_item_node(self, item: Item) -> str:
        node_id = f"I{item.id}"
        self.graph.add_node(node_id, data=item)
        return node_id

    def add_edge(self, source_node: str, target_node: str, weight: int = 1) -> None:
        self.graph.add_edge(source_node, target_node, weight=weight)

    def build_from_database(self, loader: DatabaseGraphLoader) -> nx.DiGraph:
        """
        Loads processes and associated items from the database via loader,
        and builds a networkx directed graph.
        - Edges from an input item node to its process node carry a weight equal to the quantity.
        - Edges from a process node to its output item node have a weight of 1.
        """
        processes = loader.load_processes()
        for process in processes:
            proc_node = self.add_process_node(process)

            # Process Inputs (can be either bought or produced items)
            inputs = loader.load_process_inputs(process.id)
            for inp in inputs:
                item = loader.get_item(inp.id)
                item_node = self.add_item_node(item)
                self.add_edge(item_node, proc_node, weight=inp.quantity)

            # Process Output (should be a produced item)
            output = loader.load_process_output(process.id)
            if output:
                item = loader.get_item(output.item_id)
                item_node = self.add_item_node(item)
                self.add_edge(proc_node, item_node, weight=1)

        return self.graph


# Example usage:
if __name__ == "__main__":
    with Session(engine) as session:
        loader = DatabaseGraphLoader(session)
        builder = NxGraphBuilder()
        nx_graph = builder.build_from_database(loader)

    # Optionally, visualize the graph using matplotlib:
    import matplotlib.pyplot as plt

    pos = nx.spring_layout(nx_graph)
    nx.draw(nx_graph, pos, with_labels=True, node_color='lightblue', node_size=2500, font_size=10)
    plt.title("Process-Item Graph")
    plt.show()
