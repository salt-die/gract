from .node_base import Node
from .random_neighbors import RandomNeighbors


class GiveTakeNode(Node, neighbors_cls=RandomNeighbors):
    """
    A GiveTakeNode, u, chooses some neighbor, v. If deg(u) > deg(v),
    u will give v a neighbor, else u will steal a neighbor from v.
    """
    __slots__ = ()

    def update(self):
        if self.degree == 0:
            return

        neighbors = self.neighbors
        v = neighbors.choose()

        if self.degree > v.degree:
            v.neighbors.add( neighbors.pop() )
        else:
            neighbors.add( v.neighbors.pop() )

        self.activity += 1
