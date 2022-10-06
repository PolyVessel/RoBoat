import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    """Limits function to seconds in parameter
    
    Example:

    try:
        with time_limit(10):
            long_function_call()
    except TimeoutException as e:
        print("Timed out!")"""

    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
