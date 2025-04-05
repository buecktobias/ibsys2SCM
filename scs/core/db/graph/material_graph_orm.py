from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.base import Base
from scs.core.db.mixins.id_mixin import IdMixin
from scs.core.db.process_models import ProcessORM


class MaterialGraphORM(IdMixin, Base):
    """
    Represents a material graph structure and its relationships in the database.

    This class models a material graph used for representing hierarchical structures
    of materials and the associated processes within a database. It provides fields
    and relationships to manage parent-child structures and link related processes.
    The `material_graph` table serves as the database table corresponding to this
    class.

    Attributes:
        __tablename__ (str): Name of the database table to which this class is mapped.
        name (Mapped[str]): Name of the material graph.
        parent_graph_id (Mapped[Optional[int]]): Foreign key referencing the parent
            material graph's ID. Enables hierarchical relationships.
        parent_graph (Mapped[MaterialGraphORM]): Relationship to the parent graph.
            Represents the parent material graph in the hierarchy.
        subgraphs (Mapped[list[MaterialGraphORM]]): Relationship to child material
            graphs. Lists all subgraphs associated with the current graph.
        processes (Mapped[list[ProcessORM]]): Relationship to processes associated
            with the material graph. Links the material graph to its processes.
    """
    __tablename__ = "material_graph"
    name: Mapped[str]
    parent_graph_id: Mapped[Optional[int]] = mapped_column(
            ForeignKey("material_graph.id", onupdate="CASCADE", ondelete="SET NULL")
    )

    parent_graph: Mapped[MaterialGraphORM] = relationship(
            back_populates="subgraphs", remote_side=lambda: MaterialGraphORM.id, lazy="joined"
    )
    subgraphs: Mapped[list[MaterialGraphORM]] = relationship(back_populates="parent_graph", lazy="joined")
    processes: Mapped[list[ProcessORM]] = relationship(back_populates="graph", lazy="joined")
