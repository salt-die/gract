from contextlib import contextmanager
from itertools import cycle
from time import monotonic
from .scheduler import run_soon, sleep

UPDATE_INTERVAL = .1
BAR_LENGTH = 75
SPINNER = cycle("___-`''´-___")
PARTIAL_FILL = ' ▏▎▍▌▋▊▉█'

async def _progress_bar(duration):
    """
    A time-based asynchronous progress bar.


    Parameters
    ----------
    duration: float
        Total duration of progress bar.

    """
    start_time = monotonic()
    end_time = start_time + duration

    while (current_time := monotonic()) < end_time:
        elapsed_time = current_time - start_time
        percent = elapsed_time / duration

        filled_length = BAR_LENGTH * percent
        partial_fill = PARTIAL_FILL[int((filled_length % 1) * 9)]
        flip = next(SPINNER) if max(0, BAR_LENGTH - filled_length - 1) else ''

        bar = f'{"█" * int(filled_length)}{partial_fill}{flip}'.ljust(BAR_LENGTH, '_')

        progress = ' | '.join((
            bar,
            f'Completed: {percent * 100:>5.1f}%',
            f'Time Elapsed: {elapsed_time:>5.1f}s',
            f'Time Left: {duration - elapsed_time:>5.1f}s',
        ))
        print(progress, end='\r')

        await sleep(UPDATE_INTERVAL)

@contextmanager
def progress_bar(duration):
    """Progress bar context manager. Schedule progress bar on enter and clean up stdout on exit.
    """
    try:
        run_soon(_progress_bar(duration))
        yield
    finally:
        print()
