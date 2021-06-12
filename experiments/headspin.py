from gract import Gract
from gract.node_types import HeadSpinNode

gract = Gract.random_graph(node_types=HeadSpinNode, nnodes=1000, degree=5)
gract.run(duration=30, npolls=3)
gract.save(activity=True, histograms=True)
