import os
import uuid
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import tempfile
from audio_processor import AudioProcessor

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Store file mappings in memory (in production, use Redis or database)
file_storage = {}

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
        
        # Generate a unique file ID and store the mapping
        file_id = str(uuid.uuid4())
        file_storage[file_id] = {
            'filepath': filepath,
            'filename': filename
        }
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': filename,
            'statistics': stats
        })
    except Exception as e:
        # Log the error for debugging (in production, use proper logging)
        print(f"Error in upload_file: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the file'}), 500

@app.route('/process', methods=['POST'])
def process_audio():
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        operation = data.get('operation')
        
        if not file_id or file_id not in file_storage:
            return jsonify({'error': 'Invalid file ID'}), 404
        
        filepath = file_storage[file_id]['filepath']
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        processor = AudioProcessor(filepath)
        
        # Extract optional start and end times for sample processing
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        # Convert to float if provided
        start_time = float(start_time) if start_time is not None else None
        end_time = float(end_time) if end_time is not None else None
        
        if operation == 'compressor':
            threshold = float(data.get('threshold', -20))
            ratio = float(data.get('ratio', 4))
            attack = float(data.get('attack', 5))
            release = float(data.get('release', 50))
            
            output_path = processor.apply_compressor(threshold, ratio, attack, release, start_time, end_time)
        
        elif operation == 'limiter':
            threshold = float(data.get('threshold', -1))
            release = float(data.get('release', 50))
            
            output_path = processor.apply_limiter(threshold, release, start_time, end_time)
        
        else:
            return jsonify({'error': 'Invalid operation'}), 400
        
        # Store the output file with a new ID
        output_id = str(uuid.uuid4())
        file_storage[output_id] = {
            'filepath': output_path,
            'filename': os.path.basename(output_path)
        }
        
        return jsonify({
            'success': True,
            'file_id': output_id,
            'filename': os.path.basename(output_path)
        })
    
    except Exception as e:
        # Log the error for debugging (in production, use proper logging)
        print(f"Error in process_audio: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the audio'}), 500

@app.route('/download/<file_id>')
def download_file(file_id):
    try:
        if file_id not in file_storage:
            return jsonify({'error': 'Invalid file ID'}), 404
        
        file_info = file_storage[file_id]
        filepath = file_info['filepath']
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True, download_name=file_info['filename'])
    except Exception as e:
        # Log the error for debugging (in production, use proper logging)
        print(f"Error in download_file: {str(e)}")
        return jsonify({'error': 'An error occurred while downloading the file'}), 500

if __name__ == '__main__':
    # Use environment variable to control debug mode
    # In production, set FLASK_DEBUG=False or don't set it at all
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
