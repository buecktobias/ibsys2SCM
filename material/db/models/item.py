import logging

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from material.db.models.graph_node import GraphNode


class Item(GraphNode):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(
        ForeignKey("graph_node.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "item",
    }

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __repr__(self):
        logging.warning(f"Item {self.id} is neither bought nor produced")
        return f"Item({self.id})"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
