"""
Utility functions for the Art Gallery Generator
"""

import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional

from .config import SUPPORTED_IMAGE_FORMATS, SUPPORTED_VIDEO_FORMATS


def should_skip_file(file_path: Path) -> bool:
    """
    Check if a file should be skipped during processing.
    Filters out AppleDouble files, system files, and other unwanted content.
    
    This is the centralized filtering function used throughout the application
    to ensure consistent filtering behavior.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if file should be skipped, False otherwise
        
    Example:
        >>> should_skip_file(Path("._myfile.jpg"))
        True
        >>> should_skip_file(Path(".DS_Store"))
        True
        >>> should_skip_file(Path("myfile.jpg"))
        False
    """
    filename = file_path.name
    
    # Skip system and metadata files
    skip_patterns = [
        '._',           # AppleDouble files (macOS resource forks)
        '.DS_Store',    # macOS directory metadata  
        'Thumbs.db',    # Windows thumbnail cache
        'desktop.ini',  # Windows folder settings
        '__MACOSX',     # macOS compression artifacts
    ]
    
    # Check if filename starts with any skip pattern
    for pattern in skip_patterns:
        if filename.startswith(pattern):
            return True
    
    # Skip other hidden files (starting with .)
    if filename.startswith('.'):
        return True
    
    # Skip links files
    if filename.startswith('links-'):
        return True
    
    # Skip ZIP files (they should be extracted, not displayed)
    if file_path.suffix.lower() == '.zip':
        return True
        
    return False


def check_ffmpeg() -> bool:
    """Check if ffmpeg is available on the system."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def parse_folder_name(folder_name: str) -> Tuple[datetime, str]:
    """
    Extract date and title from folder name.
    
    Args:
        folder_name: The folder name to parse
        
    Returns:
        Tuple of (date_object, title)
    """
    # Try to match YYYY-MM-DD format at the start
    date_match = re.match(r'^(\d{4}-\d{2}-\d{2})', folder_name)
    if date_match:
        date_str = date_match.group(1)
        title = re.sub(r'^\d{4}-\d{2}-\d{2}[-\s]*', '', folder_name)
    else:
        # Try alternative formats like "2023-03-24 19-10-津島善子"
        alt_match = re.match(r'^(\d{4}-\d{2}-\d{2})\s+\d{2}-\d{2}-(.+)', folder_name)
        if alt_match:
            date_str = alt_match.group(1)
            title = alt_match.group(2)
        else:
            date_str = "1970-01-01"
            title = folder_name
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        date_obj = datetime(1970, 1, 1)
        
    return date_obj, title


def clean_text_for_js(content: str) -> str:
    """
    Clean and escape text content for safe JavaScript embedding.
    
    Args:
        content: Raw text content
        
    Returns:
        Cleaned and escaped text
    """
    # Clean up content and escape for JavaScript
    content = content.replace('\r\n', '\\n').replace('\r', '\\n').replace('\n', '\\n')
    # Remove any problematic characters and escape quotes
    content = content.replace('"', '\\"').replace("'", "\\'")
    content = ''.join(char for char in content if ord(char) >= 32 or char in '\\n\\t')
    return content


def make_safe_filename(name: str) -> str:
    """
    Convert a string to a safe filename by replacing problematic characters.
    
    Args:
        name: Original name
        
    Returns:
        Safe filename
    """
    return re.sub(r'[^\w\-_\.]', '_', name)


def get_media_type(file_path: Path) -> Optional[str]:
    """
    Determine the media type of a file based on its extension.
    
    Also filters out files that should be skipped (AppleDouble, system files, etc.)
    
    Args:
        file_path: Path to the file
        
    Returns:
        Media type ('image', 'gif', 'video') or None if unsupported or should be skipped
    """
    # First check if file should be skipped
    if should_skip_file(file_path):
        return None
    
    ext = file_path.suffix.lower()
    
    if ext == '.gif':
        return 'gif'
    elif ext in SUPPORTED_IMAGE_FORMATS and ext != '.gif':
        return 'image'
    elif ext in SUPPORTED_VIDEO_FORMATS:
        return 'video'
    
    return None


def read_post_text(post_dir: Path) -> str:
    """
    Read content from links-*.txt file in the post directory.
    
    Args:
        post_dir: Path to the post directory
        
    Returns:
        Text content or empty string if no file found
    """
    txt_files = list(post_dir.glob('links-*.txt'))
    if txt_files:
        try:
            with open(txt_files[0], 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return clean_text_for_js(content)
        except Exception:
            pass
    return ""
