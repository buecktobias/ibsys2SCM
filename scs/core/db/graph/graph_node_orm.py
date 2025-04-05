from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.base import Base


class GraphNodeORM(Base):
    """
    Represents a GraphNode in the database.

    This class defines the structure and behavior of a graph node within the database,
    using SQLAlchemy ORM. It inherits from IdMixin and Base, providing common identifiers
    and base functionalities. The class includes mapping for polymorphic behavior to
    differentiate between various graph node types.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        type (Mapped[str]): The type field for distinguishing polymorphic identity,
            stored as a string with a maximum length of 50 characters.
        __mapper_args__ (dict): Dictionary containing configuration for polymorphic
            behavior. Specifies the polymorphic identity as 'graph_node' and the
            polymorphic discriminator as 'type'.
    """
    __tablename__ = "graph_node"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
            "polymorphic_identity": "graph_node",
            "polymorphic_on": "type",
    }

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id
