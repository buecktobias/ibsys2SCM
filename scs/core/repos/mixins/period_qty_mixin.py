import collections
from collections import Counter

from scs.core.db.mixins.period_mixin import PeriodMixin
from scs.core.db.mixins.quantity_mixin import QuantityMixin
from scs.core.domain.item_models import Item
from scs.core.domain.periodic_quantities.periodic_item_quantities import PeriodicItemQuantity
from scs.core.repos.mixins.period_repo_mixin import PeriodRepoMixin


class PeriodQtyMixin[T: (PeriodMixin, QuantityMixin)](PeriodRepoMixin[T]):
    def load_as_counter(self, period: int | None = None) -> Counter[Item]:
        rows: collections.Iterable[T] = self.find_by_period(period)
        return Counter({row.item: row.quantity for row in rows})

    def get_periodic_item_quantity(self) -> PeriodicItemQuantity:
        # Load all rows and convert them to a PeriodicItemQuantity
        return PeriodicItemQuantity(
                {
                        period: self.load_as_counter(period)
                        for period in self.unique_periods()
                }
        )
