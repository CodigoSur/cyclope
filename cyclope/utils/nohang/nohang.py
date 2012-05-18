"""
nohang module provides a way to ensure that a function that could block get's
interrupted if it hangs more time that it should.
nohang does *not* support threading.
"""
import signal
import threading
import warnings

class TimeExpired(Exception):
    pass

_in_main_thread = isinstance(threading.current_thread(), threading._MainThread)
if not _in_main_thread:
   warnings.warn("nohang is running in a thread so it will not work", RuntimeWarning)


def run(function, args=None, kwargs=None, wait=None):
    """
    function gets called with args and kwargs and returns a tuple with the result
    and success. If function doesn't return in less than wait, in seconds (float),
    it's excecution is interrupted and the return value is (None, False).
    """

    if args is None:
        args = tuple()
    if kwargs is None:
        kwargs = dict()
    try:
        wait = float(wait)
    except:
        raise TypeError("wait argument should be a float")

    if _in_main_thread:
        signal.signal(signal.SIGALRM, _timer_handler)
        signal.setitimer(signal.ITIMER_REAL, wait)

    result, success = None, True
    try:
        result = function(*args, **kwargs)
    except TimeExpired:
        success = False

    if _in_main_thread:
        signal.setitimer(signal.ITIMER_REAL, 0) # Cancel the timer

    return result, success


def _timer_handler(signum, frame):
    raise TimeExpired



