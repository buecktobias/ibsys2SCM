import abc

from pydantic import BaseModel

from scs.core.db.base import Base


class BaseMapper[T_ORM: Base, T_Domain: BaseModel](abc.ABC):
    """
    Base class for mappers that convert between ORM models and domain models.
    """

    @abc.abstractmethod
    def convert_to_domain(self, orm_model: T_ORM) -> T_Domain:
        """
        Convert an ORM model to its domain representation.
        :param orm_model: The ORM model to convert.
        :return: The domain representation of the ORM model.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abc.abstractmethod
    def convert_to_orm(self, domain_model: T_Domain) -> T_ORM:
        """
        Convert a domain model to its ORM representation.
        :param domain_model: The domain model to convert.
        :return: The ORM representation of the domain model.
        """
        raise NotImplementedError("Subclasses must implement this method.")
