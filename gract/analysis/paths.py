from time import asctime, localtime
from pathlib import Path

RESULTS = 'results'
HISTOGRAMS = 'histograms'
VISUALS = 'visuals'

def get_paths():
    root = Path() / RESULTS / asctime(localtime()).replace(' ', '_').replace(':', '_')
    histograms = root / HISTOGRAMS
    visuals = root / VISUALS

    return root, histograms, visuals
