"""
Video processing utilities for the Art Gallery Generator
"""

import subprocess
from pathlib import Path
from typing import Optional

from .config import (
    THUMBNAIL_SIZE, 
    THUMBNAIL_TIMESTAMP_PERCENT, 
    MIN_THUMBNAIL_TIMESTAMP, 
    MAX_THUMBNAIL_TIMESTAMP
)


class VideoProcessor:
    """Handles video thumbnail generation using ffmpeg."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def get_video_duration(self, video_path: Path) -> Optional[float]:
        """
        Get video duration in seconds using ffprobe.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Duration in seconds or None if failed
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-show_entries', 'format=duration',
                '-of', 'csv=p=0',
                str(video_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration
        except Exception as e:
            if self.verbose:
                print(f"    Error getting duration for {video_path.name}: {e}")
        return None
    
    def get_optimal_thumbnail_timestamp(self, video_path: Path) -> str:
        """
        Get optimal timestamp for thumbnail (around 10% into video, but not too early).
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Timestamp string in HH:MM:SS format
        """
        duration = self.get_video_duration(video_path)
        if duration:
            # Take thumbnail at configured percent of video duration, but within bounds
            timestamp_seconds = max(
                MIN_THUMBNAIL_TIMESTAMP, 
                min(duration * THUMBNAIL_TIMESTAMP_PERCENT, MAX_THUMBNAIL_TIMESTAMP)
            )
            # Convert to HH:MM:SS format
            hours = int(timestamp_seconds // 3600)
            minutes = int((timestamp_seconds % 3600) // 60)
            seconds = int(timestamp_seconds % 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return "00:00:01"  # Default fallback
    
    def generate_thumbnail(self, video_path: Path, output_path: Path, 
                          timestamp: Optional[str] = None) -> bool:
        """
        Generate a thumbnail from a video file using ffmpeg.
        
        Args:
            video_path: Path to the source video
            output_path: Path where thumbnail should be saved
            timestamp: Optional timestamp (uses optimal if not provided)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Use provided timestamp or calculate optimal one
            if timestamp is None:
                timestamp = self.get_optimal_thumbnail_timestamp(video_path)
            
            # ffmpeg command to extract frame at timestamp
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-ss', timestamp,  # Seek to timestamp
                '-vframes', '1',   # Extract only 1 frame
                '-f', 'image2',    # Output format
                '-vf', f'scale={THUMBNAIL_SIZE}:force_original_aspect_ratio=decrease,pad={THUMBNAIL_SIZE}:(ow-iw)/2:(oh-ih)/2:black',
                '-y',              # Overwrite output file
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_path.exists():
                if self.verbose:
                    print(f"    ✅ Generated thumbnail: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"    ❌ Failed to generate thumbnail for {video_path.name}: {result.stderr}")
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"    ❌ Error generating thumbnail for {video_path.name}: {e}")
            return False