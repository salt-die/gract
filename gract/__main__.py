import networkx as nx

from .gract import Gract
from .histogram import save_histogram
from .nodes import HeadSpin
from .neighbors import RandomNeighbors
from .scheduler import run, sleep
from .visual import save_visual
from .paths import get_paths

async def main(nnodes, degree, delay, n):
    g = Gract.random_graph(HeadSpin, RandomNeighbors, degree, nnodes)
    g.run()

    adj_lists = [ ]
    for _ in range(n):
        await sleep(delay)
        adj_lists.append(g.adjacency)

    return adj_lists

# Run experiment
graphs = run(main(nnodes=1000, degree=5, delay=10, n=3))

# Save graphs, histograms, and visualizations.
root, histograms, visuals = get_paths()
for i, graph in enumerate(graphs):
    with open(root / f'{i}.adjlist', 'w') as adjlist:
        adjlist.write(graph)

    g = nx.read_adjlist(root / f'{i}.adjlist', create_using=nx.MultiDiGraph)
    save_histogram(g, histograms / f'{i}.png')
    save_visual(g, visuals / f'{i}.png')
