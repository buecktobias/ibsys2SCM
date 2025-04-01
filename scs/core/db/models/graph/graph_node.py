from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.models.base import Base
from scs.core.db.models.mixins.id_mixin import IdMixin


class GraphNodeORM(IdMixin, Base):
    __tablename__ = "graph_node"
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
            "polymorphic_identity": "graph_node",
            "polymorphic_on": "type",
    }
