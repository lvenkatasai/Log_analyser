from collections import Counter
from patterns import ERROR_PATTERN, SIGNATURES

class LogAnalyzer:
    def __init__(self):
        self.total_logs = 0
        self.level_counts = Counter()
        self.anomaly_counts = Counter()
        self.error_signatures = Counter()

    def analyze(self, log_entries):
        """
        Consumes an iterator of parsed log entries and aggregates statistics.
        """
        for entry in log_entries:
            self.total_logs += 1
            level = entry.get('level', 'UNKNOWN')
            self.level_counts[level] += 1
            
            message = entry.get('message', '')
            
            # Pattern matching for anomalies
            if level in ('ERROR', 'CRITICAL', 'FATAL') or ERROR_PATTERN.search(message):
                self.anomaly_counts['total_errors'] += 1
                
                # Further categorize the error
                categorized = False
                for sig_name, pattern in SIGNATURES.items():
                    if pattern.search(message):
                        self.error_signatures[sig_name] += 1
                        categorized = True
                
                if not categorized:
                    self.error_signatures['other_errors'] += 1

    def get_results(self):
        return {
            "total_logs": self.total_logs,
            "level_counts": dict(self.level_counts),
            "total_anomalies": self.anomaly_counts.get('total_errors', 0),
            "error_signatures": dict(self.error_signatures)
        }
