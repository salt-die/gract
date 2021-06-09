from collections.abc import Iterable
from itertools import chain
from random import choices

from . import analysis
from . import scheduler

_POLL_ATTRS = 'nx_adjlist', 'activity',  # Attributes that are saved in results when a gract is polled.


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

    """
    __slots__ = 'nodes', 'results',

    def __init__(self, node_types, nnodes):
        if isinstance(nnodes, int):
            self.nodes = tuple( node_types() for _ in range(nnodes) )
        else:
            nodes = ((node_type() for _ in range(n)) for node_type, n in zip(node_types, nnodes))
            self.nodes = tuple( chain.from_iterable(nodes) )

        self.results = [ ]

    @classmethod
    def random_graph(cls, node_types, nnodes, degree):
        gract = cls(node_types, nnodes)

        for node in gract:
            node.neighbors |= choices(gract.nodes, k=degree)

        return gract

    def __iter__(self):
        yield from self.nodes

    @property
    def nx_adjlist(self):
        """The current adjacency list of the graph in a string format readable by networkx.
        """
        return '\n'.join(f'{node} {" ".join(map(str, node.neighbors))}' for node in self)

    @property
    def activity(self):
        """The number of updates of each node.
        """
        total = sum(node.updates for node in self)
        individual_updates = '\n'.join(f'{node} {node.updates}' for node in self)
        return f'Total Updates: {total}\n{individual_updates}'

    def poll(self):
        """Add current adjacency list and various meta-data like node activity to results.
        """
        self.results.append(tuple(getattr(self, attr) for attr in _POLL_ATTRS))

    async def _run(self, npolls, delay):
        """Coroutine passed to scheduler's `run`.
        """
        scheduler.run_soon(node.update_forever() for node in self)

        for _ in range(npolls):
            await scheduler.sleep(delay)
            self.poll()

    def run(self, npolls, delay):
        """Run the gract, polling every `delay` seconds `npolls` times.
        """
        scheduler.run(self._run(npolls, delay))

    save = analysis.save
