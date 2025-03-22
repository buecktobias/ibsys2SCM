import typing

from sqlalchemy import select
from sqlalchemy.orm import Session

from material.db.models import Process, Item


class DatabaseGraphLoader:
    def __init__(self, session: Session):
        self.session = session

    def load_processes(self):
        result = self.session.execute(select(Process))
        return result.unique().scalars().all()

    def get_item(self, item_id: int) -> Item:
        item = self.session.get(Item, item_id)
        if item is None:
            raise ValueError(f"Item {item_id} not found")
        return typing.cast(item, Item)
