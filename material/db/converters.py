from sqlmodel import Session

from material.graph.production_graph.base_graph import BaseGraph
from models import (
    Item as ItemORM,
    Process as ProcessORM,
    ProcessInput as ProcessInputORM,
    ProcessOutput as ProcessOutputORM,
    MaterialGraphORM as GraphORM,
    BoughtItem as BoughtItemORM,
    ProducedItem as ProducedItemORM

)


class ProcessConverter:
    """
    Converts domain DomainProcess objects to ORM objects using session.merge.
    """

    def __init__(self, session: Session):
        self.session = session

    def add_process_to_db(self, process: DomainProcess):
        """
        Persists a single process (with its inputs and output). Assumes
        process.unique_numerical_id is the primary key and process.id
        is already set.
        """
        orm_process = ProcessORM(
            process_id=process.unique_numerical_id,
            workstation_id=process.workstation_id,
            process_duration=process.process_duration,
            setup_duration=process.setup_duration,
            graph_id=process.id
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

    def _persist_item(self, item: DomainItem):
        """
        Persists an item into the correct table (BoughtItem or ProducedItem).
        """
        if isinstance(item, DomainBought):
            orm_item = BoughtItemORM(
                item_id=item.unique_numerical_id,
                base_price=item.base_price,
                discount_amount=item.discount_amount,
                mean_order_duration=item.mean_order_duration,
                order_std_dev=item.order_std_dev,
                base_order_cost=0
            )
        elif isinstance(item, (DomainFullProduced, DomainStepProduced)):
            orm_item = ProducedItemORM(
                item_id=item.unique_numerical_id,
            )
        else:
            orm_item = ItemORM(item_id=item.unique_numerical_id)

        self.session.merge(orm_item)
        return orm_item


class GraphConverter:
    """
    Converts a domain BaseGraph (with processes and subgraphs) to ORM objects
    using session.merge. BaseGraph is assumed to have:
      - label (used as unique id)
      - get_own_processes() returning a set of processes,
      - get_subgraphs() returning a set of subgraphs.
    """

    def __init__(self, session: Session):
        self.session = session
        self.process_converter = ProcessConverter(session)

    def add_graph(self, graph: BaseGraph, parent_graph_id: int = None):
        """
        Persists the BaseGraph and its processes, then recursively persists its subgraphs.
        The BaseGraph's label is used as its id.
        """
        orm_graph = GraphORM(
            graph_id=graph.unique_numerical_id,
            name=graph.label,
            parent_graph_id=parent_graph_id
        )
        self.session.merge(orm_graph)
        # Persist the graph's own processes
        for process in graph.get_own_processes():
            process.id = orm_graph.id  # assign current graph id
            self.process_converter.add_process_to_db(process)
        # Recursively persist subgraphs, passing the current graph id as parent_graph_id
        for subgraph in graph.get_subgraphs():
            self.add_graph(subgraph, parent_graph_id=graph.unique_numerical_id)
        return orm_graph
