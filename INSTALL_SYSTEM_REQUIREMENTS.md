# System Requirements for cmps-357-audio-processing

Before installing Python dependencies, ensure the following system packages and tools are installed:

## Required Packages

- **libbz2-dev**
  - Development headers and libraries for bzip2 compression. Required for building Python with bzip2 support and for some scientific packages.
  - Install with: `sudo apt-get install libbz2-dev`

- **libsqlite3-dev**
  - Development headers and libraries for SQLite3. Required for building Python with SQLite3 support and for database functionality in Python.
  - Install with: `sudo apt-get install libsqlite3-dev`

## Python Version Management

- **pyenv**
  - A tool for easily installing and managing multiple Python versions. Recommended for development environments where you need a specific Python version.
  - Install instructions: https://github.com/pyenv/pyenv#installation

- **Python 3.12.0**
  - The recommended Python version for this project. Many scientific packages are not yet compatible with Python 3.13 or newer.
  - Install with pyenv:
    ```bash
    pyenv install 3.12.0
    pyenv local 3.12.0
    ```

## Python Package Compatibility

- **Numpy**
  - For Python 3.12, you must use `numpy>=1.26.0` due to upstream compatibility changes. Older versions (e.g., 1.24.x) will not install or build correctly on Python 3.12.
  - This requirement is reflected in the project's `requirements.txt`.

## Notes
- If you use pyenv, ensure your shell is configured to load pyenv (see `.zshrc` or `.bashrc` setup instructions).
- After installing these system requirements, you can proceed to set up your Python virtual environment and install project dependencies.
