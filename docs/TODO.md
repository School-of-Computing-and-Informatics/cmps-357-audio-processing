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

----

How to use
----------
- Use these entries as GitHub issue templates: copy the Title + Description + Acceptance criteria
  into a new issue and assign/estimate as needed.
- The project's managed todo list (used by the developer tools) has been updated with these
  entries so you can mark progress from the editor/agent UI.

