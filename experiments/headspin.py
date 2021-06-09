from gract import Gract
from gract.node_types import HeadSpin

gract = Gract.random_graph(node_types=HeadSpin, nnodes=1000, degree=5)
gract.run(npolls=3, delay=10)
gract.save(activity=True, histograms=True, visualizations=True)
