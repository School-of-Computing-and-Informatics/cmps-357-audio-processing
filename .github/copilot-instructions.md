# GitHub Copilot Instructions for Audio Processing Web Application

## Project Overview

This is a Flask-based audio processing web application that allows users to upload audio files (MP3, AAC, AC3), analyze their statistics, and apply professional audio effects (compressor and limiter).

## Key Technologies

- **Backend**: Flask 3.0.0 (Python web framework)
- **Audio Processing**: pydub 0.25.1 (wrapper for FFmpeg)
- **Audio Backend**: FFmpeg (required system dependency)
- **Numerical Operations**: NumPy 1.26.0+
- **Security**: Werkzeug 3.0.3
- **Testing**: pytest 7.4.3

## Project Structure

```
├── src/                   # Source code
│   ├── app.py            # Flask application with routes and handlers
│   ├── audio_processor.py # AudioProcessor class for audio operations
│   └── templates/        # Web interface templates
│       └── index.html
├── tests/                 # Test files
│   └── test_app.py       # Unit tests
├── docs/                  # Documentation files
├── scripts/               # Utility scripts
│   ├── example_usage.py  # CLI usage example
│   └── startup.sh        # Setup and test script
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
└── README.md            # User documentation
```

## Coding Guidelines

### Python Code Style

1. **Follow PEP 8**: Use 4-space indentation, descriptive variable names
2. **Type Hints**: Not required but encouraged for function signatures
3. **Error Handling**: Always use try-except blocks with generic user-facing errors
4. **Logging**: Use print statements for now (future: proper logging)
5. **Security**: Never expose file paths, stack traces, or internal errors to users

### Flask Routes

- Use `@app.route` decorators with explicit methods
- Return JSON for API endpoints using `jsonify()`
- Always validate input data and return appropriate HTTP status codes
- Handle file uploads securely with `secure_filename()`

### Audio Processing

- All audio processing should use the `AudioProcessor` class in `audio_processor.py`
- Use pydub for audio manipulation (it wraps FFmpeg)
- Export processed audio as MP3 format
- Store files in system temp directory using `tempfile.gettempdir()`

### Multi-threading Pattern for Audio Analysis

**All audio analysis operations MUST use the standard multi-threading pattern to ensure consistent performance.**

#### ThreadConfig Singleton

Use `ThreadConfig` to manage thread count:

```python
from audio_processor import ThreadConfig

# Get current configuration
num_threads = ThreadConfig.get_num_threads()  # Default: half of CPU cores
max_threads = ThreadConfig.get_max_threads()   # Maximum: CPU cores

# Set specific number of threads
ThreadConfig.set_num_threads(4)
```

#### Standard Pattern for New Analysis Operations

Follow this three-step pattern when adding any new audio analysis operation:

**Step 1: Define Chunk Processor Function**

```python
def _process_chunk_for_my_operation(chunk_bytes, sample_width, frame_rate, channels):
    """Process a single chunk of audio (runs in worker process)."""
    from pydub import AudioSegment
    
    # Reconstruct AudioSegment from raw data
    chunk = AudioSegment(
        data=chunk_bytes,
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=channels
    )
    
    # Perform your analysis and return result
    result = analyze_chunk(chunk)
    return result
```

**Step 2: Define Unpacker Function**

```python
def _unpack_args_for_my_operation(args):
    """Unpack arguments and call chunk processor."""
    chunk_bytes, sample_width, frame_rate, channels, kwargs = args
    
    # Extract any optional parameters from kwargs
    threshold = kwargs.get('threshold', -50)
    
    return _process_chunk_for_my_operation(
        chunk_bytes, sample_width, frame_rate, channels
    )
```

**Step 3: Add Method to AudioProcessor**

```python
def _calculate_my_metric(self, threshold=-50):
    """Calculate my_metric using multi-threaded processing."""
    results = _parallel_process_audio_chunks(
        self.audio,
        _process_chunk_for_my_operation,
        _unpack_args_for_my_operation,
        threshold=threshold
    )
    
    # Aggregate results appropriately:
    # - Sum: return sum(results)
    # - Max: return max(results)
    # - Average: return sum(results) / len(results)
    return aggregate(results)
```

#### Current Multi-threaded Operations

- `_calculate_max_dbfs()` - Finds maximum dBFS, aggregates via `max()`
- `_calculate_min_dbfs()` - Finds minimum amplitude, converts to dBFS
- `_calculate_non_silence_duration()` - Sums non-silent durations from chunks

#### Why This Matters

- **Consistency**: All operations use the same threading mechanism
- **Configurability**: Users can adjust threads via Settings UI (`GET/POST /settings/threads`)
- **Performance**: Large files benefit from parallel processing
- **Future-proof**: New operations automatically respect thread configuration

