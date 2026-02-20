import re

COMMON_WEAK = {"password", "12345678", "qwerty", "11111111"}

def validate_password(pw: str) -> None:
    if len(pw) < 12:
        raise ValueError("Password must be at least 12 characters long.")

    if pw.lower() in COMMON_WEAK:
        raise ValueError("Password is too common or too weak.")

    if not re.search(r"[A-Za-z]", pw):
        raise ValueError("Password must contain at least one letter.")

    if not re.search(r"\d", pw):
        raise ValueError("Password must contain at least one number.")