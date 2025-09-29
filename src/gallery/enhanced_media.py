"""
Enhanced media file handling for the Art Gallery Generator with ZIP extraction
"""

import shutil
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional

from .utils import get_media_type, make_safe_filename, should_skip_file
from .video import VideoProcessor


class EnhancedMediaProcessor:
    """Enhanced media processor that handles ZIP extraction and preserves all file types."""
    
    def __init__(self, output_dir: Path, verbose: bool = False, extract_zips: bool = True):
        self.output_dir = output_dir
        self.verbose = verbose
        self.extract_zips = extract_zips
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
        Preserves ALL file types including .psd, .clip, etc.
        """
        if not self.extract_zips:
            return False
            
        zip_files = list(post_dir.glob('*.zip'))
        if not zip_files:
            return False
        
        extracted_dir = post_dir / "extracted"
        any_extracted = False
        
        for zip_file in zip_files:
            if self.verbose:
                print(f"    📦 Found ZIP file: {zip_file.name}")
            
            try:
                extracted_dir.mkdir(exist_ok=True)
                
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    file_list = zip_ref.namelist()
                    
                    # Define file types to extract (includes artwork files)
                    extractable_extensions = {
                        # Media files for gallery display
                        '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff',
                        '.mp4', '.webm', '.mov', '.avi', '.mkv', '.flv',
                        # Artwork source files for archival
                        '.psd', '.clip', '.ai', '.xcf', '.kra', '.ora', '.sai', '.sai2',
                        '.sketch', '.fig', '.afdesign', '.afphoto', '.afpub',
                        '.blend', '.c4d', '.max', '.ma', '.mb',
                        # Document files
                        '.pdf', '.txt', '.md', '.rtf', '.doc', '.docx',
                        # Other potentially useful files
                        '.svg', '.eps', '.dwg', '.dxf'
                    }
                    
                    # Filter for files we want to extract
                    extractable_files = []
                    for file_name in file_list:
                        file_path = Path(file_name)
                        
                        # Skip directories
                        if file_name.endswith('/'):
                            continue
                        
                        # Skip system files (AppleDouble, etc.)
                        if should_skip_file(file_path):
                            if self.verbose:
                                print(f"      ⏭️  Skipping system file in ZIP: {file_path.name}")
                            continue
                        
                        # Check if file has an extractable extension
                        if file_path.suffix.lower() in extractable_extensions:
                            extractable_files.append(file_name)
                        # Also extract files without extensions (might be images)
                        elif not file_path.suffix and len(file_path.name) > 0:
                            extractable_files.append(file_name)
                    
                    if extractable_files:
                        if self.verbose:
                            print(f"      📂 Extracting {len(extractable_files)} files from {zip_file.name}")
                        
                        # Extract files
                        for file_name in extractable_files:
                            try:
                                zip_ref.extract(file_name, extracted_dir)
                                
                                # If the file was extracted in a subdirectory structure,
                                # move it to the root of extracted directory
                                extracted_file = extracted_dir / file_name
                                if extracted_file.exists() and extracted_file.parent != extracted_dir:
                                    safe_name = self._make_safe_extracted_filename(
                                        extracted_file.name, extracted_dir
                                    )
                                    final_path = extracted_dir / safe_name
                                    shutil.move(str(extracted_file), str(final_path))
                                    self._cleanup_empty_dirs(extracted_file.parent, extracted_dir)
                                
                                if self.verbose:
                                    file_ext = Path(file_name).suffix.lower()
                                    if file_ext in ['.psd', '.clip', '.ai', '.xcf', '.kra', '.sai']:
                                        print(f"        🎨 Extracted artwork file: {Path(file_name).name}")
                                    elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                                        print(f"        🖼️ Extracted image: {Path(file_name).name}")
                                    elif file_ext in ['.mp4', '.webm', '.mov', '.avi']:
                                        print(f"        🎬 Extracted video: {Path(file_name).name}")
                                    else:
                                        print(f"        📄 Extracted file: {Path(file_name).name}")
                                    
                            except Exception as e:
                                if self.verbose:
                                    print(f"        ❌ Failed to extract {file_name}: {e}")
                        
                        any_extracted = True
                    else:
                        if self.verbose:
                            print(f"      ℹ️  No extractable files found in {zip_file.name}")
                
            except Exception as e:
                if self.verbose:
                    print(f"      ❌ Error processing {zip_file.name}: {e}")
        
        return any_extracted
    
    def _make_safe_extracted_filename(self, filename: str, extracted_dir: Path) -> str:
        """Create a safe filename for extracted files, avoiding conflicts."""
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
        """Remove empty directories up to but not including stop_dir."""
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
        First extracts any ZIP files found, preserving ALL file types.
        """
        # Skip processing if we're already in an extracted directory
        if post_dir.name == "extracted":
            return []
        
        # First, extract any ZIP files (this will preserve .psd, .clip, etc.)
        zip_extracted = self.extract_zip_files(post_dir)
        if zip_extracted and self.verbose:
            print(f"      ✅ ZIP extraction completed")
        
        media_files = []
        
        # Get files from main directory (only displayable media for gallery)
        for file_path in sorted(post_dir.iterdir()):
            if file_path.is_file() and not should_skip_file(file_path):
                media_type = get_media_type(file_path)
                if media_type:
                    media_files.append({
                        'type': media_type,
                        'filename': file_path.name,
                        'path': file_path,
                        'extracted': False
                    })
        
        # Get displayable media files from extracted directory for gallery
        extracted_dir = post_dir / "extracted"
        if extracted_dir.exists():
            for file_path in sorted(extracted_dir.iterdir()):
                if file_path.is_file() and not should_skip_file(file_path):
                    media_type = get_media_type(file_path)
                    if media_type:  # Only add displayable files to gallery
                        media_files.append({
                            'type': media_type,
                            'filename': f"[extracted] {file_path.name}",
                            'path': file_path,
                            'extracted': True
                        })
        
        return media_files
    
    def copy_media_files(self, artist_name: str, post_title: str, 
                        media_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Copy media files to output directory and generate thumbnails."""
        safe_artist = make_safe_filename(artist_name)
        safe_title = make_safe_filename(post_title)
        
        media_dir = self.output_dir / "media" / safe_artist / safe_title
        media_dir.mkdir(parents=True, exist_ok=True)
        
        thumbs_dir = self.output_dir / "thumbnails" / safe_artist / safe_title
        thumbs_dir.mkdir(parents=True, exist_ok=True)
        
        copied_files = []
        
        for media in media_files:
            dest_path = media_dir / media['filename']
            try:
                shutil.copy2(media['path'], dest_path)
                if self.verbose:
                    prefix = "📄" if not media.get('extracted', False) else "📂"
                    print(f"    {prefix} Copied: {media['filename']}")
            except Exception as e:
                if self.verbose:
                    print(f"    ❌ Error copying {media['filename']}: {e}")
                continue
            
            rel_path = dest_path.relative_to(self.output_dir)
            
            # Generate video thumbnail if needed
            thumbnail_path = None
            if media['type'] == 'video' and self.ffmpeg_available:
                thumbnail_path = self._generate_video_thumbnail(
                    media['path'], thumbs_dir, media['filename']
                )
            
            copied_files.append({
                'type': media['type'],
                'filename': media['filename'],
                'path': str(rel_path).replace('\\', '/'),
                'thumbnail': thumbnail_path,
                'extracted': media.get('extracted', False)
            })
        
        return copied_files
    
    def _generate_video_thumbnail(self, video_path: Path, thumbs_dir: Path, 
                                 filename: str) -> Optional[str]:
        """Generate thumbnail for a video file."""
        thumb_filename = f"{Path(filename).stem}_thumb.jpg"
        thumb_path = thumbs_dir / thumb_filename
        
        if self.video_processor.generate_thumbnail(video_path, thumb_path):
            thumbnail_rel_path = thumb_path.relative_to(self.output_dir)
            return str(thumbnail_rel_path).replace('\\', '/')
        
        return None
    
    def select_thumbnail(self, media_files: List[Dict[str, Any]]) -> Optional[str]:
        """Select the best thumbnail from available media."""
        # Prefer images/gifs, then video thumbnails
        for media in media_files:
            if media['type'] in ['image', 'gif']:
                return media['path']
            elif media['type'] == 'video' and media.get('thumbnail'):
                return media['thumbnail']
        
        # If no thumbnail found but we have videos, use the first video's thumbnail
        for media in media_files:
            if media['type'] == 'video' and media.get('thumbnail'):
                return media['thumbnail']
        
        return None
    
    def get_extraction_summary(self, post_dir: Path) -> Dict[str, int]:
        """Get summary of extracted files by type."""
        extracted_dir = post_dir / "extracted"
        if not extracted_dir.exists():
            return {}
        
        summary = {
            'artwork_files': 0,
            'images': 0,
            'videos': 0,
            'documents': 0,
            'other': 0,
            'total': 0
        }
        
        artwork_extensions = {'.psd', '.clip', '.ai', '.xcf', '.kra', '.sai', '.sketch'}
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        video_extensions = {'.mp4', '.webm', '.mov', '.avi', '.mkv'}
        document_extensions = {'.pdf', '.txt', '.md', '.rtf', '.doc'}
        
        for file_path in extracted_dir.iterdir():
            if file_path.is_file() and not should_skip_file(file_path):
                ext = file_path.suffix.lower()
                summary['total'] += 1
                
                if ext in artwork_extensions:
                    summary['artwork_files'] += 1
                elif ext in image_extensions:
                    summary['images'] += 1
                elif ext in video_extensions:
                    summary['videos'] += 1
                elif ext in document_extensions:
                    summary['documents'] += 1
                else:
                    summary['other'] += 1
        
        return summary