See `MULTITHREADING_PATTERN.md` for complete documentation.

### Security Best Practices

1. **File Validation**: Only accept `.mp3`, `.aac`, `.ac3` extensions
2. **File Size Limit**: 100MB maximum (`MAX_CONTENT_LENGTH`)
3. **UUID-based File Tracking**: Never expose actual file paths to users
4. **Secure Filenames**: Always use `secure_filename()` from werkzeug
5. **Debug Mode**: Controlled by `FLASK_DEBUG` environment variable, disabled by default
6. **Generic Error Messages**: Don't leak implementation details in error responses

## Common Tasks

### Adding a New Audio Analysis Operation

**IMPORTANT**: All audio analysis operations (calculating statistics, detecting features, etc.) must use the multi-threading pattern described above.

1. Define chunk processor function: `_process_chunk_for_operation()`
2. Define unpacker function: `_unpack_args_for_operation()`
3. Add method to `AudioProcessor` using `_parallel_process_audio_chunks()`
4. Write unit tests in `test_app.py`
5. If exposing via API, add route handler in `app.py`

### Adding a New Audio Effect

1. Add the processing method to `AudioProcessor` class in `audio_processor.py`
2. Add a new route handler in `app.py` or extend the `/process` route
3. Update the frontend HTML/JavaScript to include the new operation
4. Add appropriate parameter validation
5. Write unit tests in `test_app.py`

### Adding a New Route

```python
@app.route('/your-route', methods=['POST'])
def your_handler():
    try:
        # Validate input
        # Process request
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Generic error message'}), 500
```

### File Upload Pattern

```python
file = request.files['file']
if not allowed_file(file.filename):
    return jsonify({'error': 'Invalid file type'}), 400

filename = secure_filename(file.filename)
filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
file.save(filepath)

file_id = str(uuid.uuid4())
file_storage[file_id] = {'filepath': filepath, 'filename': filename}
```

## Testing

- Run tests with: `python -m pytest test_app.py -v`
- All routes should have corresponding tests
- Test both success and error cases
- Mock file uploads using pytest fixtures

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Run with debug mode (development only)
FLASK_DEBUG=true python app.py

# Run tests
python -m pytest test_app.py -v
```

## Dependencies

### Required System Dependencies
- **FFmpeg**: Required by pydub for audio processing
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: Download from ffmpeg.org

### Python Dependencies
See `requirements.txt` - install with `pip install -r requirements.txt`

## API Endpoints

### POST /upload
- Upload and analyze audio file
- Returns: `file_id`, `filename`, `statistics`

### POST /process
- Apply audio effects (compressor or limiter)
- Body: `{file_id, operation, threshold, ratio, attack, release}`
- Returns: new `file_id` for processed audio

### GET /download/<file_id>
- Download processed audio file
- Returns: Audio file as attachment

### GET /settings/threads
- Get current thread configuration
- Returns: `{current_threads, max_threads, default_threads}`

### POST /settings/threads
- Update thread configuration
- Body: `{num_threads}`
- Validates: `1 <= num_threads <= max_threads` (CPU cores)
- Returns: `{current_threads, max_threads}` or error

## Audio Statistics

- **max_dbfs**: Peak audio level
- **min_dbfs**: Minimum non-zero level  
- **duration_seconds**: Total length
- **non_silence_seconds**: Active audio time (-50 dB threshold)
- **sample_rate**: Frequency in Hz
- **channels**: Number of audio channels
- **sample_width**: Bit depth in bytes

## Audio Effects

### Compressor
Reduces dynamic range for more consistent audio levels.
- **threshold**: Level above which compression applies (-60 to 0 dB)
- **ratio**: Compression ratio (1 to 20)
- **attack**: Time to reach full compression (0 to 100 ms)
- **release**: Time to return to normal (10 to 500 ms)

### Limiter
Prevents audio from exceeding a maximum level (prevents clipping).
- **threshold**: Maximum output level (-10 to 0 dB)
- **release**: Time to return to normal (10 to 500 ms)
- Implementation: Uses high-ratio compression (100:1) with 1ms attack

## Common Pitfalls

1. **Don't forget FFmpeg**: The application won't work without FFmpeg installed
2. **Temp file cleanup**: Consider implementing cleanup for old files
3. **Memory usage**: Large files are loaded into memory - monitor for OOM issues
4. **File storage**: In-memory dict is not production-ready (use Redis/DB)
5. **Debug mode**: Never enable in production - allows arbitrary code execution
6. **Error messages**: Always use generic messages for security

## Future Enhancements

- Persistent storage (Redis/PostgreSQL) instead of in-memory dict
- Automatic temp file cleanup
- More audio effects (EQ, reverb, noise reduction)
- Batch processing
- Audio format conversion
- Waveform visualization
- User accounts and file history
- WebSocket for real-time processing updates
