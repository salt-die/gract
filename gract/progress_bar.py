from itertools import cycle
from time import monotonic
from .scheduler import sleep

async def progress_bar(duration, *, update_interval=.1, length=75):
    """
    A time-based asynchronous progress bar.


    Parameters
    ----------
    duration: float
        Total duration of progress bar.

    update_interval: float
        Seconds until bar is updated. (default: .1)

    length: int
        Length of progress bar. (default: 75)

    """
    spinner = cycle("___-`''´-___")
    fill = ' ▏▎▍▌▋▊▉█'

    start_time = monotonic()
    end_time = start_time + duration

    while (current_time := monotonic()) < end_time:
        elapsed_time = current_time - start_time
        percent = elapsed_time / duration

        filled = length * percent
        partial = fill[int((filled % 1) * 9)]
        flip = next(spinner) if max(0, length - filled - 1) else ''

        bar = f'{"█" * int(filled)}{partial}{flip}'.ljust(length, '_')

        progress_bar = ' | '.join((
            bar,
            f'Completed: {percent * 100:>5.1f}%',
            f'Time Elapsed: {elapsed_time:>5.1f}s',
            f'Time Left: {duration - elapsed_time:>5.1f}s',
        ))
        print(progress_bar, end='\r')

        await sleep(update_interval)
