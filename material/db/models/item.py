import logging

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

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __repr__(self):
        if self.is_bought():
            return f"K{self.id}"
        elif self.is_produced():
            return f"P{self.id}"
        else:
            logging.warning(f"Item {self.id} is neither bought nor produced")
            return f"Item({self.id})"
