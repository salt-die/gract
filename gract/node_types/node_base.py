from abc import ABC, abstractmethod
from itertools import count

from .neighbor_base import NeighborSet
from ..scheduler import sleep


class Node(ABC):
    """
    An asynchronous node in a Gract.

    Notes
    -----
    Node implementations require a `neighbors_cls` kwarg in the class definition.

    """
    __slots__ = 'id', 'neighbors', 'activity',

    _nnodes = count()

    def __init_subclass__(cls, neighbors_cls=None):

        if neighbors_cls is None:
            assert cls.__abstractmethods__, 'implementation of Node requires `neighbors_cls` kwarg.'
            return

        assert issubclass(neighbors_cls, NeighborSet), f'{neighbors_cls.__name__} is not NeighborSet'

        def __init__(self, neighbors=()):
            self.id = next(self._nnodes)
            self.activity = 0

            self.neighbors = neighbors_cls(neighbors)

        cls.__init__ = __init__

    def __str__(self):
        return str(self.id)

    @property
    def degree(self):
        return len(self.neighbors)

    @property
    def metadata(self):
        """Additional node information in a human readable format.
        """
        return f'type: {type(self).__name__}'

    @abstractmethod
    async def update(self):
        """
        Modify the local neighborhood of the node.

        Notes
        -----
        `activity` should be increased by 1 every time this method is called. (Or when this method is called and doesn't return early.)

        """

    async def update_forever(self):
        """Asynchronously update local neighborhood forever.
        """
        while True:
            await self.update()
            await sleep(0)
