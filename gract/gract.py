from random import choices

from .scheduler import is_running, run_soon


class Gract:
    __slots__ = 'nodes',

    def __init__(self, node_type, neighbors_type, nnodes):
        self.nodes = tuple( node_type(neighbors_type) for _ in range(nnodes) )

    @classmethod
    def random_graph(cls, node_type, neighbors_type, degree, nnodes):
        g = cls(node_type, neighbors_type, nnodes)

        for node in g:
            node.neighbors.extend(choices(g.nodes, k=degree))

        return g

    @property
    def adjacency(self):
        """Return an adjacency list of the graph in a string format readable by networkx.
        """
        return '\n'.join(f'{node.id} {" ".join(str(neighbor.id) for neighbor in node.neighbors)}' for node in self)

    def __iter__(self):
        yield from self.nodes

    def run(self):
        run_soon(node.update_forever() for node in self)
