from datetime import datetime, timedelta, timezone

LOCKOUT_THRESHOLD = 5
LOCKOUT_WINDOW_MINUTES = 15
LOCKOUT_DURATION_MINUTES = 15

def utcnow():
    return datetime.now(timezone.utc)

def is_locked(user) -> bool:
    return user.locked_until is not None and user.locked_until > utcnow()

def register_failed_login(user):
    now = utcnow()

    if user.last_failed_at is None or (now - user.last_failed_at) > timedelta(minutes=LOCKOUT_WINDOW_MINUTES):
        user.failed_login_count = 0

    user.failed_login_count += 1
    user.last_failed_at = now

    if user.failed_login_count >= LOCKOUT_THRESHOLD:
        user.locked_until = now + timedelta(minutes=LOCKOUT_DURATION_MINUTES)

def register_success_login(user):
    user.failed_login_count = 0
    user.locked_until = None
    user.last_failed_at = None
