from time import strftime
from pathlib import Path

import networkx as nx  # MAYBE: Defer this import until needed.

from .histogram import save_histogram
from .visualization import save_visualization

ROOT = Path(__file__).parent.parent.parent
RESULTS = 'results'
HISTOGRAMS = 'histograms'
VISUALS = 'visuals'

def save(gract, **kwargs):
    """
    Save polled adajacency lists of a gract.


    Optional Parameters
    -------------------
    activity: bool
        Save node activity if true. (default: False)

    metadata: bool
        Save node metadata if true. (default: False)

    histograms: bool
        Save degree histograms if true. (default: False)

    visualizations: bool
        Save graph visualizations if true. (default: False)

    """
    results = ROOT / RESULTS / strftime('%m_%d_%y__%H_%M_%S')
    results.mkdir()

    histogram_path = results / HISTOGRAMS
    visualization_path = results / VISUALS

    if histograms := kwargs.get('histograms'):
        histogram_path.mkdir()

    if visualizations := kwargs.get('visualizations'):
        visualization_path.mkdir()

    for i, (adjlist, activity, meta_data) in enumerate(gract.results):
        adjlist_path = results / f'{i}.adjlist'
        adjlist_path.write_text(adjlist)

        if kwargs.get('activity'):
            activity_path = results / f'{i}.activity'
            activity_path.write_text(activity)

        if kwargs.get('metadata'):
            metadata_path = results / f'{i}.metadata'
            metadata_path.write_text(meta_data)

        if histograms or visualizations:
            g = nx.read_adjlist(adjlist_path, create_using=nx.MultiDiGraph, nodetype=int)

            if histograms:
                save_histogram(g, histogram_path / f'{i}.png')

            if visualizations:
                save_visualization(g, visualization_path / f'{i}.png')
