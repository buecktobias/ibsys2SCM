from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.base import Base
from scs.core.db.models.process_models.process_orm import ProcessORM


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
