from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.models.base import Base
from scs.core.db.models.mixins.id_mixin import IdMixin


class GraphNodeORM(IdMixin, Base):
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
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
            "polymorphic_identity": "graph_node",
            "polymorphic_on": "type",
    }
