from random import randrange, choice

from .bases import Neighbors


class RandomNeighbors(Neighbors):
    """A collection of neighbors where `pop` and `choose` select a random neighbor.
    """
    __slots__ = '_neighbors',

    def __init__(self):
        self._neighbors = [ ]

    def __len__(self):
        return len(self._neighbors)

    def __iter__(self):
        yield from self._neighbors

    def pop(self):
        neighbors = self._neighbors

        i = randrange(len(neighbors))

        # We efficiently remove from the list by swapping the random neighbor with the last neighbor then popping.
        neighbors[i], neighbors[-1] = neighbors[-1], neighbors[i]

        return neighbors.pop()

    def append(self, item):
        self._neighbors.append(item)

    def choose(self):
        return choice(self._neighbors)
