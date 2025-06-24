from commit import Commit
from commit_data_csv import CommitDataCSV

class CommitManager:
    def __init__(self, path: str):
        self.path = path
        self.data = CommitDataCSV(path)

    def save(self, message: str) -> Commit:
        commit = Commit(message)
        self.data.write(commit)
        return commit

    def get_by_hash(self, hash_code: str) -> Commit | None:
        return self.data.read_by_hash(hash_code)

    def get_last_commit(self) -> Commit | None:
        return self.data.read_last()

    def get_last_hash(self) -> str | None:
        last = self.get_last_commit()
        return last.hash_code if last else None

    def is_empty(self) -> bool:
        return self.data.is_empty()

    def print_all(self):
        for commit in self.data.read_all():
            print(commit)
