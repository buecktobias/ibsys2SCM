import abc
from abc import abstractmethod


class LabeledGraphNode(abc.ABC):

    @property
    @abstractmethod
    def label(self) -> str:
        """
        Returns the unique identifier for the item as a string.
        """
        pass

    def __repr__(self):
        return f"{self.label}"
