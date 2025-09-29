"""
Enhanced gallery generator with ZIP extraction and download capabilities
"""

import json
import shutil
from pathlib import Path
from typing import List, Dict, Any

from .config import GALLERY_TITLE
from .utils import parse_folder_name, read_post_text, check_ffmpeg
from .enhanced_media import EnhancedMediaProcessor
from .template_loader import TemplateLoader

# Try to import download functionality
try:
    from .downloader import ContentDownloader
    DOWNLOAD_AVAILABLE = True
except ImportError:
    DOWNLOAD_AVAILABLE = False


class EnhancedArtGalleryGenerator:
    """Enhanced gallery generator with ZIP extraction and comprehensive file preservation."""
    
    def __init__(self, art_directory: Path, output_directory: str = "gallery", 
                 verbose: bool = False, extract_zips: bool = True, download_content: bool = False):
        self.art_dir = Path(art_directory)
        self.output_dir = Path(output_directory)
        self.verbose = verbose
        self.extract_zips = extract_zips
        self.download_content = download_content and DOWNLOAD_AVAILABLE
        
        self.media_processor = EnhancedMediaProcessor(
            self.output_dir, 
            verbose, 
            extract_zips=extract_zips
        )
        self.template_loader = TemplateLoader()
        
        # Initialize downloader if requested and available
        self.downloader = None
        if self.download_content:
            self.downloader = ContentDownloader(verbose=verbose)
        elif download_content and not DOWNLOAD_AVAILABLE:
            if verbose:
                print("⚠️  Download functionality requested but ContentDownloader not available")
        
        self.extraction_stats = {
            'total_zips_processed': 0,
            'total_files_extracted': 0,
            'artwork_files_preserved': 0,
            'posts_with_extractions': 0
        }
        
        self.download_stats = {
            'posts_processed': 0,
            'links_found': 0,
            'files_downloaded': 0,
            'download_failures': 0
        }
    
    def scan_posts(self) -> List[Dict[str, Any]]:
        """Scan all posts and return structured data."""
        posts = []
        
        if not self.media_processor.ffmpeg_available:
            if self.verbose:
                print("⚠️  Warning: ffmpeg not found. Video thumbnails will not be generated.")
                print("   Install ffmpeg to enable video thumbnail generation.")
        
        if self.extract_zips and self.verbose:
            print("🔧 ZIP extraction enabled - preserving all file types including .psd, .clip, etc.")
        
        if self.download_content and self.verbose:
            print("📥 Content downloading enabled - will attempt to download from links in posts")
        
        for artist_dir in self.art_dir.iterdir():
            if not artist_dir.is_dir():
                continue
                
            artist_name = artist_dir.name
            if self.verbose:
                print(f"🎨 Processing artist: {artist_name}")
            
            for post_dir in artist_dir.iterdir():
                if not post_dir.is_dir() or post_dir.name == "extracted":
                    continue
                
                if self.verbose:
                    print(f"  📂 Processing post: {post_dir.name}")
                
                # Check for ZIP files before processing
                zip_files = list(post_dir.glob('*.zip'))
                if zip_files and self.verbose:
                    print(f"      🔍 Found {len(zip_files)} ZIP file(s) to process")
                
                date_obj, title = parse_folder_name(post_dir.name)
                post_text = read_post_text(post_dir)
                
                # Process downloads if enabled
                if self.download_content and self.downloader:
                    if self.verbose:
                        print(f"      📥 Processing links for downloads...")
                    
                    downloaded_files = self.downloader.process_post_links(post_dir, artist_name, title)
                    if downloaded_files:
                        self.download_stats['posts_processed'] += 1
                        self.download_stats['files_downloaded'] += len(downloaded_files)
                        if self.verbose:
                            print(f"      ✅ Downloaded {len(downloaded_files)} files")
                    else:
                        if self.verbose and post_text:
                            print(f"      ℹ️  No downloadable content found in links")
                
                media_files = self.media_processor.get_media_files(post_dir)
                
                # Update extraction statistics
                if zip_files:
                    self.extraction_stats['total_zips_processed'] += len(zip_files)
                    extraction_summary = self.media_processor.get_extraction_summary(post_dir)
                    if extraction_summary.get('total', 0) > 0:
                        self.extraction_stats['posts_with_extractions'] += 1
                        self.extraction_stats['total_files_extracted'] += extraction_summary['total']
                        self.extraction_stats['artwork_files_preserved'] += extraction_summary.get('artwork_files', 0)
                
                if media_files:  # Only include posts with media
                    copied_media = self.media_processor.copy_media_files(
                        artist_name, title, media_files
                    )
                    
                    thumbnail = self.media_processor.select_thumbnail(copied_media)
                    
                    # Add extraction info to post data
                    post_data = {
                        'artist': artist_name,
                        'title': title,
                        'date': date_obj.isoformat(),
                        'text': post_text,
                        'media': copied_media,
                        'thumbnail': thumbnail
                    }
                    
                    # Add extraction summary if files were extracted
                    if zip_files:
                        extraction_summary = self.media_processor.get_extraction_summary(post_dir)
                        if extraction_summary.get('total', 0) > 0:
                            post_data['extraction_summary'] = extraction_summary
                    
                    posts.append(post_data)
        
        # Sort by date, newest first
        posts.sort(key=lambda x: x['date'], reverse=True)
        return posts
    
    def generate(self) -> None:
        """Generate the gallery with enhanced ZIP extraction."""
        # Clean up and create fresh output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        if self.verbose:
            print("🔍 Scanning posts...")
        posts = self.scan_posts()
        
        if self.verbose:
            print(f"📊 Found {len(posts)} posts")
            self._print_debug_info()
            self._print_extraction_stats()
            self._print_download_stats()
        
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
            self._print_summary(posts)
    
    def _print_debug_info(self) -> None:
        """Print debug information about generated files."""
        media_dir = self.output_dir / "media"
        thumbs_dir = self.output_dir / "thumbnails"
        
        if media_dir.exists():
            media_count = sum(1 for f in media_dir.rglob('*') if f.is_file())
            print(f"📄 Copied {media_count} media files")
        
        if thumbs_dir.exists():
            thumb_count = sum(1 for f in thumbs_dir.rglob('*') if f.is_file())
            print(f"🖼️ Generated {thumb_count} video thumbnails")
    
    def _print_extraction_stats(self) -> None:
        """Print statistics about ZIP extraction."""
        if not self.extract_zips:
            return
            
        stats = self.extraction_stats
        if stats['total_zips_processed'] > 0:
            print(f"\n📦 ZIP Extraction Summary:")
            print(f"   📁 ZIP files processed: {stats['total_zips_processed']}")
            print(f"   📂 Posts with extractions: {stats['posts_with_extractions']}")
            print(f"   📄 Total files extracted: {stats['total_files_extracted']}")
            print(f"   🎨 Artwork files preserved: {stats['artwork_files_preserved']}")
            print(f"   💾 All files saved to 'extracted/' folders for future access")
        else:
            print(f"📦 No ZIP files found to extract")
    
    def _print_download_stats(self) -> None:
        """Print statistics about content downloading."""
        if not self.download_content:
            return
            
        stats = self.download_stats
        if stats['posts_processed'] > 0:
            print(f"\n📥 Download Summary:")
            print(f"   📂 Posts with downloads: {stats['posts_processed']}")
            print(f"   📄 Files downloaded: {stats['files_downloaded']}")
            if stats['download_failures'] > 0:
                print(f"   ❌ Download failures: {stats['download_failures']}")
            print(f"   💾 Downloaded files saved to 'downloads/' folders")
        elif self.downloader:
            print(f"📥 No downloadable content found in link files")
    
    def _print_summary(self, posts: List[Dict[str, Any]]) -> None:
        """Print summary of the first post for debugging."""
        if posts:
            print("\n📋 First post example:")
            post = posts[0]
            print(f"  Artist: {post['artist']}")
            print(f"  Title: {post['title']}")
            print(f"  Thumbnail: {post['thumbnail']}")
            print(f"  Media count: {len(post['media'])}")
            
            # Show extraction info if available
            if 'extraction_summary' in post:
                summary = post['extraction_summary']
                print(f"  Extracted files: {summary['total']} total")
                if summary.get('artwork_files', 0) > 0:
                    print(f"    🎨 Artwork files: {summary['artwork_files']}")
                if summary.get('images', 0) > 0:
                    print(f"    🖼️ Images: {summary['images']}")
                if summary.get('videos', 0) > 0:
                    print(f"    🎬 Videos: {summary['videos']}")
            
            # Show video thumbnails if any
            for media in post['media']:
                if media['type'] == 'video' and media.get('thumbnail'):
                    print(f"  Video thumbnail: {media['thumbnail']}")
                if media.get('extracted', False):
                    print(f"  Extracted media: {media['filename']}")
    
    def get_extraction_report(self) -> Dict[str, Any]:
        """Get detailed report of extraction activities."""
        return {
            'extraction_enabled': self.extract_zips,
            'download_enabled': self.download_content,
            'statistics': self.extraction_stats.copy(),
            'download_statistics': self.download_stats.copy(),
            'supported_artwork_formats': [
                '.psd', '.clip', '.ai', '.xcf', '.kra', '.sai', '.sketch', 
                '.fig', '.afdesign', '.afphoto'
            ],
            'supported_media_formats': [
                '.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.webm', '.mov', '.avi'
            ]
        }