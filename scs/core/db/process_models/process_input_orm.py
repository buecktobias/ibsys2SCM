from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.base import Base
from scs.core.db.mixins.quantity_mixin import QuantityMixin


class ProcessInputORM(QuantityMixin, Base):
    """
    Represents the ORM model for process input in the database.

    The ProcessInputORM class defines a model for storing input data associated with a
    process. It manages the relationship between processes and their inputs, allowing for
    joined loading and updates or deletions to be cascaded properly, ensuring seamless
    interaction with the underlying database.

    Attributes:
        __tablename__ (str): The name of the database table for this ORM model.
        process_id (int): The identifier of the associated process, acting as the primary key.
        process (ProcessORM): The relationship to the ProcessORM object, representing the
            associated process with joined loading.
    """
    __tablename__ = "process_input"
    process_id: Mapped[int] = mapped_column(
            ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    # noinspection PyUnresolvedReferences
    process: Mapped["ProcessORM"] = relationship(back_populates="inputs", lazy="joined")
