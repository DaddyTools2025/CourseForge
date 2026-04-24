"""
CourseForge Logger
Standardized logging for Vibecoding compliance.
"""

import sys
from datetime import datetime
from enum import Enum

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARN"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

class VibeLogger:
    @staticmethod
    def _log(level: LogLevel, message: str, *args):
        timestamp = datetime.now().isoformat()
        formatted_message = message.format(*args) if args else message
        log_entry = f"[VIBE-{timestamp}] [{level.value}] {formatted_message}"

        # Print to console (stdout/stderr)
        if level == LogLevel.ERROR:
            print(log_entry, file=sys.stderr)
        else:
            print(log_entry, file=sys.stdout)

    @classmethod
    def info(cls, message: str, *args):
        cls._log(LogLevel.INFO, message, *args)

    @classmethod
    def warning(cls, message: str, *args):
        cls._log(LogLevel.WARNING, message, *args)

    @classmethod
    def error(cls, message: str, *args):
        cls._log(LogLevel.ERROR, message, *args)

    @classmethod
    def debug(cls, message: str, *args):
        cls._log(LogLevel.DEBUG, message, *args)
