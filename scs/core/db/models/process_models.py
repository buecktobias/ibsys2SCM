from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.base import Base
from scs.core.db.models.graph_models import GraphNode, MaterialGraphORM
from scs.core.db.models.item_models import Item
from scs.core.db.models.mixins.quantity_mapping_mixin import QuantityMappingMixin
from scs.core.db.models.ws_models import WorkstationORM


class ProcessORM(GraphNode):
    __tablename__ = "process"
    __mapper_args__ = {"polymorphic_identity": "process"}
    __table_args__ = (CheckConstraint("process_duration_minutes >= 0"), CheckConstraint("setup_duration_minutes >= 0"))

    id: Mapped[int] = mapped_column(
            ForeignKey("graph_node.id", onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True
    )
    graph_id: Mapped[int] = mapped_column(
            ForeignKey("material_graph.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    workstation_id: Mapped[int] = mapped_column(
            ForeignKey("workstation.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    process_duration_minutes: Mapped[int]
    setup_duration_minutes: Mapped[int]

    graph: Mapped[MaterialGraphORM] = relationship(back_populates="processes", lazy="joined")
    inputs: Mapped[list["ProcessInputORM"]] = relationship(back_populates="process", lazy="joined")
    workstation: Mapped[WorkstationORM] = relationship(lazy="joined")
    output: Mapped["ProcessOutputORM"] = relationship(back_populates="process", uselist=False, lazy="joined")


class ProcessInputORM(QuantityMappingMixin, Base):
    __tablename__ = "process_input"
    __table_args__ = (CheckConstraint("quantity >= 1"),)
    process_id: Mapped[int] = mapped_column(
            ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    process: Mapped[ProcessORM] = relationship(back_populates="inputs", lazy="joined")


class ProcessOutputORM(Base):
    __tablename__ = "process_output"
    process_id: Mapped[int] = mapped_column(
            ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
            ForeignKey("item.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )

    item: Mapped[Item] = relationship(lazy="joined")
    process: Mapped[ProcessORM] = relationship(back_populates="output", lazy="joined")
