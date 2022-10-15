import inject
import time
from datetime import datetime
from functools import wraps
import logging as log

from config import Config

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end = time.perf_counter_ns()
        log.debug(f'{func.__qualname__} execution time: {_to_ms(end - start)} ms')
        return result

    return wrapper

def _to_ms(ns: int) -> float:
    return ns / 1E6
