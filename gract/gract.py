from random import choices

from .scheduler import run, run_soon, sleep


# TODO: Add options for starting topologies.
# TODO: Keep track of number of node updates.  This along with `delay` parameter could be added as meta-data to adjacency-lists.
class Gract:
    """A dynamic graph. Nodes asynchronously update their local neighborhoods.
    """
    __slots__ = 'nodes',

    def __init__(self, node_type, nnodes):
        # It would make sense to allow multiple node types as long as nodes had some common api to work with each other.
        # An iterable of types and an iterable of nnodes will be the future.
        self.nodes = tuple( node_type() for _ in range(nnodes) )

    @classmethod
    def random_graph(cls, node_type, nnodes, degree):
        gract = cls(node_type, nnodes)

        for node in gract:
            node.neighbors.update(choices(gract.nodes, k=degree))

        return gract

    @property
    def nx_adjlist(self):
        """The current adjacency list of the graph in a string format readable by networkx.
        """
        return '\n'.join(f'{node.id} {" ".join(map(str, node.neighbors))}' for node in self)

    def __iter__(self):
        yield from self.nodes

    async def _main(self, npolls, delay):
        """Coroutine passed to scheduler's `run`.
        """
        run_soon(node.update_forever() for node in self)

        adj_lists = [ ]
        for _ in range(npolls):
            await sleep(delay)
            adj_lists.append(self.nx_adjlist)

        return adj_lists

    def run(self, npolls, delay):
        """Run the gract. Adjacency list is added to a list every delay seconds npolls times.
        """
        return run(self._main(npolls, delay))
