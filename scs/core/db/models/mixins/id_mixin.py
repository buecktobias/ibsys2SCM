from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.models.base import Base


class IdMixin(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
