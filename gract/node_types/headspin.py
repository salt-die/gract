from random import randrange, choice

from ..bases import Neighbors, Node


class RandomNeighbors(Neighbors):
    """A collection of neighbors where `pop` and `choose` select a random neighbor.
    """
    __slots__ = '_neighbors',

    def __init__(self):
        self._neighbors = [ ]

    def __iter__(self):
        yield from self._neighbors

    def __len__(self):
        return len(self._neighbors)

    def pop(self):
        neighbors = self._neighbors

        i = randrange(len(neighbors))

        # We efficiently remove from the list by swapping the random neighbor with the last neighbor then popping.
        neighbors[i], neighbors[-1] = neighbors[-1], neighbors[i]

        return neighbors.pop()

    def choose(self):
        return choice(self._neighbors)

    def add(self, neighbor):
        self._neighbors.append(neighbor)


class HeadSpin(Node):
    """
    An edge with a source at this node will have its target updated to an adjacent
    node (head-move) or reverse (spin).
    """
    __slots__ = ()

    neighbors_type = RandomNeighbors

    def update(self):
        neighbors = self.neighbors

        if not neighbors:
            return

        old = neighbors.pop()

        # Last condition prevents all edge targets from converging to same node.
        if not old.neighbors or (new := old.neighbors.choose()) is old:
            old.neighbors.add( self )
        else:
            neighbors.add( new )
