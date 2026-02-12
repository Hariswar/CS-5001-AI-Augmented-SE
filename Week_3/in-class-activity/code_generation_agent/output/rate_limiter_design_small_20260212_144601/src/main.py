import time
from typing import Optional

class RateLimiter:
    """A simple token bucket rate limiter using standard library components."""

    def __init__(self, capacity: float, refill_rate: float) -> None:
        """
        Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens the bucket can hold.
            refill_rate: Number of tokens added per second.

        Raises:
            ValueError: If capacity or refill_rate is not positive.
        """
        if capacity <= 0 or refill_rate <= 0:
            raise ValueError("Capacity and refill_rate must be positive.")
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def _refill_tokens(self) -> None:
        """Refill tokens based on elapsed time since last refill."""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + self.refill_rate * elapsed)
        self.last_refill = now

    def allow(self) -> bool:
        """
        Check if a request is allowed.

        Returns:
            bool: True if a token is available, False otherwise.
        """
        self._refill_tokens()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def __enter__(self) -> "RateLimiter":
        """Support for context manager protocol (no-op)."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> Optional[bool]:
        """Support for context manager protocol (no-op)."""
        return None

def main() -> None:
    """Demonstrate the rate limiter with example usage."""
    limiter = RateLimiter(capacity=3, refill_rate=1)

    print("Testing rate limiter with capacity=3 and refill_rate=1 per second.")
    print("Attempting 5 requests in quick succession:")

    for i in range(5):
        if limiter.allow():
            print(f"Request {i + 1}: Allowed")
        else:
            print(f"Request {i + 1}: Blocked")

    print("\nWaiting 2 seconds to refill tokens...")
    time.sleep(2)

    print("Attempting 2 more requests after waiting:")
    for i in range(2):
        if limiter.allow():
            print(f"Request {i + 3}: Allowed")
        else:
            print(f"Request {i + 3}: Blocked")

if __name__ == "__main__":
    main()
