import abc

from scs.core.db.models.item_models import Item
from scs.core.db.types import DomainSimTime


def abstract_property(func):
    return property(abc.abstractmethod(func))


class InvChange(abc.ABC):
    @abstract_property
    def id(self) -> str:
        pass

    @abstract_property
    def item(self) -> Item:
        pass

    @abc.abstractmethod
    def expected_inv_change_between(self, from_time: DomainSimTime, to_time: DomainSimTime) -> float:
        pass


class IOrder(InvChange, abc.ABC):
    @abstract_property
    def created_at(self) -> DomainSimTime:
        pass

    @abc.abstractmethod
    @property
    def creation_cost(self):
        pass
