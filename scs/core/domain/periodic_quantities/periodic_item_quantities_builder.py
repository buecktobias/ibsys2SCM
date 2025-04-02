from collections import Counter

from scs.core.domain.item_models import Item
from scs.core.domain.periodic_quantities.periodic_item_quantities import PeriodicItemQuantity


class PeriodicItemQuantityBuilder:
    def __init__(self):
        self.periodic_item_quantity: dict[int, dict[Item, int]] = {}

    def add_product(self, item: Item, product_counts: list[int]):
        for period, count in enumerate(product_counts):
            period += 1
            if period not in self.periodic_item_quantity:
                self.periodic_item_quantity[period] = Counter[Item]()
            self.periodic_item_quantity[period][item] = count
        return self

    def build(self):
        return PeriodicItemQuantity(self.periodic_item_quantity)
