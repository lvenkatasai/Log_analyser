import os
from patterns import LOG_PATTERN

def read_logs_generator(file_path):
    """
    Generator that lazily yields lines from a file.
    Efficient for high-volume log files.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Log file not found: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

def parse_log_line(line):
    """
    Parses a single log line using regular expressions.
    Returns a dictionary of extracted fields, or None if no match.
    """
    match = LOG_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None

def process_log_file(file_path):
    """
    Generator that yields parsed log entries.
    """
    for line in read_logs_generator(file_path):
        parsed = parse_log_line(line)
        if parsed:
            # We can optionally keep the raw line
            parsed['raw'] = line
            yield parsed
