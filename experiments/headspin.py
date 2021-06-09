from gract import Gract
from gract.node_types import HeadSpin

# Run experiment
gract = Gract.random_graph(node_types=HeadSpin, nnodes=1000, degree=5)

# gract.run(npolls=3, delay=10) is more efficient, but we're checking that the event-loop is properly destroyed and re-init after each run.
gract.run(npolls=1, delay=10)
print('Polled once')

gract.run(npolls=1, delay=10)
print('Polled twice')

gract.run(npolls=1, delay=10)
print('Polled thrice')

print('Saving...')
gract.save(histograms=True, visualizations=True)
