# # commit.py
# from datetime import datetime
# import hashlib
# class Commit:
#     def __init__(self, message, hash_code=None, date_time=None):
#         self.date_time = date_time if date_time else datetime.now().isoformat()
#         self.message = message
#         if hash_code:
#             self.hash_code = hash_code
#         else:
#             hash_input = f"{self.date_time}_{self.message}".encode('utf-8')
#             self.hash_code = hashlib.sha1(hash_input).hexdigest()[:10]
#
#     def __str__(self):
#         return f"ID: {self.hash_code}\tMessage: {self.message}\tDate: {self.date_time}"
#
#     def get_list_value(self):
#         return [self.hash_code, self.message, self.date_time]


#
# #commit.py
# from datetime import datetime
# import hashlib
#
# class Commit:
#     def __init__(self, message, hash_code=None, timestamp=None):
#         self.timestamp = timestamp if timestamp else datetime.now().isoformat()
#         self.message = message
#         self.hash_code = hash_code or self._generate_hash()
#
#     def _generate_hash(self):
#         data = f"{self.timestamp}_{self.message}".encode("utf-8")
#         return hashlib.sha1(data).hexdigest()[:10]
#
#     def __str__(self):
#         return f"ID: {self.hash_code}\tMessage: {self.message}\tDate: {self.timestamp}"
#
#     def to_dict(self):
#         return {
#             "hash_code": self.hash_code,
#             "message": self.message,
#             "timestamp": self.timestamp
#         }
#
#     @classmethod
#     def from_dict(cls, data: dict):
#         return cls(
#             message=data["message"],
#             hash_code=data.get("hash_code"),
#             timestamp=data.get("timestamp")
#         )

from datetime import datetime
import hashlib

class Commit:
    def __init__(self, message, hash_code=None, timestamp=None):
        self.timestamp = timestamp or datetime.now().isoformat()
        self.message = message
        self.hash_code = hash_code or self._generate_hash()

    def _generate_hash(self):
        data = f"{self.timestamp}_{self.message}".encode()
        return hashlib.sha1(data).hexdigest()[:10]

    def __str__(self):
        return f"commit {self.hash_code}\nDate:   {self.timestamp}\n\n    {self.message}"


