from time import asctime, localtime
from pathlib import Path

RESULTS = 'results'
HISTOGRAMS = 'histograms'
VISUALS = 'visuals'

def get_paths():
    root = Path() / RESULTS / asctime(localtime()).replace(' ', '_').replace(':', '_')
    root.mkdir()

    histograms = root / HISTOGRAMS
    histograms.mkdir()

    visuals = root / VISUALS
    visuals.mkdir()

    return root, histograms, visuals
