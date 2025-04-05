import random
from decimal import Decimal

from scs.core.domain.item_models import BoughtItem, ProducedItem


class ItemFactory:
    def create_bought_item(
            self,
            id: int | None = None,
            base_price: int | None = None,
            discount_amount: int | None = None,
            mean_order_duration: float | None = None,
            order_std_dev: float | None = None,
            base_order_cost: int | None = None
    ) -> BoughtItem:
        return BoughtItem(
                id=id or random.randint(1, 10 ** 8),
                base_price=base_price or Decimal(random.randint(1, 10 ** 1)),
                discount_amount=discount_amount or Decimal(random.randint(1, 10 ** 4)),
                mean_order_duration=mean_order_duration or random.random(),
                order_std_dev=order_std_dev or random.random(),
                base_order_cost=base_order_cost or random.randint(1, 10 ** 4),
        )

    def create_produced_item(self, id: int | None = None) -> ProducedItem:
        return ProducedItem(
                id=id or random.randint(1, 10 ** 8),
        )
