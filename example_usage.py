#!/usr/bin/env python3
"""
Example usage of the AudioProcessor class for command-line processing.
This demonstrates the audio processing capabilities without the web interface.

Usage:
    python example_usage.py <input_audio_file>
    
Example:
    python example_usage.py sample.mp3
"""

import sys
import os
from audio_processor import AudioProcessor

def main():
    if len(sys.argv) < 2:
        print("Usage: python example_usage.py <input_audio_file>")
        print("Example: python example_usage.py sample.mp3")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    print(f"Processing: {input_file}\n")
    
    try:
        # Initialize processor
        processor = AudioProcessor(input_file)
        
        # Get statistics
        print("=" * 60)
        print("AUDIO STATISTICS")
        print("=" * 60)
        stats = processor.get_statistics()
        
        print(f"Max Level:           {stats['max_dbfs']} dBFS")
        print(f"Min Level:           {stats['min_dbfs']} dBFS")
        print(f"Total Duration:      {stats['duration_seconds']} seconds")
        print(f"Non-Silence:         {stats['non_silence_seconds']} seconds")
        print(f"Silence Threshold:   {stats['silence_threshold_db']} dB")
        print(f"Sample Rate:         {stats['sample_rate']} Hz")
        print(f"Channels:            {stats['channels']}")
        print(f"Sample Width:        {stats['sample_width']} bytes")
        print()
        
        # Apply compressor
        print("=" * 60)
        print("APPLYING COMPRESSOR")
        print("=" * 60)
        print("Parameters: threshold=-20dB, ratio=4:1, attack=5ms, release=50ms")
        compressed_file = processor.apply_compressor(
            threshold=-20,
            ratio=4,
            attack=5,
            release=50
        )
        print(f"✓ Compressed file saved: {compressed_file}")
        print()
        
        # Apply limiter
        print("=" * 60)
        print("APPLYING LIMITER")
        print("=" * 60)
        print("Parameters: threshold=-1dB, release=50ms")
        limited_file = processor.apply_limiter(
            threshold=-1,
            release=50
        )
        print(f"✓ Limited file saved: {limited_file}")
        print()
        
        print("=" * 60)
        print("PROCESSING COMPLETE")
        print("=" * 60)
        print(f"Original:   {input_file}")
        print(f"Compressed: {compressed_file}")
        print(f"Limited:    {limited_file}")
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
