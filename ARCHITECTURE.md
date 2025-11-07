# Audio Processing Application - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Modern Web Interface (HTML/CSS/JS)              │  │
│  │  - File upload UI                                         │  │
│  │  - Statistics display                                     │  │
│  │  - Processing controls                                    │  │
│  │  - Download functionality                                 │  │
│  └────────────────────┬──────────────────────────────────────┘  │
└─────────────────────────┼─────────────────────────────────────────┘
                         │ HTTP/JSON
                         │
        ┌────────────────▼───────────────────┐
        │      Flask Web Server               │
        │  ┌──────────────────────────────┐  │
        │  │  app.py - Main Application   │  │
        │  │  - Route handlers             │  │
        │  │  - File management (UUID)     │  │
        │  │  - Error handling             │  │
        │  │  - Security controls          │  │
        │  └───────────┬──────────────────┘  │
        │              │                      │
        │  ┌───────────▼──────────────────┐  │
        │  │  audio_processor.py          │  │
        │  │  - AudioProcessor class       │  │
        │  │  - Statistics calculation     │  │
        │  │  - Compressor/Limiter effects │  │
        │  │  - Audio file I/O             │  │
        │  └───────────┬──────────────────┘  │
        └──────────────┼─────────────────────┘
                       │
        ┌──────────────▼──────────────────┐
        │     Audio Processing Layer      │
        │  ┌──────────────────────────┐   │
        │  │   pydub (Python)          │   │
        │  │   - Audio manipulation    │   │
        │  │   - Format conversion     │   │
        │  │   - Effects processing    │   │
        │  └──────────┬────────────────┘   │
        │             │                     │
        │  ┌──────────▼────────────────┐   │
        │  │   FFmpeg (Backend)        │   │
        │  │   - Audio codec support   │   │
        │  │   - Format decoding       │   │
        │  │   - Audio encoding        │   │
        │  └───────────────────────────┘   │
        └─────────────────────────────────┘
                       │
        ┌──────────────▼──────────────────┐
        │    Temporary File Storage        │
        │  - Uploaded audio files          │
        │  - Processed output files        │
        │  - UUID-based naming             │
        └──────────────────────────────────┘
```

## Data Flow

### 1. Upload and Analysis
```
User selects file → Browser uploads via POST
  ↓
Flask receives file → Validates extension (mp3/aac/ac3)
  ↓
Saves to temp directory → Generates UUID
  ↓
AudioProcessor loads file → Analyzes audio
  ↓
Returns statistics → Displays in browser
  (max/min dB, duration, non-silence, etc.)
```

### 2. Audio Processing
```
User selects operation → Sets parameters
  ↓
Browser sends JSON → Flask validates file_id
  ↓
AudioProcessor loads file → Applies effect
  (Compressor or Limiter)
  ↓
Exports processed file → Generates new UUID
  ↓
Returns file_id → Browser shows download button
```

### 3. Download
```
User clicks download → Browser requests /download/<file_id>
  ↓
Flask validates file_id → Retrieves file path
  ↓
Returns file → Browser downloads
```

## Security Features

1. **File ID Abstraction**
   - UUIDs hide actual file paths
   - Prevents directory traversal attacks

2. **Input Validation**
   - File extension whitelist
   - File size limits (100MB)
   - Secure filename sanitization

3. **Error Handling**
   - Generic error messages to users
   - Detailed logging for debugging
   - No stack trace exposure

4. **Debug Mode Control**
   - Environment variable configuration
   - Disabled by default
   - Warning in documentation

## Technology Stack

- **Backend**: Flask 3.0.0 (Python web framework)
- **Audio Processing**: pydub 0.25.1 (Python audio library)
- **Audio Backend**: FFmpeg (required by pydub)
- **Numerical Operations**: NumPy 1.24.3
- **Security**: Werkzeug 3.0.3 (patched version)
- **Testing**: pytest 7.4.3

## File Structure

```
cmps-357-audio-processing/
├── app.py                  # Flask application (routes, handlers)
├── audio_processor.py      # Audio processing logic
├── requirements.txt        # Python dependencies
├── test_app.py            # Unit tests
├── .env.example           # Environment variable template
├── README.md              # Documentation
├── .gitignore             # Git ignore rules
└── templates/
    └── index.html         # Web interface
```

## Supported Audio Formats

**Input:**
- MP3 (.mp3)
- AAC (.aac)
- AC3 (.ac3)

**Output:**
- MP3 (.mp3) - Default for all processed files

## Processing Operations

### Compressor
- **Purpose**: Reduce dynamic range
- **Parameters**:
  - Threshold: -60 to 0 dB (default: -20)
  - Ratio: 1 to 20 (default: 4)
  - Attack: 0 to 100 ms (default: 5)
  - Release: 10 to 500 ms (default: 50)

### Limiter
- **Purpose**: Prevent clipping and peaks
- **Parameters**:
  - Threshold: -10 to 0 dB (default: -1)
  - Release: 10 to 500 ms (default: 50)
- **Implementation**: High-ratio compression (100:1) with fast attack

## Audio Statistics

1. **Max dBFS**: Peak level in the audio
2. **Min dBFS**: Minimum non-zero level
3. **Duration**: Total length in seconds
4. **Non-Silence Duration**: Active audio time (threshold: -50 dBFS)
5. **Sample Rate**: Samples per second (Hz)
6. **Channels**: Mono (1) or Stereo (2)
7. **Sample Width**: Bit depth in bytes
