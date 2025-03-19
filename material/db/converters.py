from sqlalchemy.orm import Session
from material.graph.nodes.graph_nodes import FullProduced, Bought, StepProduced, Item
from material.graph.nodes.process import Process as DomainProcess
from material.graph.production_graph.base_graph import BaseGraph
from models import (
    Item as ItemORM,
    Process as ProcessORM,
    ProcessInput as ProcessInputORM,
    ProcessOutput as ProcessOutputORM,
    Graph as GraphORM
)


class ProcessConverter:
    """
    Converts domain Process objects to ORM objects using session.merge.
    """

    def __init__(self, session: Session):
        self.session = session

    def add_process_to_db(self, process: DomainProcess):
        """
        Persists a single process (with its inputs and output). Assumes
        process.unique_numerical_id is the primary key and process.graph_id
        is already set.
        """
        orm_process = ProcessORM(
            process_id=process.unique_numerical_id,
            workstation_id=process.workstation_id,
            process_duration_in_mins=process.process_duration,
            setup_duration_in_mins=process.setup_duration,
            graph_id=process.graph_id
        )
        self.session.merge(orm_process)
        # Persist each input
        for item, qty in process.inputs.items():
            self._persist_item(item)
            orm_input = ProcessInputORM(
                process_id=process.unique_numerical_id,
                item_id=item.unique_numerical_id,
                quantity=qty
            )
            self.session.merge(orm_input)
        # Persist the single output
        output = process.output
        self._persist_item(output)
        orm_output = ProcessOutputORM(
            process_id=process.unique_numerical_id,
            item_id=output.unique_numerical_id
        )
        self.session.merge(orm_output)
        return orm_process

    def _persist_item(self, item: Item):
        """
        Persists an item into the single item table.
        """
        orm_item = ItemORM(
            item_id=item.unique_numerical_id,
            type=item.node_type.value  # e.g. "bought", "produced", etc.
        )
        if isinstance(item, Bought):
            orm_item.base_price = item.base_price
            orm_item.discount_amount = item.discount_amount
            orm_item.discount_percentage = item.discount
            orm_item.mean_order_duration_in_periods = item.mean_order_duration
            orm_item.order_standard_deviation_in_periods = item.mean_order_std_dev
        elif isinstance(item, FullProduced):
            orm_item.base_value_price = item.base_value_price
        elif isinstance(item, StepProduced):
            orm_item.parent_item_id = item.parent_produced.node_numerical_id
        self.session.merge(orm_item)


class GraphConverter:
    """
    Converts a domain BaseGraph (with processes and subgraphs) to ORM objects
    using session.merge. BaseGraph is assumed to have:
      - label (used as unique graph_id)
      - get_own_processes() returning a set of processes,
      - get_subgraphs() returning a set of subgraphs.
    """

    def __init__(self, session: Session):
        self.session = session
        self.process_converter = ProcessConverter(session)

    def add_graph(self, graph: BaseGraph, parent_graph_id: str = None):
        """
        Persists the BaseGraph and its processes, then recursively persists its subgraphs.
        The BaseGraph's label is used as its graph_id.
        """
        orm_graph = GraphORM(
            graph_id=graph.label,
            name=graph.label,
            parent_graph_id=parent_graph_id
        )
        self.session.merge(orm_graph)
        # Persist the graph's own processes
        for process in graph.get_own_processes():
            process.graph_id = orm_graph.graph_id  # assign current graph id
            self.process_converter.add_process_to_db(process)
        # Recursively persist subgraphs, passing the current graph id as parent_graph_id
        for subgraph in graph.get_subgraphs():
            self.add_graph(subgraph, parent_graph_id=orm_graph.graph_id)
        return orm_graph
