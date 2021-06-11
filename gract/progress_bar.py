from contextlib import contextmanager
from itertools import cycle
import os
from time import monotonic
from .scheduler import run_soon, sleep

UPDATE_INTERVAL = .1
SPINNER = cycle("___-`''´-___")
FILL = '█'
PARTIAL_FILL = ' ▏▎▍▌▋▊▉█'

async def _progress_bar(duration):
    """An asynchronous progress bar that tracks time for `duration` seconds.
    """
    bar_length = min(75, os.get_terminal_size()[0] - 58)  # 58 is length of non-bar characters printed.

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

        fill, partial = divmod(bar_length * percent, 1)
        filled_length, partial_index = int(fill), int(len(PARTIAL_FILL) * partial)

        partial_fill = PARTIAL_FILL[partial_index]

        bar = f'{FILL * filled_length}{partial_fill}{next(SPINNER)}'.ljust(bar_length, '_')[:bar_length]

        print(
            ' | '.join((
                f'[{bar}] {100 * percent:>5.1f}%',
                f'Time Elapsed: {elapsed_time:>5.1f}s',
                f'Time Remaining: {duration - elapsed_time:>5.1f}s',
            )),
            end='\r'
        )

        await sleep(UPDATE_INTERVAL)

@contextmanager
def progress_bar(duration):
    """Progress bar context manager.
    """
    run_soon(_progress_bar(duration))
    print('\x1b[?25l', end='') # Hide cursor

    try:
        yield
    finally:
        print('\x1b[?25h') # Show cursor and print newline.
