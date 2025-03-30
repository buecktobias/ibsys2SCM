from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.base import Base
from scs.core.db.models.process_models import ProcessORM


class GraphNode(Base):
    __tablename__ = "graph_node"
    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
            "polymorphic_identity": "graph_node",
            "polymorphic_on": "type",
    }


class MaterialGraphORM(Base):
    __tablename__ = "material_graph"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_graph_id: Mapped[Optional[int]] = mapped_column(
            ForeignKey("material_graph.id", onupdate="CASCADE", ondelete="SET NULL")
    )
    parent_graph: Mapped["MaterialGraphORM"] = relationship(
            back_populates="subgraphs", remote_side=[id], lazy="joined"
    )
    subgraphs: Mapped[list["MaterialGraphORM"]] = relationship(back_populates="parent_graph", lazy="joined")
    processes: Mapped[list["ProcessORM"]] = relationship(back_populates="graph", lazy="joined")
