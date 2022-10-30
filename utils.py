import time
from functools import wraps
import logging as log

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        log.debug(f'{func.__qualname__} execution time: {_to_ms(end - start)} ms')
        return result

    return wrapper

def _to_ms(seconds: int) -> float:
    return seconds * 1000
