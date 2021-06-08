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


class _NextTask:
    __slots__ = ()

    def __await__(self):
        yield


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
        await _NextTask()

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

            if ready:
                self.current = ready.popleft()
            else:
                continue

            try:
                self.current.send(None)
            except StopIteration as e:
                return e.value
            else:
                if self.current is not None:
                    ready.append(self.current)

        _destroy_event_loop()


EVENT_LOOP_STARTED = False
CURRENT_EVENT_LOOP = None

def _destroy_event_loop():
    global EVENT_LOOP_STARTED, CURRENT_EVENT_LOOP
    EVENT_LOOP_STARTED = False
    CURRENT_EVENT_LOOP = None

########################
### Public Functions ###
########################

def run_soon(coros):
    """Schedule the given coroutines to run immediately.
    """
    global CURRENT_EVENT_LOOP
    if CURRENT_EVENT_LOOP is None:
        CURRENT_EVENT_LOOP = _Scheduler()

    CURRENT_EVENT_LOOP.run_soon(coros)

def run(coro):
    """Start the event loop.
    """
    global EVENT_LOOP_STARTED, CURRENT_EVENT_LOOP

    if EVENT_LOOP_STARTED:
        raise RuntimeError('an event loop is already running')

    if CURRENT_EVENT_LOOP is None:
        CURRENT_EVENT_LOOP = _Scheduler()

    EVENT_LOOP_STARTED = True
    return CURRENT_EVENT_LOOP.run(coro)

async def sleep(delay):
    if not EVENT_LOOP_STARTED:
        raise RuntimeError('no running event loop')

    await CURRENT_EVENT_LOOP.sleep(delay)
