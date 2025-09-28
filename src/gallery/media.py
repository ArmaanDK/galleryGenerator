"""
Media file handling for the Art Gallery Generator
"""

import shutil
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional

from .utils import get_media_type, make_safe_filename
from .video import VideoProcessor


class MediaProcessor:
    """Handles copying and processing of media files."""
    
    def __init__(self, output_dir: Path, verbose: bool = False):
        self.output_dir = output_dir
        self.verbose = verbose
        self.video_processor = VideoProcessor(verbose)
        self._ffmpeg_available = None
    
    @property
    def ffmpeg_available(self) -> bool:
        """Check if ffmpeg is available (cached)."""
        if self._ffmpeg_available is None:
            from .utils import check_ffmpeg
            self._ffmpeg_available = check_ffmpeg()
        return self._ffmpeg_available
    
    def extract_zip_files(self, post_dir: Path) -> bool:
        """
        Extract ZIP files in the post directory to an 'extracted' subfolder.
        
        Args:
            post_dir: Path to the post directory
            
        Returns:
            True if any ZIP files were extracted, False otherwise
        """
        zip_files = list(post_dir.glob('*.zip'))
        if not zip_files:
            return False
        
        extracted_dir = post_dir / "extracted"
        any_extracted = False
        
        for zip_file in zip_files:
            if self.verbose:
                print(f"    📦 Found ZIP file: {zip_file.name}")
            
            try:
                # Create extracted directory if it doesn't exist
                extracted_dir.mkdir(exist_ok=True)
                
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    # Get list of files in the ZIP
                    file_list = zip_ref.namelist()
                    
                    # Filter for supported media files
                    media_files = []
                    for file_name in file_list:
                        file_path = Path(file_name)
                        if get_media_type(file_path) is not None:
                            media_files.append(file_name)
                    
                    if media_files:
                        if self.verbose:
                            print(f"      📁 Extracting {len(media_files)} media files from {zip_file.name}")
                        
                        # Extract only media files
                        for media_file in media_files:
                            try:
                                # Extract to extracted directory
                                zip_ref.extract(media_file, extracted_dir)
                                
                                # If the file was extracted in a subdirectory structure,
                                # move it to the root of extracted directory
                                extracted_file = extracted_dir / media_file
                                if extracted_file.exists() and extracted_file.parent != extracted_dir:
                                    # Create a safe filename to avoid conflicts
                                    safe_name = self._make_safe_extracted_filename(
                                        extracted_file.name, extracted_dir
                                    )
                                    final_path = extracted_dir / safe_name
                                    
                                    # Move file to root of extracted directory
                                    shutil.move(str(extracted_file), str(final_path))
                                    
                                    # Clean up empty subdirectories
                                    self._cleanup_empty_dirs(extracted_file.parent, extracted_dir)
                                
                                if self.verbose:
                                    print(f"        ✅ Extracted: {Path(media_file).name}")
                                    
                            except Exception as e:
                                if self.verbose:
                                    print(f"        ❌ Failed to extract {media_file}: {e}")
                        
                        any_extracted = True
                    else:
                        if self.verbose:
                            print(f"      ℹ️  No media files found in {zip_file.name}")
                
            except Exception as e:
                if self.verbose:
                    print(f"      ❌ Error processing {zip_file.name}: {e}")
        
        return any_extracted
    
    def _make_safe_extracted_filename(self, filename: str, extracted_dir: Path) -> str:
        """
        Create a safe filename for extracted files, avoiding conflicts.
        
        Args:
            filename: Original filename
            extracted_dir: Directory where file will be placed
            
        Returns:
            Safe filename that doesn't conflict with existing files
        """
        base_name = Path(filename).stem
        extension = Path(filename).suffix
        safe_base = make_safe_filename(base_name)
        
        counter = 1
        safe_name = f"{safe_base}{extension}"
        
        while (extracted_dir / safe_name).exists():
            safe_name = f"{safe_base}_{counter}{extension}"
            counter += 1
        
        return safe_name
    
    def _cleanup_empty_dirs(self, start_dir: Path, stop_dir: Path) -> None:
        """
        Remove empty directories up to but not including stop_dir.
        
        Args:
            start_dir: Directory to start cleaning from
            stop_dir: Directory to stop at (not removed)
        """
        current = start_dir
        while current != stop_dir and current.exists():
            try:
                if current.is_dir() and not list(current.iterdir()):
                    current.rmdir()
                    current = current.parent
                else:
                    break
            except OSError:
                break
    
    def get_media_files(self, post_dir: Path) -> List[Dict[str, Any]]:
        """
        Get all media files from post directory, including extracted files.
        First extracts any ZIP files found.
        
        Args:
            post_dir: Path to the post directory
            
        Returns:
            List of media file dictionaries
        """
        # First, try to extract any ZIP files
        if self.extract_zip_files(post_dir):
            if self.verbose:
                print(f"    🔄 ZIP extraction completed for {post_dir.name}")
        
        media_files = []
        
        # Get media files from the main directory
        for file_path in sorted(post_dir.iterdir()):
            if (file_path.is_file() and 
                not file_path.name.startswith('links-') and 
                not file_path.suffix.lower() == '.zip' and
                not file_path.suffix.lower() == '.psd'):  # Skip PSD files as they're not web-displayable
                
                media_type = get_media_type(file_path)
                if media_type:
                    media_files.append({
                        'type': media_type,
                        'filename': file_path.name,
                        'path': file_path
                    })
        
        # Get media files from extracted directory if it exists
        extracted_dir = post_dir / "extracted"
        if extracted_dir.exists() and extracted_dir.is_dir():
            for file_path in sorted(extracted_dir.iterdir()):
                if file_path.is_file():
                    media_type = get_media_type(file_path)
                    if media_type:
                        # Mark extracted files with a prefix for clarity
                        display_name = f"[extracted] {file_path.name}"
                        media_files.append({
                            'type': media_type,
                            'filename': display_name,
                            'path': file_path,
                            'is_extracted': True
                        })
        
        return media_files
    
    def copy_media_files(self, artist_name: str, post_title: str, 
                        media_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Copy media files to output directory and generate thumbnails.
        
        Args:
            artist_name: Name of the artist
            post_title: Title of the post
            media_files: List of media file dictionaries
            
        Returns:
            List of copied media file dictionaries with paths updated
        """
        # Create safe directory names
        safe_artist = make_safe_filename(artist_name)
        safe_title = make_safe_filename(post_title)
        
        media_dir = self.output_dir / "media" / safe_artist / safe_title
        media_dir.mkdir(parents=True, exist_ok=True)
        
        # Create thumbnails directory
        thumbs_dir = self.output_dir / "thumbnails" / safe_artist / safe_title
        thumbs_dir.mkdir(parents=True, exist_ok=True)
        
        copied_files = []
        
        for media in media_files:
            # Use original filename for file operations, but keep display name for UI
            original_filename = media['path'].name
            display_filename = media['filename']
            
            # Create unique filename if there are conflicts
            dest_filename = original_filename
            counter = 1
            while (media_dir / dest_filename).exists():
                name_parts = Path(original_filename)
                dest_filename = f"{name_parts.stem}_{counter}{name_parts.suffix}"
                counter += 1
            
            dest_path = media_dir / dest_filename
            
            try:
                shutil.copy2(media['path'], dest_path)
                if self.verbose:
                    extracted_indicator = " (extracted)" if media.get('is_extracted') else ""
                    print(f"    📄 Copied: {display_filename}{extracted_indicator}")
            except Exception as e:
                if self.verbose:
                    print(f"    ❌ Error copying {display_filename}: {e}")
                continue
            
            rel_path = dest_path.relative_to(self.output_dir)
            
            # Generate video thumbnail if needed
            thumbnail_path = None
            if media['type'] == 'video' and self.ffmpeg_available:
                thumbnail_path = self._generate_video_thumbnail(
                    media['path'], thumbs_dir, dest_filename
                )
            
            copied_files.append({
                'type': media['type'],
                'filename': display_filename,  # Use display name for UI
                'path': str(rel_path).replace('\\', '/'),
                'thumbnail': thumbnail_path,
                'is_extracted': media.get('is_extracted', False)
            })
        
        return copied_files
    
    def _generate_video_thumbnail(self, video_path: Path, thumbs_dir: Path, 
                                 filename: str) -> Optional[str]:
        """
        Generate thumbnail for a video file.
        
        Args:
            video_path: Path to the source video
            thumbs_dir: Directory to save thumbnails
            filename: Original filename
            
        Returns:
            Relative path to thumbnail or None if failed
        """
        thumb_filename = f"{Path(filename).stem}_thumb.jpg"
        thumb_path = thumbs_dir / thumb_filename
        
        if self.video_processor.generate_thumbnail(video_path, thumb_path):
            thumbnail_rel_path = thumb_path.relative_to(self.output_dir)
            return str(thumbnail_rel_path).replace('\\', '/')
        
        return None
    
    def select_thumbnail(self, media_files: List[Dict[str, Any]]) -> Optional[str]:
        """
        Select the best thumbnail from available media.
        
        Args:
            media_files: List of processed media files
            
        Returns:
            Path to the best thumbnail or None
        """
        # Prefer non-extracted images/gifs first, then extracted ones, then video thumbnails
        for media in media_files:
            if media['type'] in ['image', 'gif'] and not media.get('is_extracted'):
                return media['path']
        
        for media in media_files:
            if media['type'] in ['image', 'gif'] and media.get('is_extracted'):
                return media['path']
        
        for media in media_files:
            if media['type'] == 'video' and media.get('thumbnail'):
                return media['thumbnail']
        
        return None