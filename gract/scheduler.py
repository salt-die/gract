"""
Originally built on top of asyncio, but `gract` is currently experimenting with a much trimmer event loop.

Warning
-------
No task-wrapping of coroutines and event-loop ends as soon as a coroutine raises StopIteration.

"""
from collections import deque
from collections.abc import Iterable
from heapq import heappop, heappush
from itertools import count
from time import monotonic

_EVENT_LOOP_STARTED = False
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
            for coro in coros:
                self.ready.append(coro)
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
                break

            if self.current is not None:
                ready.append(self.current)

        _destroy_event_loop()


def _destroy_event_loop():
    global _EVENT_LOOP_STARTED, _CURRENT_EVENT_LOOP

    _EVENT_LOOP_STARTED = False
    _CURRENT_EVENT_LOOP = None

########################
### Public Functions ###
########################

def run_soon(coros):
    """Schedule the given coroutines to run immediately.
    """
    global _CURRENT_EVENT_LOOP

    if _CURRENT_EVENT_LOOP is None:
        _CURRENT_EVENT_LOOP = _Scheduler()

    _CURRENT_EVENT_LOOP.run_soon(coros)

def run(coro):
    """Start the event loop.
    """
    global _EVENT_LOOP_STARTED, _CURRENT_EVENT_LOOP

    if _EVENT_LOOP_STARTED:
        raise RuntimeError('an event loop is already running')

    if _CURRENT_EVENT_LOOP is None:
        _CURRENT_EVENT_LOOP = _Scheduler()

    _EVENT_LOOP_STARTED = True
    _CURRENT_EVENT_LOOP.run(coro)

async def sleep(delay):
    if not _EVENT_LOOP_STARTED:
        raise RuntimeError('no running event loop')

    await _CURRENT_EVENT_LOOP.sleep(delay)
