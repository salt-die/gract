from .bases import Node


class HeadSpin(Node):
    """A node that updates its adjacencies by "head"-moves or "spins".  See comments in `update` for further explanation.
    """
    __slots__ = ()

    def update(self):
        neighbors = self.neighbors

        if not neighbors:
            return

        old = neighbors.pop()

        # Last condition prevents all edge targets from converging to same node.
        if len(old.neighbors) <= len(self.neighbors) or (new := old.neighbors.choose()) is old:
            # The edge from self to old is now an edge from old to self,
            # i.e., the edge reversed (a /spin/)...
            old.neighbors.append( self )
        else:
            # ...the edge from self to old is now an edge from self to new,
            # i.e., the /head/ (target) of the edge moved...
            neighbors.append( new )

        # ...hence the name /HeadSpin/.
