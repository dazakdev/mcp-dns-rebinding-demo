"""Shared flip flag: the name points at 127.0.0.1 only inside this window."""

import os
import time

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".phase")
WINDOW_SECONDS = 90


def open_local_window():
    with open(STATE_FILE, "w") as f:
        f.write(str(time.time() + WINDOW_SECONDS))


def in_local_window():
    try:
        with open(STATE_FILE) as f:
            return time.time() < float(f.read().strip() or 0)
    except OSError:
        return False
