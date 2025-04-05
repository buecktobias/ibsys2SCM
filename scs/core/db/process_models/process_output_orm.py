from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.base import Base


class ProcessOutputORM(Base):
    __tablename__ = "process_output"
    process_id: Mapped[int] = mapped_column(
            ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
            ForeignKey("item.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )

    # noinspection PyUnresolvedReferences
    item: Mapped[ItemORM] = relationship(lazy="joined")
    # noinspection PyUnresolvedReferences
    process: Mapped[ProcessORM] = relationship(back_populates="output", lazy="joined")
