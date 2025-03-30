import abc

from scs.db.models.item import Item
from scs.db.types import DomainSimTime


def abstract_property(func):
    return property(abc.abstractmethod(func))


class IOrder(abc.ABC):
    @abstract_property
    def id(self) -> str:
        pass

    @abstract_property
    def created_at(self) -> DomainSimTime:
        pass

    @abstract_property
    def item(self) -> Item:
        pass

    @abc.abstractmethod
    def is_incoming(self) -> bool:
        pass

    @abc.abstractmethod
    @property
    def expected_execution_at_mean(self) -> DomainSimTime:
        pass

    @abc.abstractmethod
    @property
    def expected_execution_at_stdv(self) -> DomainSimTime:
        pass

    @abc.abstractmethod
    @property
    def was_executed(self) -> bool:
        pass

    @abc.abstractmethod
    @property
    def abs_highest_possible_change(self) -> int:
        pass

    @abc.abstractmethod
    @property
    def lowest_qty_inv_change(self) -> int:
        pass

    @abc.abstractmethod
    @property
    def cash_flow_per_item(self):
        pass

    @abc.abstractmethod
    @property
    def penalty(self):
        pass

    @abc.abstractmethod
    @property
    def creation_cost(self):
        pass

    @abc.abstractmethod
    def expected_inv_change_until(self, time: DomainSimTime) -> int:
        pass

    @abc.abstractmethod
    def expected_inv_change_between(self, start: DomainSimTime, end: DomainSimTime) -> int:
        pass


class BuyOffer(IOrder, abc.ABC):

    @property
    def offered_to_us(self) -> bool:
        return True

    @property
    def offered_by_us(self) -> bool:
        return False


class SellOrder(IOrder, abc.ABC):

    @property
    def offered_to_us(self) -> bool:
        return False

    @property
    def offered_by_us(self) -> bool:
        return False
