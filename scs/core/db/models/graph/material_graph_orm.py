from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.base import Base
from scs.core.db.models.mixins.id_mixin import IdMixin
from scs.core.db.models.process_models import ProcessORM


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
