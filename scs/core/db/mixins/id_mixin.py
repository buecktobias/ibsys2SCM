from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.base import Base


class IdMixin(Base):
    """
    A mixin class for providing an ID attribute to models.

    This class adds a primary key ID column to any SQLAlchemy model that inherits
    it. It is marked as abstract and is designed to be used as a base class
    for creating models that require a primary key ID field.

    Attributes:
        id (int): The primary key ID attribute for the model. It is mapped to an
            integer field and serves as the primary key.
    """
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
