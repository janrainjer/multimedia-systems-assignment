import time


class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None

    def start(self):
        """Start the timer."""
        self.start_time = time.perf_counter()

    def stop(self):
        """Stop the timer and calculate the elapsed time."""
        if self.start_time is not None:
            self.end_time = time.perf_counter()
            self.elapsed_time = self.end_time - self.start_time
            self.start_time = None
            self.end_time = None
            return self.elapsed_time
        else:
            return None

    def print_elapsed_time(self):
        """Print the elapsed time."""
        elapsed_time = self.stop()
        if elapsed_time is not None:
            print(f"Elapsed time: {elapsed_time:.2f} seconds")
        else:
            print("Timer was not started.")