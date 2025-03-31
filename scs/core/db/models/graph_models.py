from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.base import Base, IdMixin
from scs.core.db.models.process_models import ProcessORM


class GraphNodeORM(IdMixin, Base):
    __tablename__ = "graph_node"
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
            "polymorphic_identity": "graph_node",
            "polymorphic_on": "type",
    }


class MaterialGraphORM(IdMixin, Base):
    __tablename__ = "material_graph"
    name: Mapped[str]
    parent_graph_id: Mapped[Optional[int]] = mapped_column(
            ForeignKey("material_graph.id", onupdate="CASCADE", ondelete="SET NULL")
    )
    parent_graph: Mapped[MaterialGraphORM] = relationship(
            back_populates="subgraphs", remote_side=[super().id], lazy="joined"
    )
    subgraphs: Mapped[list[MaterialGraphORM]] = relationship(back_populates="parent_graph", lazy="joined")
    processes: Mapped[list[ProcessORM]] = relationship(back_populates="graph", lazy="joined")
