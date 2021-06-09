from time import strftime
from pathlib import Path

import networkx as nx

from .histogram import save_histogram
from .visualization import save_visualization

RESULTS = 'results'
HISTOGRAMS = 'histograms'
VISUALS = 'visuals'

def save(gract, *, histograms=True, visualizations=True):
    root = Path() / RESULTS / strftime('%m_%d_%y__%H_%M_%S')
    root.mkdir()

    histogram_path = root / HISTOGRAMS
    visualization_path = root / VISUALS

    if histograms:
        histogram_path.mkdir()

    if visualizations:
        visualization_path.mkdir()

    for i, (adjlist, updates) in enumerate(gract.results):
        adjlist_path = root / f'{i}.adjlist'
        adjlist_path.write_text(adjlist)

        updates_path = root / f'{i}.activity'
        updates_path.write_text(updates)

        if histograms or visualizations:
            g = nx.read_adjlist(adjlist_path, create_using=nx.MultiDiGraph, nodetype=int)

            if histograms:
                save_histogram(g, histogram_path / f'{i}.png')

            if visualizations:
                save_visualization(g, visualization_path / f'{i}.png')
