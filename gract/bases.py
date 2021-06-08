from abc import ABC, abstractmethod
from itertools import count

from .scheduler import sleep


# DELETE?: How useful is this ABC? We can specify what methods we require of a collection of neighbors in Node/Edges instead.
# We only need enough functionality to allow Node.update or Edge.update to not error.
# Gract is currently using `extend` though to produce random graphs and __iter__ to produce adjacency lists.
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
        """Remove and return a neighbor.
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


# TODO: Nodes (and eventually Edges) will probably need to be more specific about what methods `neighbors` needs to implement.
#  Likely this will be added to some class attribute, e.g., `__neighbor_methods__`.
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
        """Modify the local neighborhood of the node.
        """

    async def update_forever(self):
        """Asynchronously update local neighborhood forever.
        """
        while True:
            self.update()
            await sleep(0)
