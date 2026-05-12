"""Small server logging helper used by the Flask server code.

Provides a single `_log(msg: str)` function which prefixes messages
with a timestamp and adds color based on the first bracketed tag
found in the message (e.g. "[ERROR]", "[WARN]", "[INFO]").

Colors:
- [INFO] -> default terminal color
- [ERROR] -> red
- [WARN] -> yellow (approx. orange)
- otherwise -> grey
"""
from datetime import datetime
import re

try:
    import colorama
    colorama.init()
except Exception:
    # colorama is optional; ANSI codes may still work on modern terminals
    pass

RESET = "\033[0m"
COLORS = {
    "ERROR": "\033[31m",
    "WARN": "\033[33m",
    "INFO": "",
}


def _log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    m = re.search(r"\[([^\]]+)\]", msg)
    tag = m.group(1).upper() if m else ""
    color = COLORS.get(tag, "\033[90m")

    if color:
        print(f"[{ts}] {color}{msg}{RESET}")
    else:
        print(f"[{ts}] {msg}")
