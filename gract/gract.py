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
        """The current adjacency list of the graph in a string format readable by networkx (and also by humans).
        """
        return '\n'.join(f'{node} {" ".join(map(str, node.neighbors))}' for node in self)

    @property
    def activity(self):
        """The activity each node in a human-readable string format.
        """
        total = sum(node.activity for node in self)
        individual = '\n'.join(f'{node} {node.activity}' for node in self)
        return f'Total Activity: {total}\n{individual}'

    @property
    def metadata(self):
        """Meta-data of each node in a human-readable string format.
        """
        return '\n'.join(f'{node} {node.metadata}' for node in self)

    def poll(self):
        """Add current adjacency list, activity, and node meta-data to results.
        """
        self.results.append((self.nx_adjlist, self.activity, self.metadata))

    async def _run(self, npolls, delay):
        """Coroutine passed to scheduler's `run`.
        """
        scheduler.run_soon(node.update_forever() for node in self)

        for _ in range(npolls):
            await scheduler.sleep(delay)
            self.poll()

    def run(self, duration, npolls):
        """Run the gract for `duration` seconds, polling `npolls` times.
        """
        npolls = max(1, npolls)
        scheduler.run(self._run(npolls, duration / npolls))

    save = analysis.save
