from random import random

from .neighbor_base import NeighborSet


class RandomNeighbors(NeighborSet):
    """A collection of neighbors where `pop` and `choose` select a random neighbor.
    """
    __slots__ = '_neighbors',

    def __init__(self, neighbors=()):
        self._neighbors = list(neighbors)

    def __iter__(self):
        yield from self._neighbors

    def __len__(self):
        return len(self._neighbors)

    def __contains__(self, neighbor):
        return neighbor in self._neighbors

    def pop(self):
        neighbors = self._neighbors

        i = int(random() * len(neighbors))

        # We efficiently remove from the list by swapping the random neighbor with the last neighbor then popping.
        neighbors[i], neighbors[-1] = neighbors[-1], neighbors[i]

        return neighbors.pop()

    def choose(self):
        neighbors = self._neighbors
        i = int(random() * len(neighbors))
        return neighbors[i]

    def add(self, neighbor):
        self._neighbors.append(neighbor)

    def discard(self, neighbor):
        try:
            self._neighbors.remove(neighbor)
        except ValueError:
            pass
