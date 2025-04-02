from __future__ import annotations

import abc
import decimal
import logging

from pydantic import BaseModel, Field


class GraphNode(BaseModel, abc.ABC):
    id: int = Field(ge=0, title="Unique identifier for a Graph Node", description="Used in the in the Material Graph")

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Item(GraphNode, abc.ABC):
    pass


class BoughtItem(Item):
    """
    Represents an item that has been bought.
    Attributes:
        base_price (float):
        discount_amount (float):
        mean_order_duration (float):
        order_std_dev (float):
        base_order_cost (float):
    """
    base_price: decimal.Decimal = Field(ge=0, title="Base price of the item")
    discount_amount: decimal.Decimal = Field(ge=0, title="Discount amount applied to the base price")
    mean_order_duration: float = Field(ge=0, title="Average duration (in periods) it takes for an order of this item")
    order_std_dev: float = Field(ge=0, title="Standard deviation of ordering durations (in periods)")
    base_order_cost: float = Field(ge=0, title="Baseline cost associated with fulfilling orders for the item")


class ProducedItem(Item):
    """
    Represents a produced item that extends the base functionality of an item.
    Attributes:
        id (int): unique identifier for the item.
    """
    pass
