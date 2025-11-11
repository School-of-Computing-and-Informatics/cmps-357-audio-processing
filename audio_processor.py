import os
import tempfile
from typing import Optional, Callable, List, Any
from pydub import AudioSegment
from pydub.effects import compress_dynamic_range, normalize
import numpy as np
import concurrent.futures
import math


class ThreadConfig:
    """Configuration for multi-threading in audio processing operations."""
    _instance = None
    _num_threads = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThreadConfig, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def set_num_threads(cls, num_threads: Optional[int] = None):
        """
        Set the number of threads to use for audio processing.
        
        Args:
            num_threads: Number of threads to use. If None, defaults to half of CPU cores.
                        Maximum is the number of CPU cores.
        """
        cpu_count = os.cpu_count() or 2
        if num_threads is None:
            cls._num_threads = max(1, cpu_count // 2)
        else:
            cls._num_threads = max(1, min(num_threads, cpu_count))
    
    @classmethod
    def get_num_threads(cls) -> int:
        """Get the configured number of threads for audio processing."""
        if cls._num_threads is None:
            cls.set_num_threads()
        return cls._num_threads
    
    @classmethod
    def get_max_threads(cls) -> int:
        """Get the maximum number of threads (CPU cores)."""
        return os.cpu_count() or 2


def _parallel_process_audio_chunks(
    audio: AudioSegment,
    process_func: Callable,
    chunk_processor_func: Callable,
    min_chunk_size_ms: int = 10000,
    **kwargs
) -> Any:
    """
    Generic pattern for processing audio in parallel chunks.
    
    This function divides audio into chunks and processes them in parallel using
    the configured number of threads. This pattern should be used for all analysis
    operations to ensure consistent multi-threading behavior.
    
    Args:
        audio: AudioSegment to process
        process_func: Function to process a single chunk (runs in worker process)
        chunk_processor_func: Function to unpack args and call process_func
        min_chunk_size_ms: Minimum chunk size in milliseconds
        **kwargs: Additional arguments to pass to process_func
        
    Returns:
        Result depends on the process_func - typically a list of results from each chunk
    """
    audio_length_ms = len(audio)
    num_workers = ThreadConfig.get_num_threads()
    chunk_size_ms = max(min_chunk_size_ms, audio_length_ms // num_workers)
    
    chunks = []
    for i in range(0, audio_length_ms, chunk_size_ms):
        start = i
        end = min(i + chunk_size_ms, audio_length_ms)
        chunks.append(audio[start:end])
    
    # Single chunk - process directly without multiprocessing overhead
    if len(chunks) == 1:
        args = (
            chunks[0].raw_data,
            chunks[0].sample_width,
            chunks[0].frame_rate,
            chunks[0].channels,
            kwargs
        )
        return [chunk_processor_func(args)]
    
    # Multiple chunks - use parallel processing
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        args_list = [
            (chunk.raw_data, chunk.sample_width, chunk.frame_rate, chunk.channels, kwargs)
            for chunk in chunks
        ]
        results = list(executor.map(chunk_processor_func, args_list))
    
    return results


def _process_chunk_for_nonsilence(chunk_bytes, sample_width, frame_rate, channels, silence_threshold):
    from pydub import AudioSegment
    from pydub.silence import detect_nonsilent
    chunk = AudioSegment(
        data=chunk_bytes,
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=channels
    )
    ranges = detect_nonsilent(
        chunk,
        min_silence_len=100,
        silence_thresh=silence_threshold
    )
    return sum(end - start for start, end in ranges)

def _unpack_args_for_nonsilence(args):
    chunk_bytes, sample_width, frame_rate, channels, kwargs = args
    silence_threshold = kwargs.get('silence_threshold', -50)
    return _process_chunk_for_nonsilence(chunk_bytes, sample_width, frame_rate, channels, silence_threshold)


def _process_chunk_for_max_dbfs(chunk_bytes, sample_width, frame_rate, channels):
    """Process a chunk to find maximum dBFS."""
    from pydub import AudioSegment
    chunk = AudioSegment(
        data=chunk_bytes,
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=channels
    )
    return chunk.max_dBFS


def _unpack_args_for_max_dbfs(args):
    chunk_bytes, sample_width, frame_rate, channels, kwargs = args
    return _process_chunk_for_max_dbfs(chunk_bytes, sample_width, frame_rate, channels)


def _process_chunk_for_min_dbfs(chunk_bytes, sample_width, frame_rate, channels):
    """Process a chunk to find minimum non-zero sample for dBFS calculation."""
    from pydub import AudioSegment
    import numpy as np
    
    chunk = AudioSegment(
        data=chunk_bytes,
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=channels
    )
    
    samples = np.array(chunk.get_array_of_samples())
    non_zero_samples = samples[samples != 0]
    
    if len(non_zero_samples) > 0:
        return np.abs(non_zero_samples).min()
    return None


def _unpack_args_for_min_dbfs(args):
    chunk_bytes, sample_width, frame_rate, channels, kwargs = args
    return _process_chunk_for_min_dbfs(chunk_bytes, sample_width, frame_rate, channels)

class AudioProcessor:
    """Process audio files and provide statistics and effects."""
    
    def __init__(self, filepath):
        """Initialize with an audio file path."""
        self.filepath = filepath
        self.audio = self._load_audio(filepath)
        
    def _load_audio(self, filepath):
        """Load audio file using pydub."""
        file_extension = os.path.splitext(filepath)[1].lower()
        
        if file_extension == '.mp3':
            return AudioSegment.from_mp3(filepath)
        elif file_extension == '.aac':
            return AudioSegment.from_file(filepath, format='aac')
        elif file_extension == '.ac3':
            return AudioSegment.from_file(filepath, format='ac3')
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def get_statistics(self):
        """Get audio file statistics using multi-threaded analysis."""
        # Get max dBFS using multi-threaded processing
        max_dbfs = self._calculate_max_dbfs()
        
        # Get min dBFS using multi-threaded processing
        min_dbfs = self._calculate_min_dbfs()
        
        # Get total duration in seconds
        duration_seconds = len(self.audio) / 1000.0
        
        # Calculate non-silence duration using multi-threaded processing
        # Threshold for silence: -50 dBFS (reasonable default)
        silence_threshold = -50
        non_silent_duration = self._calculate_non_silence_duration(silence_threshold)
        
        return {
            'max_dbfs': round(max_dbfs, 2),
            'min_dbfs': round(min_dbfs, 2) if isinstance(min_dbfs, (int, float)) and not np.isnan(min_dbfs) else None,
            'duration_seconds': round(duration_seconds, 2),
            'non_silence_seconds': round(non_silent_duration, 2),
            'silence_threshold_db': silence_threshold,
            'sample_rate': self.audio.frame_rate,
            'channels': self.audio.channels,
            'sample_width': self.audio.sample_width
        }
    
    def _calculate_max_dbfs(self):
        """Calculate maximum dBFS using multi-threaded processing."""
        results = _parallel_process_audio_chunks(
            self.audio,
            _process_chunk_for_max_dbfs,
            _unpack_args_for_max_dbfs
        )
        # Return the maximum dBFS from all chunks
        return max(results)
    
    def _calculate_min_dbfs(self):
        """Calculate minimum dBFS using multi-threaded processing."""
        results = _parallel_process_audio_chunks(
            self.audio,
            _process_chunk_for_min_dbfs,
            _unpack_args_for_min_dbfs
        )
        
        # Filter out None values and find minimum amplitude
        valid_results = [r for r in results if r is not None]
        
        if len(valid_results) == 0:
            return -float('inf')
        
        min_amplitude = min(valid_results)
        max_possible = 2 ** (self.audio.sample_width * 8 - 1)
        ratio = min_amplitude / max_possible
        
        if ratio > 0:
            return 20 * np.log10(ratio)
        return None
    
    def _calculate_non_silence_duration(self, silence_threshold=-50):
        """Calculate the duration of non-silent parts of the audio using parallel chunk processing."""
        results = _parallel_process_audio_chunks(
            self.audio,
            _process_chunk_for_nonsilence,
            _unpack_args_for_nonsilence,
            silence_threshold=silence_threshold
        )
        
        # Sum all non-silent durations from chunks
        total_nonsilent_ms = sum(results)
        return total_nonsilent_ms / 1000.0
    
    def _extract_segment(self, start_time: Optional[float] = None, end_time: Optional[float] = None) -> AudioSegment:
        """
        Extract a segment of audio from start_time to end_time.
        
        Args:
            start_time: Start time in seconds (default: None - from beginning)
            end_time: End time in seconds (default: None - to end)
        
        Returns:
            AudioSegment object containing the specified segment
        """
        # If no times specified, return the full audio
        if start_time is None and end_time is None:
            return self.audio
        
        # Convert times to milliseconds (pydub uses milliseconds)
        start_ms = int(start_time * 1000) if start_time is not None else 0
        end_ms = int(end_time * 1000) if end_time is not None else len(self.audio)
        
        # Ensure times are within bounds
        start_ms = max(0, min(start_ms, len(self.audio)))
        end_ms = max(start_ms, min(end_ms, len(self.audio)))
        
        # Extract and return the segment
        return self.audio[start_ms:end_ms]
    
    def apply_compressor(self, threshold: float = -20.0, ratio: float = 4.0, attack: float = 5.0, release: float = 50.0, start_time: Optional[float] = None, end_time: Optional[float] = None) -> str:
        """
        Apply compression to audio.
        
        Args:
            threshold: Threshold in dBFS (default: -20)
            ratio: Compression ratio (default: 4)
            attack: Attack time in ms (default: 5)
            release: Release time in ms (default: 50)
            start_time: Start time in seconds for processing (default: None - process from beginning)
            end_time: End time in seconds for processing (default: None - process to end)
        
        Returns:
            Path to processed audio file
        """
        # Extract segment if start_time or end_time is specified
        audio_to_process = self._extract_segment(start_time, end_time)
        
        # Apply dynamic range compression using pydub
        compressed = compress_dynamic_range(
            audio_to_process,
            threshold=threshold,
            ratio=ratio,
            attack=attack,
            release=release
        )
        
        # Generate output filename
        base_name = os.path.splitext(os.path.basename(self.filepath))[0]
        output_path = os.path.join(
            tempfile.gettempdir(),
            f"{base_name}_compressed.mp3"
        )
        
        # Export as mp3
        compressed.export(output_path, format='mp3')
        return output_path
    
    def apply_limiter(self, threshold: float = -1.0, release: float = 50.0, start_time: Optional[float] = None, end_time: Optional[float] = None) -> str:
        """
        Apply limiting to audio (extreme compression with high ratio).
        
        Args:
            threshold: Threshold in dBFS (default: -1)
            release: Release time in ms (default: 50)
            start_time: Start time in seconds for processing (default: None - process from beginning)
            end_time: End time in seconds for processing (default: None - process to end)
        
        Returns:
            Path to processed audio file
        """
        # Extract segment if start_time or end_time is specified
        audio_to_process = self._extract_segment(start_time, end_time)
        
        # A limiter is essentially a compressor with a very high ratio
        # We use ratio of 100:1 for limiting
        limited = compress_dynamic_range(
            audio_to_process,
            threshold=threshold,
            ratio=100,
            attack=0.1,  # Very fast attack for limiting
            release=release
        )
        
        # Normalize to prevent clipping
        limited = normalize(limited, headroom=0.1)
        
        # Generate output filename
        base_name = os.path.splitext(os.path.basename(self.filepath))[0]
        output_path = os.path.join(
            tempfile.gettempdir(),
            f"{base_name}_limited.mp3"
        )
        
        # Export as mp3
        limited.export(output_path, format='mp3')
        return output_path
