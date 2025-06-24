from datetime import datetime
import hashlib

class Commit:
    """A commit object with message, timestamp, and unique hash."""

    def __init__(self, message, hash_code=None, timestamp=None):
        """Initialize commit with message and optional hash/timestamp."""
        self.timestamp = timestamp or datetime.now().isoformat()
        self.message = message
        self.hash_code = hash_code or self._generate_hash()

    def _generate_hash(self):
        """Generate a short SHA-1 hash from timestamp and message."""
        data = f"{self.timestamp}_{self.message}".encode()
        return hashlib.sha1(data).hexdigest()[:10]

    def __str__(self):
        """Return Git-like string representation of the commit."""
        return f"commit {self.hash_code}\nDate:   {self.timestamp}\n\n    {self.message}"
