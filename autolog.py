import os
import functools
from datetime import datetime

# Global log file path (folder-wide)
LOG_DIR = "Logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "activity_log.txt")

# Ensure file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("=== Activity Log ===\n")

def log_activity(message):
    """Write a log entry with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def auto_log(func):
    """Decorator: logs whenever a function is called."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arg_list = ", ".join([str(a) for a in args[1:]])  # skip self
        kwarg_list = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        params = ", ".join(filter(None, [arg_list, kwarg_list]))

        log_activity(f"CALL {func.__qualname__}({params})")
        result = func(*args, **kwargs)
        log_activity(f"RETURN {func.__qualname__} -> {type(result).__name__}")
        return result

    return wrapper
