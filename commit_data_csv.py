import os,csv
from commit import Commit
from file_manager import wit_subfolder

class CommitDataCSV:
    def __init__(self, path: str):
        self.path = path
        self.csv_path = os.path.join(wit_subfolder(path), "data.csv")

    def write(self, commit: Commit):
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        with open(self.csv_path, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([commit.hash_code, commit.message, commit.timestamp])

    def read_all(self) -> list[Commit]:
        commits = []
        if not os.path.exists(self.csv_path):
            return commits
        with open(self.csv_path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                commits.append(Commit(row[1], row[0], row[2]))
        return commits

    def read_last(self) -> Commit | None:
        commits = self.read_all()
        return commits[-1] if commits else None

    def read_by_hash(self, hash_code: str) -> Commit | None:
        for c in self.read_all():
            if c.hash_code == hash_code:
                return c
        return None

    def is_empty(self) -> bool:
        return not os.path.exists(self.csv_path) or os.stat(self.csv_path).st_size == 0
