import argparse
import sys
from log_parser import process_log_file
from analyzer import LogAnalyzer
from report_generator import generate_text_report, generate_json_report, save_report

def main():
    parser = argparse.ArgumentParser(description="Log Analysis Tool for processing large-scale system logs.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input log file.")
    parser.add_argument("-o", "--output", help="Path to save the output report.")
    parser.add_argument("--format", choices=['text', 'json'], default='text', help="Format of the output report.")
    
    args = parser.parse_args()
    
    print(f"Processing log file: {args.input}...")
    
    analyzer = LogAnalyzer()
    
    try:
        # Create an iterator over the parsed log entries
        log_entries = process_log_file(args.input)
        
        # Analyze the entries
        analyzer.analyze(log_entries)
    except FileNotFoundError:
        print(f"Error: Log file '{args.input}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        sys.exit(1)
        
    results = analyzer.get_results()
    
    # Generate Report
    if args.format == 'json':
        report_content = generate_json_report(results)
    else:
        report_content = generate_text_report(results)
        
    # Output Report
    if args.output:
        save_report(report_content, args.output)
        print(f"Report saved to: {args.output}")
    else:
        print("\n" + report_content)

if __name__ == "__main__":
    main()
