from abc import ABC, abstractmethod
from itertools import count

from .scheduler import sleep


class Neighbors(ABC):
    """A collection of the neighbors of a Node or Edge.
    """

    @abstractmethod
    def __len__(self):
        """Number of neighbors.
        """

    @abstractmethod
    def __iter__(self):
        """Iterator over neighbors.
        """

    @abstractmethod
    def pop(self):
        """Return a neighbor.
        """

    @abstractmethod
    def append(self, neighbor):
        """Add a neighbor.
        """

    def extend(self, iterable):
        for neighbor in iterable:
            self.append(neighbor)

    @abstractmethod
    def choose(self):
        """Return some neighbor.
        """

class Node(ABC):
    __slots__ = 'id', 'neighbors',

    counter = count()

    def __init__(self, neighbors_type):
        assert issubclass(neighbors_type, Neighbors)

        self.id = next(self.counter)
        self.neighbors = neighbors_type()

    def __str__(self):
        return str(self.id)

    @abstractmethod
    def update(self):
        """Modify the local neighbor of the node.
        """

    async def update_forever(self):
        """Asynchronously update local neighborhood forever.
        """
        while True:
            self.update()
            await sleep(0)
