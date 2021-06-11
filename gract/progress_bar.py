from contextlib import contextmanager
from itertools import cycle
from time import monotonic
from .scheduler import run_soon, sleep

UPDATE_INTERVAL = .1
BAR_LENGTH = 75
SPINNER = cycle("___-`''´-___")
FILL = '█'
PARTIAL_FILL = ' ▏▎▍▌▋▊▉█'

async def _progress_bar(duration):
    """
    A time-based asynchronous progress bar.


    Parameters
    ----------
    duration: float
        Total duration of progress bar.

    """
    start_time = current_time = monotonic()
    end_time = start_time + duration

    while current_time < end_time:
        current_time = monotonic()

        if end_time - current_time < UPDATE_INTERVAL:
            current_time = end_time
            elapsed_time = duration
            percent = 1
        else:
            elapsed_time = current_time - start_time
            percent = elapsed_time / duration

        fill, partial = divmod(BAR_LENGTH * percent, 1)
        filled_length, partial_index = int(fill), int(len(PARTIAL_FILL) * partial)

        partial_fill = PARTIAL_FILL[partial_index]

        bar = f'{FILL * filled_length}{partial_fill}{next(SPINNER)}'.ljust(BAR_LENGTH, '_')[:BAR_LENGTH]

        print(
            ' | '.join((
                bar,
                f'Completed: {100 * percent:>5.1f}%',
                f'Time Elapsed: {elapsed_time:>5.1f}s',
                f'Time Left: {duration - elapsed_time:>5.1f}s',
            )),
            end='\r'
        )

        await sleep(UPDATE_INTERVAL)

@contextmanager
def progress_bar(duration):
    """Progress bar context manager. Schedule progress bar on enter and clean up stdout on exit.
    """
    run_soon(_progress_bar(duration))

    try:
        yield
    finally:
        print()
