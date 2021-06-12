from abc import abstractmethod
from collections.abc import MutableSet


class NeighborSet(MutableSet):
    __slots__ = ()

    def __init__(self, neighbors=()):
        self |= neighbors

    @abstractmethod
    def choose(self):
        """Return a single neighbor, if one exists.
        """
