TODOs and converted issue entries
===============================

This file aggregates in-repo TODO comments and converts them into ready-to-open GitHub issue texts
and tracked todo entries. Each section includes a suggested title, description, acceptance criteria,
and a short implementation note.

1) ThreadConfig singleton
-------------------------
File: `audio_processor.py` (comment near top)

Title: Refactor `ThreadConfig` to use a singleton pattern

Severity: medium

Description:
Refactor the existing ThreadConfig so it is a true singleton object that controls the number
of worker threads used by audio analysis. This will make thread configuration accessible
from any module and consistent across the codebase.

Acceptance criteria:
- Add a `ThreadConfig` singleton with `get_num_threads()` and `set_num_threads(n)` methods.
- Default behaviour remains: default threads = half of CPU cores, max threads = CPU cores.
- All existing call sites can fetch and set configuration via the singleton without breaking.

Notes: keep API stable and add a small unit test that changes and reads the number.

2) Type-safety & Pylance migration task
--------------------------------------
File(s): `audio_processor.py` and other modules

Title: Migrate code to Type-safety & Pylance guidelines

Severity: low

Description:
Create a concrete refactor task to apply type hints and Pylance-friendly adjustments according to
`.github/COPILOT_TYPE_SAFETY.md`. Prioritize `audio_processor.py` and the Flask handlers.

Acceptance criteria:
- Produce a checklist of files that need type annotations and pylance fixes.
- Optionally add a minimal mypy / pylance configuration or instructions to the README.

Notes: this is mostly a coordination / multi-file refactor; break into smaller PRs.

3) Parallel processing pattern for audio functions
-------------------------------------------------
File: `audio_processor.py`

Title: Refactor audio processing functions to use the standard parallel processing pattern

Severity: high

Description:
Refactor the audio analysis functions to follow the three-step multi-thread pattern described
in `MULTITHREADING_PATTERN.md`: (1) chunk processor, (2) unpacker wrapper, (3) AudioProcessor method
that calls `_parallel_process_audio_chunks()` and aggregates results.

Acceptance criteria:
- Each expensive audio analysis uses the pattern.
- Thread usage respects `ThreadConfig`.
- Existing statistical outputs (max_dbfs, min_dbfs, non_silence_seconds) remain consistent.

Notes: implement one function at a time and add tests for correctness.

4) Move imports to the top
-------------------------
File: `audio_processor.py`

Title: Move import statements to module top-level

Severity: trivial

Description:
Move local or late imports to the top of the module, unless a specific local import is needed
to avoid circular dependencies or reduce optional-heavy import cost. Document any justified
exceptions inline.

Acceptance criteria:
- All non-justified imports at top of `audio_processor.py` (and other modules if found).
- Lint/type checks still pass.

Notes: keep imports grouped (stdlib, third-party, local).

5) Add error reporting API endpoint
----------------------------------
File: `app.py` (comment near line ~37)

Title: Add error reporting endpoint to API

Severity: medium

Description:
Add a POST endpoint `/report-error` that allows the frontend to report non-fatal errors
from audio processing or file handling. Records or logs the report server-side for later
triage.

Acceptance criteria:
- Endpoint accepts JSON payload {source, message, details?}.
- Returns 200 on success, 4xx for invalid input, 5xx on server error.
- Does not leak filesystem paths or stack traces to clients.
- Add a unit test validating the endpoint behaviour.

Notes: keep the initial implementation simple (write to server log); we can later add
persistence (file/db) or integration with an external error-tracking service.

6) Add configuration file support
---------------------------------
Severity: low

Title: Add configuration file support (config.yaml or .env)

Description:
Add support for application configuration via a configuration file (config.yaml) or enhanced .env
support. This will allow easier customization of settings like upload folder, max file size,
default thread count, and Flask settings without modifying code.

Acceptance criteria:
- Support loading configuration from config.yaml or enhanced .env
- Override defaults for upload folder, max file size, thread count, Flask host/port
- Maintain backward compatibility with existing environment variables
- Document all configuration options in README.md

Notes: Consider using python-dotenv for .env support or PyYAML for YAML config files.

7) Add logging infrastructure
-----------------------------
Severity: medium

Title: Replace print statements with proper logging

Description:
Replace all print() statements with Python's logging module for better production readiness.
This will allow for proper log levels (DEBUG, INFO, WARNING, ERROR), log rotation, and
configurable output destinations.

Acceptance criteria:
- Replace all print() calls with appropriate logging statements
- Configure logging with levels and formats
- Add logging configuration options
- Support log file output in addition to console
- Add documentation for logging configuration

