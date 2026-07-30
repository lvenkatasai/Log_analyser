import os
import sys
import platform
import subprocess
import datetime

OUTPUT_FILE = "large_sample_logs.log"

def normalize_windows_level(level):
    level = level.strip().lower()
    if level == "error": return "ERROR"
    if level == "warning": return "WARNING"
    if level == "information": return "INFO"
    return "DEBUG"

def extract_windows_logs():
    print("Detected Windows OS. Extracting Event Logs from the last 24 hours...")
    # We fetch Application logs. System logs could also be fetched.
    ps_command = (
        "Get-EventLog -LogName Application -After (Get-Date).AddDays(-1) -ErrorAction SilentlyContinue | "
        "Select-Object TimeGenerated, EntryType, Message | "
        "ConvertTo-Json -Compress"
    )
    
    try:
        # Note: Depending on volume, this might be huge. We'll limit it for safety in JSON.
        # Actually, piping to JSON might fail if the message contains complex formatting.
        # Let's use a simpler custom formatting in powershell to ensure we get lines.
        ps_command = (
            "Get-EventLog -LogName Application -After (Get-Date).AddDays(-1) -Newest 5000 -ErrorAction SilentlyContinue | "
            "ForEach-Object { "
            "  $time = $_.TimeGenerated.ToString('yyyy-MM-dd HH:mm:ss'); "
            "  $type = $_.EntryType; "
            "  $msg = $_.Message -replace \"`n|`r\", ' '; "
            "  \"[$time] [$type] $msg\" "
            "}"
        )
        result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error running PowerShell:", result.stderr)
            return []
            
        logs = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line: continue
            
            # Line format: [2023-10-27 10:00:00] [Information] The description...
            # We need to map [Information] -> [INFO]
            try:
                parts = line.split("] [", 1)
                time_part = parts[0] + "]" # [2023-10-27 10:00:00]
                rest = parts[1].split("] ", 1)
                level = rest[0]
                msg = rest[1]
                norm_level = normalize_windows_level(level)
                logs.append(f"{time_part} [{norm_level}] {msg}")
            except Exception:
                # If parsing fails, just keep it as INFO
                logs.append(line.replace("[Information]", "[INFO]"))
                
        return logs
    except Exception as e:
        print("Failed to extract Windows logs:", e)
        return []

def extract_linux_logs():
    print("Detected Linux OS. Attempting to extract logs via journalctl for the last 24 hours...")
    try:
        # We'll use journalctl and parse the date.
        cmd = ["journalctl", "--since", "24 hours ago", "--no-pager", "--output=short-iso"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        logs = []
        for line in result.stdout.splitlines():
            if not line.strip(): continue
            # Format: 2026-07-30T10:00:00+0000 hostname process[pid]: message
            try:
                parts = line.split(" ", 2)
                timestamp_raw = parts[0]
                # Convert ISO timestamp to YYYY-MM-DD HH:MM:SS
                dt = datetime.datetime.fromisoformat(timestamp_raw)
                timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                
                rest = parts[2]
                
                # Basic heuristic for level based on keywords
                level = "INFO"
                lower_rest = rest.lower()
                if "error" in lower_rest or "fail" in lower_rest: level = "ERROR"
                elif "warn" in lower_rest: level = "WARNING"
                
                logs.append(f"[{timestamp}] [{level}] {rest}")
            except Exception:
                pass
        return logs
    except Exception as e:
        print("Failed to run journalctl:", e)
        return []

def extract_mac_logs():
    print("Detected macOS. Extracting logs via log show for the last 24 hours...")
    try:
        cmd = ["log", "show", "--last", "24h", "--style", "syslog"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        logs = []
        for line in result.stdout.splitlines():
            if not line.strip(): continue
            try:
                # syslog style format usually starts with date. We will just use the current time for simplicity if parsing is too complex,
                # but let's try a simple timestamp insertion.
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                level = "INFO"
                lower_line = line.lower()
                if "error" in lower_line or "fail" in lower_line: level = "ERROR"
                elif "warn" in lower_line: level = "WARNING"
                
                logs.append(f"[{timestamp}] [{level}] {line}")
            except Exception:
                pass
        return logs
    except Exception as e:
        print("Failed to run macos log show:", e)
        return []

def main():
    current_os = platform.system()
    logs = []
    
    if current_os == "Windows":
        logs = extract_windows_logs()
    elif current_os == "Linux":
        logs = extract_linux_logs()
    elif current_os == "Darwin":
        logs = extract_mac_logs()
    else:
        print(f"Unsupported OS: {current_os}")
        sys.exit(1)
        
    if not logs:
        print("No logs extracted or command failed. Generating a dummy log to prevent empty file.")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs = [f"[{timestamp}] [INFO] System log extraction started but no logs were found."]
        
    print(f"Writing {len(logs)} real system logs to {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8", errors="replace") as f:
        for log in logs:
            f.write(log + "\n")
            
    print("Log extraction complete! You can now analyze this file in the dashboard.")

if __name__ == "__main__":
    main()
