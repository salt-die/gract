from .node_base import Node
from .random_neighbors import RandomNeighbors
from ..scheduler import sleep


class GiveTakeNode(Node, neighbors_cls=RandomNeighbors):
    """
    A GiveTakeNode, u, chooses some neighbor, v. If deg(u) > deg(v),
    u will give v a neighbor, else u will steal a neighbor from v.

    Afterwards, u will sleep an amount of time inversely proportional to the difference
    of u and v's degrees.
    """
    __slots__ = ()

    async def update(self):
        if self.degree == 0:
            return

        neighbors = self.neighbors
        v = neighbors.choose()
        delta = self.degree - v.degree

        if delta > 0:
            v.neighbors.add( neighbors.pop() )
        else:
            neighbors.add( v.neighbors.pop() )

        self.activity += 1
        await sleep(.01 / (1 + abs(delta)))
