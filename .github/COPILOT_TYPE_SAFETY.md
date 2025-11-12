# Type-safety & Pylance guidelines for this repository

This file documents a consistent type-safety style intended to keep the project Pylance-friendly and easy for contributors (and Copilot) to follow.

Principles
- Be explicit: annotate public APIs with return types and parameter types.
- Narrow types: prefer Optional[float] or List[float] rather than Any when the shape is known.
- Validate at runtime: prefer `isinstance(...)` checks and `assert` to document invariants instead of silent casts.
- Keep runtime behavior unchanged: type hints and checks should document and verify invariants, not change semantics.

Recommended patterns and examples

1) Class attributes initialized to None

```python
from typing import Optional

class ThreadConfig:
    _instance: Optional["ThreadConfig"] = None
    _num_threads: Optional[int] = None

    def __new__(cls) -> "ThreadConfig":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def set_num_threads(cls, num_threads: Optional[int] = None) -> None:
        cpu = os.cpu_count() or 2
        cls._num_threads = max(1, cpu // 2) if num_threads is None else max(1, min(num_threads, cpu))

    @classmethod
    def get_num_threads(cls) -> int:
        if cls._num_threads is None:
            cls.set_num_threads()
        # Make invariant explicit for the type checker
        assert isinstance(cls._num_threads, int)
        return cls._num_threads
```

2) Precise Callables and return types for helpers

```python
from typing import Callable, Any, List

def _parallel_process_audio_chunks(
    audio: AudioSegment,
    process_func: Callable[..., Any],
    chunk_processor_func: Callable[[Any], Any],
    min_chunk_size_ms: int = 10000,
) -> List[Any]:
    ...
```

3) Helper functions should use narrow return types

```python
from typing import Optional

def _process_chunk_for_min_dbfs(...) -> Optional[float]:
    # returns float amplitude or None
    ...
```

4) Guard data coming from untyped sources (HTTP/JSON)

```python
data = request.get_json()
if not data or not isinstance(data, dict):
    raise ValueError("Expected JSON body")
# data is now a dict for the type checker
value: Optional[float] = data.get('threshold')
```

5) Casting vs asserting
- Prefer `assert isinstance(x, T)` when you can ensure the invariant at runtime.
- Use `typing.cast(...)` sparingly when interacting with third-party APIs; prefer to document why the cast is safe.

Numeric conversions and explicit types
- When converting numbers, use `float(...)` or `int(...)` explicitly and validate ranges.
- Annotate functions that accept numerical parameters as `float` if callers may pass floats (helps Pylance and prevents float->int mismatches).

Small checklist when adding code
- [ ] Add explicit parameter and return types to public functions
- [ ] Avoid `Any` as a return type for new helpers
- [ ] Provide runtime guards for values that may be None
- [ ] Use `isinstance` + `assert` before returning a narrowed type

If you want, I can run a static type check (mypy) across the repository and propose incremental fixes to bring it to full type-coverage.
