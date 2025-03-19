from sqlalchemy.orm import Session

from material.graph.nodes.graph_nodes import FullProduced, Bought, StepProduced, Item
from material.graph.nodes.process import Process
from models import (
    Item as ItemORM, BoughtItem as BoughtItemORM, FullProducedItem as FullProducedItemORM,
    StepProduced as StepProducedORM,
    Process as ProcessORM, ProcessInput as ProcessInputORM, ProcessOutput as ProcessOutputORM
)


def get_or_create(session: Session, orm_cls, pk, **kwargs):
    instance = session.get(orm_cls, pk)
    if instance:
        return instance
    instance = orm_cls(**{orm_cls.__mapper__.primary_key[0].name: pk}, **kwargs)
    session.add(instance)
    return instance


class ProcessConverter:
    def __init__(self, session: Session):
        self.session = session

    def add_process_to_db(self, process: Process):
        orm_process = get_or_create(
            self.session, ProcessORM, process.unique_numerical_id,
            workstation_id=process.workstation_id,
            process_duration_in_mins=process.process_duration,
            setup_duration_in_mins=process.setup_duration
        )
        for item, qty in process.inputs.items():
            self._persist_item(item)
            inp = ProcessInputORM(process_id=process.unique_numerical_id, item_id=item.node_numerical_id, quantity=qty)
            self.session.merge(inp)
        output = process.output
        self._persist_item(output)
        out = ProcessOutputORM(process_id=process.unique_numerical_id, item_id=output.node_numerical_id)
        self.session.merge(out)
        return orm_process

    def _persist_item(self, item: Item):
        if isinstance(item, Bought):
            get_or_create(self.session, BoughtItemORM, item.node_numerical_id,
                          base_price=item.base_price, discount_amount=item.discount_amount,
                          discount_percentage=item.discount_percentage,
                          mean_order_duration_in_periodes=item.mean_order_duration,
                          mean_order_standard_deviation_in_periodes=item.mean_order_std_dev)
        elif isinstance(item, FullProduced):
            get_or_create(self.session, FullProducedItemORM, item.node_numerical_id,
                          base_value_price=item.base_value_price)
        elif isinstance(item, StepProduced):
            if item.produced_by_workstation:
                get_or_create(self.session, StepProducedORM, item.unique_item_id,
                              parent_item_id=item.parent_produced.node_numerical_id)
        else:
            get_or_create(self.session, ItemORM, item.node_numerical_id)


class GraphConverter:
    def __init__(self, session: Session):
        self.converter = ProcessConverter(session)

    def add_graph(self, graph):
        for process in graph.get_all_processes():
            self.converter.add_process_to_db(process)
        self.converter.session.commit()
