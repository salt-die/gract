from pathlib import Path

import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

def save_visualization(g: nx.DiGraph, path: Path):
    layout = nx.spring_layout(g, k=.1, iterations=100, threshold=1e-5)
    cmap = plt.cm.plasma

    node_colors = [d for _, d in g.in_degree()]
    nx.draw_networkx_nodes(g, layout, node_size=3, node_color=node_colors, cmap=cmap)

    edge_colors = [g.out_degree(u) for u, v in g.edges()]
    nx.draw_networkx_edges(g, layout, node_size=3, width=.5, edge_color=edge_colors, edge_cmap=cmap)

    plt.savefig(path, bbox_inches='tight')
    plt.clf()  # Clear figure
