import json

def generate_text_report(results):
    """
    Generates a human-readable text report.
    """
    report = []
    report.append("=" * 40)
    report.append("Log Analysis Report")
    report.append("=" * 40)
    report.append(f"Total Logs Processed: {results['total_logs']}")
    
    report.append("\nLog Levels:")
    for level, count in sorted(results['level_counts'].items(), key=lambda x: x[1], reverse=True):
        report.append(f"  - {level}: {count}")
        
    report.append(f"\nTotal Anomalies Detected: {results['total_anomalies']}")
    
    if results['total_anomalies'] > 0:
        report.append("\nAnomaly Signatures:")
        for sig, count in sorted(results['error_signatures'].items(), key=lambda x: x[1], reverse=True):
            report.append(f"  - {sig}: {count}")
            
    report.append("=" * 40)
    return "\n".join(report)

def generate_json_report(results):
    """
    Generates a JSON formatted report.
    """
    return json.dumps(results, indent=4)

def save_report(report_content, output_file):
    """
    Saves the report content to the specified file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
