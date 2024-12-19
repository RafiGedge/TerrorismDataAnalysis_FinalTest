import time
from typing import Callable
from functools import wraps


def measure_time(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        execution_time = (end_time - start_time)
        print(f"\nrunning function - {func.__name__}: {execution_time}")
        return result

    return wrapper


def measure_block_time():
    class TimerContextManager:
        def __enter__(self):
            self.start = time.perf_counter()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.end = time.perf_counter()
            execution_time = (self.end - self.start)
            print(f"\nrunning time: {execution_time}")

    return TimerContextManager()

# @measure_time
# with measure_block_time():