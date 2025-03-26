import typing

from sqlalchemy import select
from sqlalchemy.orm import Session

from scs.db.models.item import Item
from scs.db.models.models import BoughtItem, MaterialGraphORM, Process, ProducedItem


class DatabaseGraphLoader:
    def __init__(self, session: Session):
        self.session = session

    def load_processes(self):
        return self.session.execute(
                select(Process)
        ).unique().scalars().all()

    def load_bought_items(self):
        return self.session.execute(
                select(BoughtItem)
        ).unique().scalars().all()

    def load_produced_items(self):
        return self.session.execute(
                select(BoughtItem)
        ).unique().scalars().all()

    def get_graph_node_dict(self) -> dict[int, Process | BoughtItem | ProducedItem]:
        return {typing.cast(int, graph_node.id): graph_node for graph_node in
                list(self.load_bought_items()) + list(self.load_processes()) + list(self.load_produced_items())}

    def get_item(self, item_id: int) -> Item:
        item = self.session.get(Item, item_id)
        if item is None:
            raise ValueError(f"Item {item_id} not found")
        return typing.cast(item, Item)

    def load_material_graph_root(self) -> MaterialGraphORM:
        stmt = select(MaterialGraphORM).where(MaterialGraphORM.parent_graph_id.is_(None))
        root = self.session.execute(stmt).unique().scalars().one_or_none()
        if root is None:
            raise ValueError("No root MaterialGraph found (parent_graph_id IS NULL)")
        return root
