import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from log_parser import parse_log_line
from analyzer import LogAnalyzer

app = Flask(__name__, static_folder='static', static_url_path='')

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

def process_uploaded_file(file_path):
    """
    Generator that parses the file without holding it all in memory.
    """
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed:
                yield parsed

@app.route('/api/analyze', methods=['POST'])
def analyze_log():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        analyzer = LogAnalyzer()
        
        try:
            # Process the log file
            log_entries = process_uploaded_file(file_path)
            analyzer.analyze(log_entries)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            # Clean up the uploaded file to save space
            if os.path.exists(file_path):
                os.remove(file_path)
                
        results = analyzer.get_results()
        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
