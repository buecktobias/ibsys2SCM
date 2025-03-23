from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedAsDataclass

from material.db.models.base import Base


class Item(MappedAsDataclass, Base, unsafe_hash=True):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(primary_key=True)

    # noinspection PyUnresolvedReferences
    bought: Mapped["BoughtItem"] = relationship(
        "BoughtItem", default=None, back_populates="item", uselist=False, lazy="joined"
    )
    # noinspection PyUnresolvedReferences
    produced: Mapped["ProducedItem"] = relationship(
        "ProducedItem", default=None, back_populates="item", uselist=False, lazy="joined"
    )

    def is_bought(self) -> bool:
        return self.bought is not None

    def is_produced(self) -> bool:
        return self.produced is not None
