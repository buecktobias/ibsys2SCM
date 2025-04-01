from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.base import Base
from scs.core.db.models.mixins.quantity_mixin import QuantityMixin
from scs.core.db.models.process_models.process_orm import ProcessORM


class ProcessInputORM(QuantityMixin, Base):
    __tablename__ = "process_input"
    process_id: Mapped[int] = mapped_column(
            ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    process: Mapped[ProcessORM] = relationship(back_populates="inputs", lazy="joined")
