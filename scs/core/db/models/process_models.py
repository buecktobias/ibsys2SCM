from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.base import Base
from scs.core.db.models.graph.graph_node import GraphNodeORM
from scs.core.db.models.item_models import ItemORM
from scs.core.db.models.mixins.periodic_quantity import QuantityMixin
from scs.core.db.models.ws_models import WorkstationORM


class ProcessORM(GraphNodeORM):
    __tablename__ = "process"
    __mapper_args__ = {"polymorphic_identity": "process"}

    id: Mapped[int] = mapped_column(
            ForeignKey(GraphNodeORM.id, onupdate="CASCADE", ondelete="CASCADE"),
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

    # noinspection PyUnresolvedReferences
    graph: Mapped["MaterialGraphORM"] = relationship(back_populates="processes", uselist=False, lazy="joined")
    inputs: Mapped[list["ProcessInputORM"]] = relationship(back_populates="process", lazy="joined")
    workstation: Mapped[WorkstationORM] = relationship(lazy="joined")
    output: Mapped["ProcessOutputORM"] = relationship(back_populates="process", uselist=False, lazy="joined")


class ProcessInputORM(QuantityMixin, Base):
    __tablename__ = "process_input"
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

    item: Mapped[ItemORM] = relationship(lazy="joined")
    process: Mapped[ProcessORM] = relationship(back_populates="output", lazy="joined")
