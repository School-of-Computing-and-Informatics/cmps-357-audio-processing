# Contributing to Audio Processing Web Application

Thank you for considering contributing to this project! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

1. **Docker** (recommended for quick setup) OR
2. **Python 3.8+** (Python 3.12 recommended) + **FFmpeg**
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org)
3. **Git** for version control

**For detailed instructions:**
- Docker installation: See [docs/DOCKER.md](docs/DOCKER.md)
- Manual installation: See [docs/INSTALL_SYSTEM_REQUIREMENTS.md](docs/INSTALL_SYSTEM_REQUIREMENTS.md)

### Setting Up Development Environment

#### Option 1: Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/School-of-Computing-and-Informatics/cmps-357-audio-processing.git
   cd cmps-357-audio-processing
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker compose up --build
   ```

   The application will be available at `http://localhost:5000`

3. **Run tests in Docker:**
   ```bash
   # Run tests in a new container
   docker compose run --rm audio_app python -m pytest tests/ -v
   ```

4. **Access container shell for debugging:**
   ```bash
   docker compose exec audio_app /bin/bash
   ```

**Docker Development Tips:**
- The source code is mounted as a volume, so changes are reflected immediately
- Use `docker compose logs -f` to view application logs
- Use `docker compose restart` to restart after configuration changes

#### Option 2: Local Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/School-of-Computing-and-Informatics/cmps-357-audio-processing.git
   cd cmps-357-audio-processing
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests to verify setup:**
   ```bash
   python -m pytest tests/ -v
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

## Project Structure

```
├── src/                   # Source code
├── tests/                 # Test files
├── docs/                  # Documentation
├── scripts/               # Utility scripts
└── screenshots/           # UI screenshots
```

For detailed architecture, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Development Workflow

### 1. Create a Branch

Create a feature or fix branch:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Changes

- Follow the coding guidelines below
- Write or update tests for your changes
- Update documentation if needed
- Keep commits focused and atomic

### 3. Test Your Changes

Always test before committing:
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_app.py::test_name -v
```

### 4. Commit Changes

Write clear, descriptive commit messages:
```bash
git add .
git commit -m "Add feature: brief description

Detailed explanation of what changed and why."
```

### 5. Push and Create Pull Request

```bash
git push origin your-branch-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Description of what was changed and why
- Reference to any related issues
- Screenshots for UI changes

## Coding Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters (flexible for readability)
- Use descriptive variable and function names

### Code Organization

- **Source code**: Place in `src/` directory
- **Tests**: Place in `tests/` directory with `test_` prefix
- **Documentation**: Place in `docs/` directory
- **Scripts**: Place in `scripts/` directory

### Imports

Organize imports in this order:
1. Standard library imports
2. Third-party library imports
3. Local application imports

```python
import os
import sys

from flask import Flask, request
from pydub import AudioSegment

from src.audio_processor import AudioProcessor
```

### Error Handling

- Always use try-except blocks for operations that might fail
- Log errors appropriately
- Return user-friendly error messages (never expose stack traces)
- Use proper HTTP status codes in API responses

### Security

- Never expose file paths to users
- Always validate and sanitize user input
- Use `secure_filename()` for file uploads
- Don't commit secrets or credentials
- Follow the security guidelines in the codebase

## Testing Guidelines

### Writing Tests

- Place tests in `tests/` directory
- Name test files with `test_` prefix
- Name test functions with `test_` prefix
- Use descriptive test names that explain what's being tested

```python
def test_upload_validates_file_extension():
    """Test that upload rejects invalid file extensions."""
    # Test implementation
```

### Test Coverage

- Write tests for new features
- Write tests for bug fixes
- Aim for good coverage of critical paths
- Include both positive and negative test cases

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_app.py -v

# Run specific test
python -m pytest tests/test_app.py::test_name -v
```

## Documentation

### Code Documentation

- Add docstrings to functions, classes, and modules
- Document parameters, return values, and exceptions
- Keep comments up-to-date with code changes

```python
def process_audio(filepath: str, threshold: float = -20) -> str:
    """
    Process audio file with compression.
    
    Args:
        filepath: Path to input audio file
        threshold: Compression threshold in dB (default: -20)
        
    Returns:
        Path to processed audio file
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If threshold is invalid
    """
    # Implementation
```

### User Documentation

- Update README.md for user-facing changes
- Update relevant docs in `docs/` directory
- Add examples for new features
- Update screenshots for UI changes

## Adding Features

### Multi-threading Pattern

For new audio analysis operations, follow the standard pattern documented in [docs/MULTITHREADING_PATTERN.md](docs/MULTITHREADING_PATTERN.md):

1. Define chunk processor function
2. Define unpacker function
3. Add method using `_parallel_process_audio_chunks()`

### Flask Routes

When adding new routes:
- Use appropriate HTTP methods (GET, POST, etc.)
- Return JSON for API endpoints
- Validate input data
- Use proper HTTP status codes
- Add tests for the new route

## Pull Request Process

1. **Ensure all tests pass**
2. **Update documentation** if needed
3. **Add tests** for new features
4. **Describe your changes** clearly in the PR description
5. **Reference related issues** using #issue-number
6. **Respond to review feedback** promptly
7. **Keep the PR focused** - one feature/fix per PR

## Reporting Issues

When reporting issues, include:
- Clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or logs (if applicable)
- Screenshots (for UI issues)

## Need Help?

- Check existing documentation in `docs/`
- Review the [TODO.md](docs/TODO.md) for planned features
- Ask questions in GitHub issues
- Review existing code for examples

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be acknowledged in the project. Thank you for helping improve this project!
