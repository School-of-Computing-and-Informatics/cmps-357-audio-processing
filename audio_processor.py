import os
import tempfile
from typing import Optional
from pydub import AudioSegment
from pydub.effects import compress_dynamic_range, normalize
import numpy as np

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
        """Get audio file statistics."""
        # Get max and min dBFS levels
        max_dbfs = self.audio.max_dBFS
        
        # Calculate RMS (root mean square) as a measure of average level
        # Convert to numpy array for calculation
        samples = np.array(self.audio.get_array_of_samples())
        
        if len(samples) == 0:
            min_dbfs = -float('inf')
        else:
            # Find minimum non-zero sample to calculate min dBFS
            non_zero_samples = samples[samples != 0]
            if len(non_zero_samples) > 0:
                min_amplitude = np.abs(non_zero_samples).min()
                max_possible = 2 ** (self.audio.sample_width * 8 - 1)
                ratio = min_amplitude / max_possible
                if ratio > 0:
                    min_dbfs = 20 * np.log10(ratio)
                else:
                    min_dbfs = None
            else:
                min_dbfs = -float('inf')
        
        # Get total duration in seconds
        duration_seconds = len(self.audio) / 1000.0
        
        # Calculate non-silence duration
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
    
    def _calculate_non_silence_duration(self, silence_threshold=-50):
        """Calculate the duration of non-silent parts of the audio using parallel chunk processing for large files."""
        from pydub.silence import detect_nonsilent
        import concurrent.futures
        import math
        
        audio_length_ms = len(self.audio)
        num_workers = min(4, (os.cpu_count() or 2))  # Use up to 4 threads
        chunk_size_ms = max(10000, audio_length_ms // num_workers)  # At least 10s per chunk
        chunks = []
        for i in range(0, audio_length_ms, chunk_size_ms):
            start = i
            end = min(i + chunk_size_ms, audio_length_ms)
            chunks.append(self.audio[start:end])
        
        def process_chunk(chunk):
            ranges = detect_nonsilent(
                chunk,
                min_silence_len=100,
                silence_thresh=silence_threshold
            )
            return sum(end - start for start, end in ranges)
        
        total_nonsilent_ms = 0
        if len(chunks) == 1:
            total_nonsilent_ms = process_chunk(chunks[0])
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                results = list(executor.map(process_chunk, chunks))
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
