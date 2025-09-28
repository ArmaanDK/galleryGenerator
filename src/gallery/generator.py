"""
Main gallery generator class
"""

import json
import shutil
from pathlib import Path
from typing import List, Dict, Any

from .config import GALLERY_TITLE
from .utils import parse_folder_name, read_post_text, check_ffmpeg
from .media import MediaProcessor
from .template_loader import TemplateLoader


class ArtGalleryGenerator:
    """Main class for generating art galleries."""
    
    def __init__(self, art_directory: Path, output_directory: str = "gallery", 
                 verbose: bool = False):
        self.art_dir = Path(art_directory)
        self.output_dir = Path(output_directory)
        self.verbose = verbose
        self.media_processor = MediaProcessor(self.output_dir, verbose)
        self.template_loader = TemplateLoader()
        
        # Statistics tracking
        self.stats = {
            'total_posts': 0,
            'total_media': 0,
            'zip_files_processed': 0,
            'extracted_media_files': 0,
            'video_thumbnails': 0,
            'artists': set()
        }
    
    def scan_posts(self) -> List[Dict[str, Any]]:
        """
        Scan all posts and return structured data.
        
        Returns:
            List of post dictionaries
        """
        posts = []
        
        if not self.media_processor.ffmpeg_available:
            if self.verbose:
                print("⚠️  Warning: ffmpeg not found. Video thumbnails will not be generated.")
                print("   Install ffmpeg to enable video thumbnail generation.")
        
        for artist_dir in self.art_dir.iterdir():
            if not artist_dir.is_dir():
                continue
                
            artist_name = artist_dir.name
            self.stats['artists'].add(artist_name)
            
            if self.verbose:
                print(f"🎨 Processing artist: {artist_name}")
            
            for post_dir in artist_dir.iterdir():
                if not post_dir.is_dir():
                    continue
                
                if self.verbose:
                    print(f"  📂 Processing post: {post_dir.name}")
                
                # Check for ZIP files before processing
                zip_count = len(list(post_dir.glob('*.zip')))
                if zip_count > 0 and self.verbose:
                    print(f"    📦 Found {zip_count} ZIP file{'s' if zip_count > 1 else ''}")
                
                date_obj, title = parse_folder_name(post_dir.name)
                post_text = read_post_text(post_dir)
                media_files = self.media_processor.get_media_files(post_dir)
                
                # Count extracted files for statistics
                extracted_files = [m for m in media_files if m.get('is_extracted')]
                if extracted_files:
                    self.stats['extracted_media_files'] += len(extracted_files)
                    if zip_count > 0:
                        self.stats['zip_files_processed'] += zip_count
                
                if media_files:  # Only include posts with media
                    copied_media = self.media_processor.copy_media_files(
                        artist_name, title, media_files
                    )
                    
                    # Count video thumbnails
                    video_thumbnails = [m for m in copied_media if m.get('thumbnail')]
                    self.stats['video_thumbnails'] += len(video_thumbnails)
                    
                    thumbnail = self.media_processor.select_thumbnail(copied_media)
                    
                    posts.append({
                        'artist': artist_name,
                        'title': title,
                        'date': date_obj.isoformat(),
                        'text': post_text,
                        'media': copied_media,
                        'thumbnail': thumbnail
                    })
                    
                    self.stats['total_posts'] += 1
                    self.stats['total_media'] += len(copied_media)
        
        # Sort by date, newest first
        posts.sort(key=lambda x: x['date'], reverse=True)
        return posts
    
    def generate(self) -> None:
        """Generate the gallery."""
        # Clean up and create fresh output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        if self.verbose:
            print("📂 Scanning posts and processing archives...")
        posts = self.scan_posts()
        
        if self.verbose:
            self._print_scan_summary()
        
        if self.verbose:
            print("🌐 Generating HTML...")
        
        html_content = self.template_loader.render_gallery(
            posts=posts,
            gallery_title=GALLERY_TITLE
        )
        
        # Write HTML file
        with open(self.output_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        if self.verbose:
            self._print_final_summary(posts)
    
    def _print_scan_summary(self) -> None:
        """Print summary of the scanning process."""
        print(f"📊 Scan Summary:")
        print(f"   Artists: {len(self.stats['artists'])}")
        print(f"   Posts: {self.stats['total_posts']}")
        print(f"   Media files: {self.stats['total_media']}")
        
        if self.stats['zip_files_processed'] > 0:
            print(f"   📦 ZIP files processed: {self.stats['zip_files_processed']}")
            print(f"   📁 Media files extracted: {self.stats['extracted_media_files']}")
        
        if self.stats['video_thumbnails'] > 0:
            print(f"   🖼️  Video thumbnails: {self.stats['video_thumbnails']}")
    
    def _print_debug_info(self) -> None:
        """Print debug information about generated files."""
        media_dir = self.output_dir / "media"
        thumbs_dir = self.output_dir / "thumbnails"
        
        if media_dir.exists():
            media_count = sum(1 for f in media_dir.rglob('*') if f.is_file())
            print(f"📄 Copied {media_count} media files")
        
        if thumbs_dir.exists():
            thumb_count = sum(1 for f in thumbs_dir.rglob('*') if f.is_file())
            print(f"🖼️  Generated {thumb_count} video thumbnails")
    
    def _print_final_summary(self, posts: List[Dict[str, Any]]) -> None:
        """Print final summary and example."""
        self._print_debug_info()
        
        if posts:
            print("\n📋 Example post:")
            post = posts[0]
            print(f"   Artist: {post['artist']}")
            print(f"   Title: {post['title']}")
            print(f"   Thumbnail: {post['thumbnail']}")
            print(f"   Media count: {len(post['media'])}")
            
            # Show extracted files if any
            extracted = [m for m in post['media'] if m.get('is_extracted')]
            if extracted:
                print(f"   Extracted files: {len(extracted)}")
                for media in extracted[:3]:  # Show first 3
                    print(f"     - {media['filename']}")
                if len(extracted) > 3:
                    print(f"     ... and {len(extracted) - 3} more")
            
            # Show video thumbnails if any
            video_thumbs = [m for m in post['media'] if m['type'] == 'video' and m.get('thumbnail')]
            if video_thumbs:
                print(f"   Video thumbnails: {len(video_thumbs)}")