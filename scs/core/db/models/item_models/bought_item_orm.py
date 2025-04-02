from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from scs.core.db.models.item_models.item_orm import ItemORM


class BoughtItemORM(MappedAsDataclass, ItemORM):
    """
    Represents an ORM mapping for a bought item in the database.

    This class serves as a data model for a purchased item, including its pricing,
    discount, and ordering-related statistics. It inherits mappings and behavior
    from ItemORM and integrates additional attributes. The class also defines
    mapping to the corresponding database table for ORM usage.

    Attributes:
        __tablename__ (str): The name of the corresponding database table.
        __mapper_args__ (dict): Defines specific SQLAlchemy ORM mapper arguments,
            such as polymorphic identity.

        id (int): The primary key of the bought item, referencing the ItemORM ID
            with cascading updates on changes.
        base_price (float): The base price of the bought item before any discount.
        discount_amount (int): The discount amount applied to the base price.
        mean_order_duration (float): The average duration (e.g., in days) it takes
            for an order of this item to be processed or completed.
        order_std_dev (float): The standard deviation of ordering durations, giving
            insights into the consistency of order times.
        base_order_cost (float): The baseline cost associated with fulfilling
            orders for the item.

    """
    __tablename__ = "bought_item"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    id: Mapped[int] = mapped_column(ForeignKey(ItemORM.id, onupdate="CASCADE"), primary_key=True)
    base_price: Mapped[float]
    discount_amount: Mapped[int]
    mean_order_duration: Mapped[float]
    order_std_dev: Mapped[float]
    base_order_cost: Mapped[float]

    def __hash__(self):
        return hash(self.id)
