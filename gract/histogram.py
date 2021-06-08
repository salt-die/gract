from itertools import chain
from pathlib import Path

import networkx as nx
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def save_histogram(g: nx.DiGraph, path: Path):
    out_degrees = [ d for _, d in g.out_degree() ]
    in_degrees = [ d for _, d in g.in_degree() ]

    smallest = min(chain(out_degrees, in_degrees))
    largest = max(chain(out_degrees, in_degrees)) + 1
    bins = range(smallest, largest)

    plt.title('Degree Histogram')
    plt.hist(out_degrees, bins, alpha=0.5, color='red', label='out')
    plt.hist(in_degrees, bins, alpha=0.5, color='blue', label='in')
    plt.legend()
    plt.savefig(path, bbox_inches='tight')
    plt.clf()  # Clear figure
