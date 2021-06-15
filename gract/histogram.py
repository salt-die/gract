"""
Real-time degree histogram display.

Current implementation plan:
    Create an inheritable neighbors behavior, say, UpdateHistogramBehavior. When `realtime_histogram=True`
    argument is passed to a gract, a new neighbors type will be created using the passed node type and this
    behavior. Every update interval the histogram will be re-printed.

Issues to solve:
    * Bins need to be calculated automatically and shouldn't change too much. Consecutive empty bins should be joined.
    * Somehow not overwrite the progress bar.  This may require some changes to the progress bar.
    * Don't want to use curses, just stdout.

"""
from .scheduler import sleep

UP = '\x1b[{}A'

def cursor_up(n):
    print(UP.format(n), end='\r')


class UpdateHistogramBehavior:
    """Mix-in for neighbors types that updates a histogram when the neighbors change.
    """
    def __init__(self, histogram, neighbor=()):
        self.histogram = histogram
        super().__init__(neighbors)

    def add(self, neighbor):
        old = len(self)
        super().add(neighbor):
        self.histogram.dispatch(old, len(self))

    def discard(self, neighbor):
        old = len(self)
        super().discard(neighbors)
        self.histogram.dispatch(old, len(self))

    def pop(self):
        old = len(self)
        neighbor = super().pop()
        self.histogram.dispatch(old, len(self))
        return neighbor


class RealTimeHistogram:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.closed = False

    async def update(self, interval):
        while True:
            self.display()
            sleep(interval)

            if self.closed:
                break

    def close(self):
        self.closed = True

    def display(self):
        raise NotImplementedError

    def dispatch(self, old, new):
        raise NotImplementedError
