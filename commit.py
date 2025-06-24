from datetime import datetime
import hashlib
# commit.py
class Commit:
    def __init__(self, message, hash_code=None, date_time=None):
        self.date_time = date_time if date_time else datetime.now().isoformat()
        self.message = message
        if hash_code:
            self.hash_code = hash_code
        else:
            hash_input = f"{self.date_time}_{self.message}".encode('utf-8')
            self.hash_code = hashlib.sha1(hash_input).hexdigest()[:10]

    def __str__(self):
        return f"ID: {self.hash_code}\tMessage: {self.message}\tDate: {self.date_time}"

    def get_list_value(self):
        return [self.hash_code, self.message, self.date_time]
