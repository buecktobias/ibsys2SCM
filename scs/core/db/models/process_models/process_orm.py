from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.graph.graph_node_orm import GraphNodeORM
from scs.core.db.models.process_models import ProcessInputORM, ProcessOutputORM
from scs.core.db.models.workstation_orm import WorkstationORM


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
