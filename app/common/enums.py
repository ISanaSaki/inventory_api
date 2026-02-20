from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"
class ChangeType(str,Enum):
    IN="IN"
    OUT="OUT"