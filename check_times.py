import time


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
