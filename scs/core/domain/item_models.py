from __future__ import annotations

import abc
import logging

from pydantic import BaseModel


class GraphNodeDomain(BaseModel, abc.ABC):
    id: int

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


class ItemDomain(GraphNodeDomain, abc.ABC):
    pass


class BoughtItemDomain(ItemDomain):
    """
    Represents an item that has been bought.
    Attributes:
        base_price: float
        discount_amount: int
        mean_order_duration: float
        order_std_dev: float
        base_order_cost: float

    """
    base_price: float
    discount_amount: int
    mean_order_duration: float
    order_std_dev: float
    base_order_cost: float


class ProducedItemDomain(ItemDomain):
    pass
