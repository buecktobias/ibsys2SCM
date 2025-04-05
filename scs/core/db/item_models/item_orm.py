from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.graph.graph_node_orm import GraphNodeORM


class ItemORM(GraphNodeORM):
    """
    Represents a database model for an item which extends the GraphNodeORM model.

    This class defines the "item" table with attributes such as id and type. It
    uses SQLAlchemy's ORM features including mapped columns and table constraints.
    The class assumes a polymorphic identity for distinguishing between object
    types in a single table inheritance scenario. This model is particularly
    useful for representing specialized graph nodes classified as items.

    Attributes:
        id (int): The primary key of the item, inheriting a foreign key
            constraint from the graph node table.
        type (str): A string value representing the type of the item, stored
            as a column with a maximum length of 50 characters.
    """
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(
            ForeignKey("graph_node.id", onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True
    )

    __mapper_args__ = {
            "polymorphic_identity": __tablename__,
    }
