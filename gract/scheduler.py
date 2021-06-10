"""
Originally built on top of asyncio, but `gract` is currently experimenting with a much trimmer (and faster) event loop.
To this end, coroutines are not wrapped in Tasks.  When a coroutine is finished running it is discarded along with any
return value(s) it may have had.

`stop` can be used to end the current event loop before all coroutines finish.

"""
from collections import deque
from collections.abc import Iterable
from heapq import heappop, heappush
from itertools import count
from time import monotonic

_CURRENT_EVENT_LOOP = None


class _Yield:
    """Primitive awaitable.
    """
    __slots__ = ()

    def __await__(self):
        yield

_YIELD = _Yield()


class _Scheduler:
    __slots__ = 'ready', 'sleeping', 'tiebreaker', 'current',

    def __init__(self):
        self.ready = deque()
        self.sleeping = [ ]
        self.tiebreaker = count()
        self.current = None

    async def sleep(self, delay):
        if delay == 0:
            self.ready.append(self.current)
        else:
            deadline = monotonic() + delay
            tiebreak = next(self.tiebreaker)
            heappush(self.sleeping, (deadline, tiebreak, self.current))

        self.current = None
        await _YIELD

    def run_soon(self, coros):
        """Schedule the given coroutine or coroutines to run immediately.
        """
        if isinstance(coros, Iterable):
            self.ready.extend(coros)
        else:
            self.ready.append(coros)

    def run(self, coro):
        """Start the event loop.
        """
        ready = self.ready
        ready.append(coro)

        sleeping = self.sleeping

        while ready or sleeping:
            while sleeping and sleeping[0][0] <= monotonic():
                ready.append(heappop(sleeping)[-1])

            if not ready:
                continue

            self.current = ready.popleft()

            try:
                self.current.send(None)
            except StopIteration:
                pass

            if self.current is not None:
                ready.append(self.current)

        _destroy_event_loop()

    def stop(self):
        """Discard all coroutines, ending the event loop.
        """
        self.current = None
        self.ready.clear()
        self.sleeping.clear()


def _destroy_event_loop():
    global _CURRENT_EVENT_LOOP
    _CURRENT_EVENT_LOOP = None

########################
### Public Functions ###
########################

def run(coro):
    """Run the coroutine.
    """
    global _CURRENT_EVENT_LOOP

    if _CURRENT_EVENT_LOOP is not None:
        raise RuntimeError('an event loop is already running')

    _CURRENT_EVENT_LOOP = _Scheduler()
    _CURRENT_EVENT_LOOP.run(coro)

def run_soon(coros):
    """Schedule the given coroutine(s) to run immediately.
    """
    if _CURRENT_EVENT_LOOP is None:
        raise RuntimeError('no running event loop')

    _CURRENT_EVENT_LOOP.run_soon(coros)

async def sleep(delay):
    """Coroutine that completes after `delay` seconds.
    """
    if _CURRENT_EVENT_LOOP is None:
        raise RuntimeError('no running event loop')

    await _CURRENT_EVENT_LOOP.sleep(delay)

def stop():
    """Stop current event loop.
    """
    if _CURRENT_EVENT_LOOP is None:
        raise RuntimeError('no running event loop')

    _CURRENT_EVENT_LOOP.stop()
