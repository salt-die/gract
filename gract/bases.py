from abc import ABC, abstractmethod
from itertools import count

from .scheduler import sleep


class Neighbors(ABC):
    """A collection of the neighbors of a Node.
    """

    @abstractmethod
    def __iter__(self):
        """Iterator over neighbors.
        """

    @abstractmethod
    def add(self, neighbor):
        """Add a neighbor.
        """

    def update(self, iterable):
        for neighbor in iterable:
            self.add(neighbor)


class Node(ABC):
    __slots__ = 'id', 'neighbors',

    neighbors_type = Neighbors
    counter = count()

    def __init__(self):
        self.id = next(self.counter)
        self.neighbors = self.neighbors_type()

    def __str__(self):
        return str(self.id)

    @abstractmethod
    def update(self):
        """Modify the local neighborhood of the node.
        """

    async def update_forever(self):
        """Asynchronously update local neighborhood forever.
        """
        while True:
            self.update()
            await sleep(0)
