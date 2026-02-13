from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class ChangeType(str,Enum):
    IN="IN"
    OUT="OUT"