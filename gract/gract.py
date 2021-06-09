from collections.abc import Iterable
from itertools import chain
from random import choices

from . import analysis
from . import scheduler


# TODO: Add options for starting topologies.
class Gract:
    """
    A dynamic graph. Nodes asynchronously update their local neighborhoods.

    Parameters
    ----------
    node_types: Union[Node, Iterable[Node]]
        Types of nodes.

    nnode: Union[int, Iterable[int]]
        Number of each type of node.

    poll_delay: float
        While running, seconds until graph is polled.

    """
    __slots__ = 'nodes', 'results', 'poll_delay'

    def __init__(self, node_types, nnodes, poll_delay):
        if isinstance(nnodes, int):
            self.nodes = tuple( node_types() for _ in range(nnodes) )
        else:
            nodes = ((node_type() for _ in range(n)) for node_type, n in zip(node_types, nnodes))
            self.nodes = tuple( chain.from_iterable(nodes) )

        self.results = [ ]
        self.poll_delay = poll_delay

    @classmethod
    def random_graph(cls, node_types, nnodes, poll_delay, degree):
        gract = cls(node_types, nnodes, poll_delay)

        for node in gract:
            node.neighbors |= choices(gract.nodes, k=degree)

        return gract

    @property
    def nx_adjlist(self):
        """The current adjacency list of the graph in a string format readable by networkx.
        """
        return '\n'.join(f'{node} {" ".join(map(str, node.neighbors))}' for node in self)

    @property
    def updates(self):
        """The number of updates of each node in the graph.
        """
        total = sum(node.updates for node in self)
        individual_updates = '\n'.join(f'{node} {node.updates}' for node in self)
        return f'Total Updates: {total}\n{individual_updates}'

    def __iter__(self):
        yield from self.nodes

    async def _run(self, npolls):
        """Coroutine passed to scheduler's `run`.
        """
        scheduler.run_soon(node.update_forever() for node in self)

        for _ in range(npolls):
            await scheduler.sleep(self.poll_delay)
            self.results.append((self.nx_adjlist, self.updates))

    def run(self, npolls):
        """Run until n polls completed.
        """
        scheduler.run(self._run(npolls))

    save = analysis.save
