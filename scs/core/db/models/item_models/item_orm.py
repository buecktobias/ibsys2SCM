from __future__ import annotations

from sqlalchemy import ForeignKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.models.graph.graph_node_orm import GraphNodeORM


class ItemORM(GraphNodeORM):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(
            primary_key=True
    )
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
            "polymorphic_identity": __tablename__,
    }
    # Here's where the foreign key reference is declared
    __table_args__ = (
            ForeignKeyConstraint(
                    [id], [GraphNodeORM.id],
            ),
    )
