# import requests
# from commit import Commit
#
# URL = 'http://localhost:8000'
#
# def request_write_commit(path, commit):
#     data = {
#         "path": str(path),
#         "hash_code": commit.hash_code,
#         "message": commit.message,
#         "timestamp": commit.timestamp
#     }
#     try:
#         response = requests.post(f"{URL}/commits", json=data)
#         if response.status_code != 200:
#             print(f"Error writing to DB: {response.text}")
#     except Exception as e:
#         print(f"Error writing to DB: {e}")
#
# def request_get_commit_by_hash(path, hash_code):
#     params = {"path": str(path), "hash_code": hash_code}
#     try:
#         response = requests.get(f"{URL}/commits/row", params=params)
#         if response.status_code == 200:
#             row = response.json().get("row")
#             if row:
#                 return Commit(row["message"], row["hash_code"], row["timestamp"])
#         else:
#             print(f"Error reading row: {response.text}")
#     except Exception as e:
#         print(f"Error reading row: {e}")
#     return None
#
# def request_print_all_commits(path):
#     params = {"path": str(path)}
#     try:
#         response = requests.get(f"{URL}/commits/all", params=params)
#         if response.status_code == 200:
#             rows = response.json().get("rows", [])
#             for row in rows:
#                 c = Commit(row["message"], row["hash_code"], row["timestamp"])
#                 print(c)
#         else:
#             print(f"Error reading all rows: {response.text}")
#     except Exception as e:
#         print(f"Error reading all rows: {e}")
#
# def request_is_data_csv_empty(path):
#     params = {"path": str(path)}
#     try:
#         response = requests.get(f"{URL}/commits/is_empty", params=params)
#         if response.status_code == 200:
#             return response.json().get("is_empty", False)
#         else:
#             print(f"Error checking if empty: {response.text}")
#     except Exception as e:
#         print(f"Error checking if empty: {e}")
#     return False
#
# def request_get_last_commit_hash(path):
#     params = {"path": str(path)}
#     try:
#         response = requests.get(f"{URL}/commits/last", params=params)
#         if response.status_code == 200:
#             return response.json().get("hash_code")
#         else:
#             print(f"Error getting last hash: {response.text}")
#     except Exception as e:
#         print(f"Error getting last hash: {e}")
#     return None




# commit_data_service.py
import requests
from commit import Commit

class CommitDataService:
    BASE_URL = "http://localhost:8000"

    def __init__(self, path):
        self.path = str(path)

    def save(self, commit: Commit):
        data = commit.to_dict()
        data["path"] = self.path
        try:
            requests.post(f"{self.BASE_URL}/commits", json=data)
        except Exception as e:
            print(f"Error writing to DB: {e}")

    def get_by_hash(self, hash_code: str) -> Commit | None:
        try:
            res = requests.get(f"{self.BASE_URL}/commits/row", params={
                "path": self.path,
                "hash_code": hash_code
            })
            if res.status_code == 200:
                row = res.json().get("row")
                if row:
                    return Commit.from_dict(row)
        except Exception as e:
            print(f"Error getting commit: {e}")
        return None

    def get_all(self) -> list[Commit]:
        commits = []
        try:
            res = requests.get(f"{self.BASE_URL}/commits/all", params={"path": self.path})
            for row in res.json().get("rows", []):
                commits.append(Commit.from_dict(row))
        except Exception as e:
            print(f"Error listing commits: {e}")
        return commits

    def is_empty(self) -> bool:
        try:
            res = requests.get(f"{self.BASE_URL}/commits/is_empty", params={"path": self.path})
            return res.json().get("is_empty", False)
        except:
            return False

    def get_last_hash(self) -> str | None:
        try:
            res = requests.get(f"{self.BASE_URL}/commits/last", params={"path": self.path})
            return res.json().get("hash_code")
        except:
            return None
