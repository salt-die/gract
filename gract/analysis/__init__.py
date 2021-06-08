import networkx as nx

from .histogram import save_histogram
from .paths import get_paths
from .visualization import save_visualization

def save(nx_adjlists, *, histograms=True, visualizations=True):
    root, histogram_path, visualization_path = get_paths()
    root.mkdir()

    if histograms:
        histogram_path.mkdir()

    if visualizations:
        visualization_path.mkdir()

    for i, adjlist in enumerate(nx_adjlists):
        adjlist_path = root / f'{i}.adjlist'
        adjlist_path.write_text(adjlist)

        if histograms or visualizations:
            g = nx.read_adjlist(adjlist_path, create_using=nx.MultiDiGraph, nodetype=int)

            if histograms:
                save_histogram(g, histogram_path / f'{i}.png')

            if visualizations:
                save_visualization(g, visualization_path / f'{i}.png')
