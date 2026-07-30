import re

# Standard log pattern format: [YYYY-MM-DD HH:MM:SS] [LEVEL] Message
# Example: [2023-10-27 10:00:00] [ERROR] Database connection failed
LOG_PATTERN = re.compile(
    r"\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+"
    r"\[(?P<level>[A-Z]+)\]\s+"
    r"(?P<message>.*)"
)

# Anomaly patterns
ERROR_PATTERN = re.compile(r"(error|exception|fail|timeout)", re.IGNORECASE)
IP_ADDRESS_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

# specific error signatures to categorize them
SIGNATURES = {
    "database_error": re.compile(r"database connection failed|mysql error|postgres error", re.IGNORECASE),
    "timeout_error": re.compile(r"timeout|timed out", re.IGNORECASE),
    "auth_failure": re.compile(r"authentication failed|invalid password", re.IGNORECASE),
}
