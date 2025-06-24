import os, csv
from commit import Commit
from file_manager import wit_subfolder

class CommitDataCSV:
    """Handles reading and writing commit metadata to a CSV file."""

    def __init__(self, path: str):
        """Initialize with repository path."""
        self.path = path
        self.csv_path = os.path.join(wit_subfolder(path), "data.csv")

    def write(self, commit: Commit):
        """Append a new commit to the CSV file."""
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        with open(self.csv_path, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([commit.hash_code, commit.message, commit.timestamp])

    def read_all(self) -> list[Commit]:
        """Return all commits from the CSV file."""
        commits = []
        if not os.path.exists(self.csv_path):
            return commits
        with open(self.csv_path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                commits.append(Commit(row[1], row[0], row[2]))
        return commits

    def read_last(self) -> Commit | None:
        """Return the most recent commit, or None if no commits."""
        commits = self.read_all()
        return commits[-1] if commits else None

    def read_by_hash(self, hash_code: str) -> Commit | None:
        """Return a commit by its hash, or None if not found."""
        for c in self.read_all():
            if c.hash_code == hash_code:
                return c
        return None

    def is_empty(self) -> bool:
        """Check if the CSV file has any commits."""
        return not os.path.exists(self.csv_path) or os.stat(self.csv_path).st_size == 0
