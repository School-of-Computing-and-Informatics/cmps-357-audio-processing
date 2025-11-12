# Multi-threading Pattern for Audio Processing

## Overview

This document describes the multi-threading pattern used in the audio processing application. All audio analysis operations use this pattern to ensure consistent performance and configurability.

## Architecture

### ThreadConfig Singleton

The `ThreadConfig` class manages the number of threads used for audio processing:

- **Default**: Half of available CPU cores (minimum 1)
- **Maximum**: Number of CPU cores available
- **Configurable**: Users can adjust via the Settings UI or API

```python
from audio_processor import ThreadConfig

# Get current configuration
num_threads = ThreadConfig.get_num_threads()
max_threads = ThreadConfig.get_max_threads()

# Set specific number of threads
ThreadConfig.set_num_threads(4)

# Reset to default (half of cores)
ThreadConfig.set_num_threads(None)
```

### Core Pattern: _parallel_process_audio_chunks()

This function provides a standardized way to process audio in parallel chunks:

```python
def _parallel_process_audio_chunks(
    audio: AudioSegment,
    process_func: Callable,
    chunk_processor_func: Callable,
    min_chunk_size_ms: int = 10000,
    **kwargs
) -> Any
```

**Parameters:**
- `audio`: The AudioSegment to process
- `process_func`: Function that processes a single chunk (runs in worker process)
- `chunk_processor_func`: Function that unpacks arguments and calls process_func
- `min_chunk_size_ms`: Minimum chunk size in milliseconds (default: 10 seconds)
- `**kwargs`: Additional arguments passed to the process function

**Returns:**
- List of results from each chunk (to be aggregated by caller)

**Behavior:**
- Divides audio into N chunks where N = number of configured threads
- Each chunk is at least `min_chunk_size_ms` in size
- Single chunk: Processes directly without multiprocessing overhead
- Multiple chunks: Uses `ProcessPoolExecutor` for parallel processing

## How to Add New Multi-threaded Operations

Follow this three-step pattern:

### Step 1: Define Chunk Processor Function

Create a function that processes a single chunk of audio. This runs in a worker process:

```python
def _process_chunk_for_my_operation(chunk_bytes, sample_width, frame_rate, channels):
    """
    Process a single chunk for my_operation.
    
    Args:
        chunk_bytes: Raw audio data
        sample_width: Bytes per sample
        frame_rate: Sample rate in Hz
        channels: Number of audio channels
        
    Returns:
        Result specific to this operation
    """
    from pydub import AudioSegment
    
    # Reconstruct AudioSegment from raw data
    chunk = AudioSegment(
        data=chunk_bytes,
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=channels
    )
    
    # Perform your analysis
    result = analyze_chunk(chunk)
    
    return result
```

### Step 2: Define Unpacker Function

Create a function to unpack arguments for the chunk processor:

```python
def _unpack_args_for_my_operation(args):
    """Unpack arguments and call the chunk processor."""
    chunk_bytes, sample_width, frame_rate, channels, kwargs = args
    
    # Extract any optional parameters from kwargs
    threshold = kwargs.get('threshold', -50)
    
    return _process_chunk_for_my_operation(
        chunk_bytes, sample_width, frame_rate, channels, threshold
    )
```

### Step 3: Use the Pattern in Your Method

Add a method to the `AudioProcessor` class that uses the pattern:

```python
def _calculate_my_metric(self, threshold=-50):
    """
    Calculate my_metric using multi-threaded processing.
    
    Args:
        threshold: Threshold parameter for the analysis
        
    Returns:
        Aggregated result from all chunks
    """
    results = _parallel_process_audio_chunks(
        self.audio,
        _process_chunk_for_my_operation,
        _unpack_args_for_my_operation,
        threshold=threshold
    )
    
    # Aggregate results as appropriate for your operation
    # Examples:
    # - Sum: return sum(results)
    # - Max: return max(results)
    # - Average: return sum(results) / len(results)
    # - Concatenate: return list(itertools.chain(*results))
    
    return aggregate(results)
```

## Current Implementations

### 1. Max dBFS Calculation

Finds the maximum dBFS level across all chunks:

```python
def _calculate_max_dbfs(self):
    results = _parallel_process_audio_chunks(
        self.audio,
        _process_chunk_for_max_dbfs,
        _unpack_args_for_max_dbfs
    )
    return max(results)
```

