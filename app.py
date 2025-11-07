import os
from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import tempfile
from audio_processor import AudioProcessor

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'mp3', 'ac3', 'aac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only mp3, ac3, and aac files are allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process audio file and get statistics
        processor = AudioProcessor(filepath)
        stats = processor.get_statistics()
        
        # Store filepath in session for later use
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process_audio():
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        operation = data.get('operation')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        processor = AudioProcessor(filepath)
        
        if operation == 'compressor':
            threshold = float(data.get('threshold', -20))
            ratio = float(data.get('ratio', 4))
            attack = float(data.get('attack', 5))
            release = float(data.get('release', 50))
            
            output_path = processor.apply_compressor(threshold, ratio, attack, release)
        
        elif operation == 'limiter':
            threshold = float(data.get('threshold', -1))
            release = float(data.get('release', 50))
            
            output_path = processor.apply_limiter(threshold, release)
        
        else:
            return jsonify({'error': 'Invalid operation'}), 400
        
        return jsonify({
            'success': True,
            'output_path': output_path,
            'filename': os.path.basename(output_path)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:filepath>')
def download_file(filepath):
    try:
        # Security: only allow files from temp directory
        if not filepath.startswith(tempfile.gettempdir()):
            return jsonify({'error': 'Invalid file path'}), 403
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
