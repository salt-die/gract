"""
Warning
-------
This is a rough-draft of a gract implementation.

"""
from .analysis import save
from .gract import Gract
from .node_types import HeadSpin

# Run experiment
gract = Gract.random_graph(HeadSpin, nnodes=1000, degree=5)
nx_adjlists = gract.run(delay=10, npolls=3)

# TODO: Probably makes sense to just add analysis tools as methods of Gract.
# Alternatively, save polling results in the Gract instance and pass the Gract to the analysis tools.

# Save results
save(nx_adjlists, histograms=True, visualizations=True)
