from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class Item:
    id: int
    value: float


@dataclass(frozen=True)
class EndProduct(Item):
    pass


@dataclass(frozen=True)
class InHouseProduct(Item):
    pass


@dataclass(frozen=True)
class PurchasePart(Item):
    discount_quantity: int
    order_time: float
    order_time_deviation: float


@dataclass
class InventoryEntry:
    item: Item
    quantity: int


@dataclass
class Inventory:
    entries: dict[Item, InventoryEntry] = field(default_factory=dict)

    def get_quantity(self, item: Item) -> int:
        entry = self.entries.get(item)
        return entry.quantity if entry else 0

    def calculate_total_value(self) -> float:
        return sum(entry.item.value * entry.quantity for entry in self.entries.values())


@dataclass
class PlanningData:
    forecast: dict[EndProduct, int]
    current_inventory: Inventory


@dataclass
class PrimaryDemandCalculator:
    data: PlanningData

    def calculate(self) -> dict[EndProduct, int]:
        demand: dict[EndProduct, int] = {}
        for product, fc in self.data.forecast.items():
            current_qty = self.data.current_inventory.get_quantity(product)
            demand[product] = max(fc - current_qty, 0)
        return demand


if __name__ == "__main__":
    loader = XMLDataLoader("_data.xml")
    planning_data = loader.load_data()
    calculator = PrimaryDemandCalculator(planning_data)
    primary_demand = calculator.calculate()
    print("Primary Demand:", primary_demand)
