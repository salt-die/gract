from .node_base import Node
from .random_neighbors import RandomNeighbors


class HeadSpinNode(Node, neighbors_cls=RandomNeighbors):
    """
    An edge with a source at this node will have its target updated to an adjacent
    node (head-move) or reverse (spin).
    """
    __slots__ = ()

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

        self.activity += 1
