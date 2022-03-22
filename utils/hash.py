import hashlib
import uuid


class ID:
    def __init__(self, value):
        self._hash = hashlib.sha256(value.encode("utf-8"))
        self._uuid = uuid.UUID(self._hash.hexdigest()[::2])
        self.ID = str(self._uuid)  
