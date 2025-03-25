from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from material.db.models.base import Base


class GraphNode(Base):
    __tablename__ = "graph_node"
    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "graph_node",
        "polymorphic_on": "type",
    }
