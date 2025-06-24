# from commit_data_service import (
#     request_write_commit,
#     request_get_commit_by_hash,
#     request_print_all_commits,
#     request_is_data_csv_empty,
#     request_get_last_commit_hash
# )
# from commit import Commit
#
# class CommitManager:
#     def __init__(self, path):
#         self.path = path
#
#     def save(self, commit: Commit):
#         request_write_commit(self.path, commit)
#
#     def get_by_hash(self, hash_code: str) -> Commit:
#         return request_get_commit_by_hash(self.path, hash_code)
#
#     def get_last_hash(self) -> str:
#         return request_get_last_commit_hash(self.path)
#
#     def print_all(self):
#         request_print_all_commits(self.path)
#
#     def is_empty(self) -> bool:
#         return request_is_data_csv_empty(self.path)




# commit_manager.py
from commit import Commit
from commit_data_service import CommitDataService

class CommitManager:
    def __init__(self, path: str):
        self.path = path
        self.data_service = CommitDataService(path)

    def save(self, message: str) -> Commit:
        commit = Commit(message)
        self.data_service.save_commit(commit)
        return commit

    def get_by_hash(self, hash_code: str) -> Commit | None:
        return self.data_service.fetch_commit_by_hash(hash_code)

    def get_last_commit(self) -> Commit | None:
        return self.data_service.fetch_last_commit()

    def get_last_hash(self) -> str | None:
        last_commit = self.get_last_commit()
        return last_commit.hash_code if last_commit else None

    def is_empty(self) -> bool:
        return self.data_service.is_empty()

    def print_all(self):
        for commit in self.data_service.fetch_all_commits():
            print(commit)

