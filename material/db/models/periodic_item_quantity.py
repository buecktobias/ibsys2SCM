import dataclasses
from collections import Counter


type PeriodicItemQuantity =


@dataclasses.dataclass
class PeriodicItemQuantity:
    data: dict[int, ItemCounter]

    def get_items(periodic_item_quantity: PeriodicItemQuantity) -> set[Item]:
        items = set()
        for item_counter in periodic_item_quantity.values():
            items.update(item_counter.keys())
        return items


    def get_periods(periodic_item_quantity: PeriodicItemQuantity) -> list[int]:
        return sorted(periodic_item_quantity.keys())


    def get_average_value(periodic_item_quantity: PeriodicItemQuantity, item: Item) -> float:
        return sum(periodic_item_quantity[t][item] for t in periodic_item_quantity) / len(periodic_item_quantity)


    def get_average_values(periodic_item_quantity: PeriodicItemQuantity) -> dict[Item, float]:
        return {item: get_average_value(periodic_item_quantity, item) for item in periodic_item_quantity[1]}


class PeriodicItemQuantityBuilder:
    def __init__(self):
        self.periodic_item_quantity: PeriodicItemQuantity = {}

    def add_product(self, item: Item, product_counts: list[int]):
        for period, count in enumerate(product_counts):
            period += 1
            if period not in self.periodic_item_quantity:
                self.periodic_item_quantity[period] = Counter[Item]()
            self.periodic_item_quantity[period][item] = count
        return self

    def build(self):
        return self.periodic_item_quantity
