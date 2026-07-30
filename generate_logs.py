import random
import datetime

# Configuration
NUM_LOGS = 15000
OUTPUT_FILE = "large_sample_logs.log"

LEVELS = [
    ("INFO", 0.70),
    ("DEBUG", 0.15),
    ("WARNING", 0.08),
    ("ERROR", 0.06),
    ("CRITICAL", 0.01),
]

# Normal messages
INFO_MESSAGES = [
    "System started successfully",
    "Handling user request for /api/v1/data",
    "Cache hit for key user_profile_123",
    "Successfully processed background job #4912",
    "User admin logged in from 192.168.1.100",
    "Connection established to message queue"
]

DEBUG_MESSAGES = [
    "Initializing cache manager",
    "Fetching row 4021 from database",
    "Parsing JSON payload",
    "Session token refreshed"
]

# Anomaly messages (matching our signatures)
WARNING_MESSAGES = [
    "Deprecated API usage detected in legacy_module.py",
    "High memory usage detected (85%)",
    "Rate limit approaching for IP 10.0.0.55"
]

ERROR_MESSAGES = [
    "Database connection failed: Connection refused",
    "Authentication failed for user guest",
    "MySQL Error: Deadlock found when trying to get lock",
    "Invalid password provided for account admin",
    "NullPointerException in DataProcessor class"
]

CRITICAL_MESSAGES = [
    "Timeout while waiting for external service after 30000ms",
    "Service crashed with exit code 137",
    "Disk space exhausted on /var/log"
]

def get_weighted_random_level():
    r = random.random()
    cumulative = 0.0
    for level, prob in LEVELS:
        cumulative += prob
        if r < cumulative:
            return level
    return "INFO"

def generate_message(level):
    if level == "INFO":
        return random.choice(INFO_MESSAGES)
    elif level == "DEBUG":
        return random.choice(DEBUG_MESSAGES)
    elif level == "WARNING":
        return random.choice(WARNING_MESSAGES)
    elif level == "ERROR":
        return random.choice(ERROR_MESSAGES)
    elif level == "CRITICAL":
        return random.choice(CRITICAL_MESSAGES)
    return "Unknown event occurred"

def main():
    print(f"Generating {NUM_LOGS} logs to {OUTPUT_FILE}...")
    start_time = datetime.datetime.now() - datetime.timedelta(days=7)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for _ in range(NUM_LOGS):
            # Increment time by random milliseconds/seconds
            start_time += datetime.timedelta(milliseconds=random.randint(10, 5000))
            
            level = get_weighted_random_level()
            message = generate_message(level)
            
            # Format: [2023-10-27 10:00:00] [INFO] message
            timestamp_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"[{timestamp_str}] [{level}] {message}\n"
            f.write(log_line)
            
    print("Log generation complete!")

if __name__ == "__main__":
    main()
