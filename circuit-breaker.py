import time
from enum import Enum

# Using an Enum makes the code readable and prevents "string typos"
class State(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10):
        self.failure_threshold = failure_threshold # How many fails before it trips
        self.recovery_timeout = recovery_timeout   # How long to wait in seconds
        
        # Initial State
        self.state = State.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        """
        The 'Brain' of the project. It decides whether to execute 
        the function or block it.
        """
        # 1. Logic: If OPEN, check if enough time has passed to try again
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                print("--- ⏱ Cooldown over. Switching to HALF-OPEN ---")
                self.state = State.HALF_OPEN
            else:
                # If still in cooldown, don't even TRY the function
                raise Exception("Circuit is OPEN. Request blocked to save resources.")

        # 2. Execution: Try to run the third-party call
        try:
            result = func(*args, **kwargs)
            self._handle_success()
            return result
        except Exception as e:
            self._handle_failure()
            raise e

    def _handle_success(self):
        if self.state == State.HALF_OPEN:
            print("--- ✅ Success! System recovered. Closing circuit. ---")
        self.state = State.CLOSED
        self.failure_count = 0

    def _handle_failure(self):
        self.failure_count += 1
        print(f"--- ❌ Failure {self.failure_count}/{self.failure_threshold} ---")
        
        if self.failure_count >= self.failure_threshold:
            print("--- 🔥 CRITICAL FAILURE: Tripping Circuit to OPEN ---")
            self.state = State.OPEN
            self.last_failure_time = time.time()