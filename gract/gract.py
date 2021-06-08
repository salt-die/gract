from random import choices

from .scheduler import run_soon


# TODO: gracts shouldn't care if they're node-centric or edge-centric; current implementation is node-centric only.
class Gract:
    __slots__ = 'nodes', '_running'

    def __init__(self, node_type, neighbors_type, nnodes):
        self._running = False
        self.nodes = tuple( node_type(neighbors_type) for _ in range(nnodes) )

    @property
    def is_running(self):
        return self._running

    @classmethod
    def random_graph(cls, node_type, neighbors_type, degree, nnodes):
        g = cls(node_type, neighbors_type, nnodes)

        for node in g:
            node.neighbors.extend(choices(g.nodes, k=degree))

        return g

    @property
    def nx_adjlist(self):
        """The current adjacency list of the graph in a string format readable by networkx.
        """
        return '\n'.join(f'{node.id} {" ".join(map(str, node.neighbors))}' for node in self)

    def __iter__(self):
        yield from self.nodes

    def run(self):
        if self._running:
            raise RuntimeError('gract already running')

        self._running = True

        run_soon(node.update_forever() for node in self)
