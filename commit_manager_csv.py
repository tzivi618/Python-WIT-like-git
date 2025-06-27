from commit import Commit
from commit_data_csv import CommitDataCSV

class CommitManager:
    """
    Handles commit operations: saving, retrieving, and listing commits.
    """

    def __init__(self, path: str):
        self.path = path
        self.data = CommitDataCSV(path)

    def save(self, message: str) -> Commit:
        """Creates and stores a new commit with the given message."""
        commit = Commit(message)
        self.data.write(commit)
        return commit

    def get_by_hash(self, hash_code: str) -> Commit | None:
        """Returns the commit matching the given hash, if exists."""
        return self.data.read_by_hash(hash_code)

    def get_last_commit(self) -> Commit | None:
        """Returns the most recent commit."""
        return self.data.read_last()

    def get_last_hash(self) -> str | None:
        """Returns the hash of the last commit."""
        last = self.get_last_commit()
        return last.hash_code if last else None

    def is_empty(self) -> bool:
        """Checks if there are no commits."""
        return self.data.is_empty()

    def print_all(self):
        """Prints all commits."""
        for commit in self.data.read_all():
            print(commit)

    def get_all_commits(self) -> list[Commit]:
        """Returns a list of all commits."""
        return self.data.read_all()