### 2. Min dBFS Calculation

Finds the minimum non-zero amplitude and converts to dBFS:

```python
def _calculate_min_dbfs(self):
    results = _parallel_process_audio_chunks(
        self.audio,
        _process_chunk_for_min_dbfs,
        _unpack_args_for_min_dbfs
    )
    
    valid_results = [r for r in results if r is not None]
    if len(valid_results) == 0:
        return -float('inf')
    
    min_amplitude = min(valid_results)
    # Convert to dBFS...
    return dbfs_value
```

### 3. Non-Silence Duration

Calculates total non-silent duration by summing results from all chunks:

```python
def _calculate_non_silence_duration(self, silence_threshold=-50):
    results = _parallel_process_audio_chunks(
        self.audio,
        _process_chunk_for_nonsilence,
        _unpack_args_for_nonsilence,
        silence_threshold=silence_threshold
    )
    
    total_nonsilent_ms = sum(results)
    return total_nonsilent_ms / 1000.0
```

## API Endpoints

### GET /settings/threads

Retrieve current thread configuration:

```json
{
  "success": true,
  "current_threads": 2,
  "max_threads": 4,
  "default_threads": 2
}
```

### POST /settings/threads

Update thread configuration:

**Request:**
```json
{
  "num_threads": 3
}
```

**Response:**
```json
{
  "success": true,
  "current_threads": 3,
  "max_threads": 4
}
```

**Validation:**
- `num_threads` must be an integer
- Must be between 1 and max_threads (CPU cores)
- Invalid values return 400 error

## Frontend Settings UI

Users can configure threading through the Settings modal:

1. Click the "⚙️ Settings" button in the top-right corner
2. View system information (max threads, default, current setting)
3. Adjust the slider to select desired thread count (1 to max)
4. Click "Save Settings" to apply changes

Settings persist for the session and affect all subsequent audio processing operations.

## Performance Considerations

### When to Use Multi-threading

✅ **Good candidates for multi-threading:**
- Operations that process large audio files (> 30 seconds)
- CPU-intensive calculations (FFT, spectral analysis, dBFS calculations)
- Operations that can be split into independent chunks
- Analysis operations that aggregate results

❌ **Poor candidates for multi-threading:**
- Small files (< 10 seconds) - overhead exceeds benefits
- Operations that require sequential processing
- Operations with significant inter-chunk dependencies
- Simple file I/O operations

### Chunk Size Tuning

The default minimum chunk size is 10 seconds (10,000 ms). Consider adjusting for:

- **Larger chunks** (20-30s): Better for operations with high setup overhead
- **Smaller chunks** (5-10s): Better for fine-grained parallelism with many cores

```python
# Example: Use 20-second minimum chunks
results = _parallel_process_audio_chunks(
    self.audio,
    process_func,
    unpacker_func,
    min_chunk_size_ms=20000
)
```

## Testing

Always add tests for new multi-threaded operations:

```python
def test_my_operation():
    """Test multi-threaded my_operation."""
    from audio_processor import AudioProcessor, ThreadConfig
    
    # Test with different thread counts
    for num_threads in [1, 2, 4]:
        ThreadConfig.set_num_threads(num_threads)
        processor = AudioProcessor(test_file_path)
        result = processor._calculate_my_metric()
        assert result is not None
        # Add appropriate assertions
```

## Best Practices

1. **Keep chunk processors pure**: No side effects, only input → output
2. **Import inside chunk processors**: Import libraries at function level to avoid pickling issues
3. **Return simple types**: Prefer primitives (int, float, list) over complex objects
4. **Handle edge cases**: Empty chunks, None values, division by zero
5. **Document parameters**: Clearly explain all kwargs in docstrings
6. **Test thoroughly**: Verify results match single-threaded implementation

## Troubleshooting

### Issue: Multiprocessing errors on Windows

**Solution**: Ensure the pattern is used within a function, not at module level.

### Issue: Results differ from single-threaded version

**Solution**: Check chunk boundaries - some operations may need overlap or special boundary handling.

### Issue: Poor performance with multi-threading

**Solution**: 
- Verify file is large enough (> 30 seconds)
- Check if operation has too much overhead
- Consider increasing `min_chunk_size_ms`

### Issue: Memory issues with large files

**Solution**:
- Process in streaming fashion if possible
- Reduce number of threads
- Increase chunk size to reduce number of chunks
