from request_manager import (
    request_write_commit,
    request_get_commit_by_hash,
    request_print_all_commits,
    request_is_data_csv_empty,
    request_get_last_commit_hash
)
from commit import Commit

class CommitManager:
    def __init__(self, path):
        self.path = path

    def save(self, commit: Commit):
        request_write_commit(self.path, commit)

    def get_by_hash(self, hash_code: str) -> Commit:
        return request_get_commit_by_hash(self.path, hash_code)

    def get_last_hash(self) -> str:
        return request_get_last_commit_hash(self.path)

    def print_all(self):
        request_print_all_commits(self.path)

    def is_empty(self) -> bool:
        return request_is_data_csv_empty(self.path)
