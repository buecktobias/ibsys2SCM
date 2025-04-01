import typing

from sqlalchemy import select
from sqlalchemy.orm import Session

from scs.core.db.models.graph.material_graph_orm import MaterialGraphORM
from scs.core.db.models.item_models import BoughtItemORM, ItemORM, ProducedItemORM
from scs.core.db.models.process_models import ProcessORM


class MaterialGraphRepository:
    def __init__(self, session: Session):
        self.session = session

    def load_processes(self):
        return self.session.execute(
                select(ProcessORM)
        ).unique().scalars().all()

    def load_bought_items(self):
        return self.session.execute(
                select(BoughtItemORM)
        ).unique().scalars().all()

    def load_produced_items(self):
        return self.session.execute(
                select(ProducedItemORM)
        ).unique().scalars().all()

    def get_graph_node_dict(self) -> dict[int, ProcessORM | BoughtItemORM | ProducedItemORM]:
        return {typing.cast(int, graph_node.id): graph_node for graph_node in
                list(self.load_bought_items()) + list(self.load_processes()) + list(self.load_produced_items())}

    def get_item(self, item_id: int) -> ItemORM:
        item = self.session.get(ItemORM, item_id)
        if item is None:
            raise ValueError(f"Item {item_id} not found")
        return typing.cast(item, ItemORM)

    def load_material_graph_root(self) -> MaterialGraphORM:
        stmt = select(MaterialGraphORM).where(MaterialGraphORM.parent_graph_id.is_(None))
        root = self.session.execute(stmt).unique().scalars().one_or_none()
        if root is None:
            raise ValueError("No root MaterialGraph found (parent_graph_id IS NULL)")
        return root