Notes: Use logging.getLogger(__name__) pattern for module-specific loggers.

8) Add Docker support
--------------------
Severity: low

Title: Create Dockerfile and docker-compose.yml for containerized deployment

Description:
Add Docker support to simplify deployment and ensure consistent environments. Include
Dockerfile with all system dependencies (FFmpeg, Python, etc.) and docker-compose.yml
for easy orchestration.

Acceptance criteria:
- Create Dockerfile with all system dependencies
- Create docker-compose.yml for easy deployment
- Document Docker usage in README.md
- Include volume mounting for persistent storage
- Optimize image size (multi-stage build if needed)

Notes: Base image should include FFmpeg. Consider using python:3.12-slim as base.

9) Add API documentation
-----------------------
Severity: low

Title: Add OpenAPI/Swagger documentation for REST API

Description:
Add API documentation using OpenAPI (Swagger) specification. This will make it easier for
developers to understand and use the API endpoints programmatically.

Acceptance criteria:
- Document all API endpoints with OpenAPI spec
- Include request/response schemas and examples
- Add Swagger UI for interactive API exploration
- Integrate with Flask using flask-swagger or similar
- Update README with link to API docs

Notes: Consider using Flask-RESTX or flask-swagger-ui for automatic doc generation.

10) Add performance benchmarks
------------------------------
Severity: low

Title: Create performance benchmark suite for audio processing

Description:
Create a benchmark suite to measure and track performance of audio processing operations
across different file sizes and thread configurations. This will help optimize performance
and catch regressions.

Acceptance criteria:
- Create benchmark script that measures processing times
- Test with various file sizes (small, medium, large)
- Test with different thread configurations
- Generate benchmark report with statistics
- Add to CI/CD pipeline (optional)

Notes: Use pytest-benchmark or create custom timing utilities.

11) Add integration tests
------------------------
Severity: medium

Title: Add integration tests for end-to-end workflows

Description:
Add integration tests that verify the complete workflows: upload → analyze → process → download.
Currently tests are mostly unit tests. Integration tests will catch issues with the full pipeline.

Acceptance criteria:
- Create integration test suite in tests/integration/
- Test complete upload → analyze workflow
- Test complete process → download workflow
- Test error handling in full workflows
- Use real audio files (small test fixtures)

Notes: Keep test fixtures small (<1MB) and store in tests/fixtures/.

12) Add user session management
-------------------------------
Severity: low

Title: Implement proper session management for multi-user support

Description:
Currently file storage uses a simple dict that's shared across all users and doesn't persist
across server restarts. Implement proper session management to isolate user files and improve
reliability.

Acceptance criteria:
- Use Flask sessions to track user files
- Isolate files per session
- Add session expiry and cleanup
- Clean up old files automatically
- Document session behavior

Notes: Consider using Flask-Session for Redis/database-backed sessions if needed.

13) Add file format validation
------------------------------
Severity: medium

Title: Add deeper audio file format validation

Description:
Currently only file extensions are checked. Add validation that verifies files are actually
valid audio files of the claimed format. This prevents security issues and improves error messages.

Acceptance criteria:
- Validate file content matches extension
- Check for corrupted or invalid audio files
- Return specific error messages for invalid files
- Add tests for various invalid file scenarios
- Document supported formats and limitations

Notes: Use pydub's file opening to validate format, catch exceptions appropriately.

14) Add audio preview/waveform
------------------------------
Severity: low

Title: Add audio waveform visualization and preview playback

Description:
Add visual waveform display for uploaded audio and allow preview playback in the browser.
This improves user experience by showing what the audio looks like.

Acceptance criteria:
- Generate waveform image or data for uploaded audio
- Display waveform in UI
- Add audio player for preview playback
- Update both original and processed audio
- Optimize performance for large files

Notes: Consider using wavesurfer.js for frontend or generate images with matplotlib.

15) Add batch processing support
--------------------------------
Severity: low

Title: Support batch processing of multiple audio files

Description:
Allow users to upload and process multiple audio files at once with the same settings.
This improves efficiency for users processing many files.

Acceptance criteria:
- Support multiple file uploads
- Apply same processing to all files
- Show progress for batch operations
- Download all as zip file
- Update UI to support batch mode

Notes: Consider job queue for large batches (Celery or RQ).

----

How to use
----------
- Use these entries as GitHub issue templates: copy the Title + Description + Acceptance criteria
  into a new issue and assign/estimate as needed.
- The project's managed todo list (used by the developer tools) has been updated with these
  entries so you can mark progress from the editor/agent UI.

