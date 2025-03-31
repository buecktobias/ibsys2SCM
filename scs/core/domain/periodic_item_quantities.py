import dataclasses
from collections import Counter
from typing import Iterable

from scs.core.domain.item_models import ItemDomain


@dataclasses.dataclass
class PeriodicItemQuantity:
    _data: dict[int, dict[ItemDomain, int]]

    def has_continuous_periods(self) -> bool:
        for i in range(self.lowest_priority, self.highest_period + 1):
            if i not in self._data:
                return False
        return True

    def __assert_each_period_has_same_items(self):
        items = self.get_unique_items()
        if any(items != set(self._data[period].keys()) for period in self.get_periods()):
            raise ValueError(f"Items are not the same in every period !")

    def __post_init__(self):
        self.__assert_each_period_has_same_items()

    @property
    def highest_period(self):
        return max(self.get_periods())

    @property
    def lowest_priority(self):
        return min(self.get_periods())

    def cut_off_periods_lower_than(self, period_cutoff: int):
        assert self.has_continuous_periods()
        new_data: dict[int, dict[ItemDomain, int]] = {}
        for period, item_counts in self._data.items():
            if period >= period_cutoff:
                new_data[period] = item_counts
        return PeriodicItemQuantity(new_data)

    def with_starting_period(self, starting_period: int = 1):
        assert self.has_continuous_periods()
        new_data: dict[int, dict[ItemDomain, int]] = {}
        for period, item_counts in self._data.items():
            new_data[(period - self.lowest_priority) + starting_period] = self._data[period]
        return PeriodicItemQuantity(new_data)

    def has_period(self, period: int) -> bool:
        return period in self._data

    def add_period(self, item_counts: dict[ItemDomain, int]):
        self._data[self.highest_period + 1] = item_counts

    def get_counters(self, period: int) -> Counter[ItemDomain]:
        return Counter(self._data[period])

    def get_value_for_item(self, period: int, item: ItemDomain) -> int:
        return self._data[period][item]

    def get_unique_items(self) -> set[ItemDomain]:
        items = set()
        for item_counter in self._data.values():
            items.update(item_counter.keys())
        return items

    def get_periods(self) -> list[int]:
        return sorted(self._data.keys())

    def get_average_value(self, item: ItemDomain) -> float:
        return sum(self._data[t][item] for t in self.get_periods()) / len(self.get_periods())

    def get_average_values(self) -> dict[ItemDomain, float]:
        return {item: self.get_average_value(item) for item in self.get_unique_items()}

    def sum(self):
        return sum(sum(item_counts.values()) for item_counts in self._data.values())

    def items(self) -> Iterable[tuple[int, dict[ItemDomain, int]]]:
        return self._data.items()


class PeriodicItemQuantityBuilder:
    def __init__(self):
        self.periodic_item_quantity: dict[int, dict[ItemDomain, int]] = {}

    def add_product(self, item: ItemDomain, product_counts: list[int]):
        for period, count in enumerate(product_counts):
            period += 1
            if period not in self.periodic_item_quantity:
                self.periodic_item_quantity[period] = Counter[ItemDomain]()
            self.periodic_item_quantity[period][item] = count
        return self

    def build(self):
        return PeriodicItemQuantity(self.periodic_item_quantity)
