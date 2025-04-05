from collections import Counter

import sqlalchemy

from scs.core.db.periodic import InventoryItemORM
from scs.core.domain.item_models import Item


class InventoryRepo:
    def __init__(self, session: sqlalchemy.orm.Session):
        self.session = session

    def get_inventory_for_period(self, period: int) -> Counter[Item]:
        """
        Get the inventory for a specific period.

        :param period: The period for which to get the inventory.
        :return: A Counter of Item objects with their quantities.
        """
        return InventoryItemORM.load_as_counter(self.session, period)
