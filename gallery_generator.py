#!/usr/bin/env python3
"""
Art Gallery Generator - Main Entry Point
Generates a static HTML gallery from organized art directories.
"""

import sys
import re
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import List, Optional

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gallery.generator import ArtGalleryGenerator
from gallery.utils import read_post_text


class ContentDownloader:
    """Handles downloading content from various sources using built-in libraries."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        # Create opener with user agent to avoid blocking
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        ]
    
    def extract_links_from_text(self, text: str) -> List[str]:
        """Extract all URLs from text content."""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(url_pattern, text)
    
    def parse_google_drive_url(self, url: str) -> Optional[str]:
        """
        Convert Google Drive share URL to direct download URL.
        
        Args:
            url: Google Drive share URL
            
        Returns:
            Direct download URL or None if not a valid Google Drive URL
        """
        # Handle different Google Drive URL formats
        patterns = [
            r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
            r'https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                file_id = match.group(1)
                return f"https://drive.google.com/uc?export=download&id={file_id}"
        
        return None
    
    def get_filename_from_url(self, url: str, response_headers: dict) -> str:
        """Get filename from URL or response headers."""
        # Try to get filename from Content-Disposition header
        content_disposition = response_headers.get('Content-Disposition', '')
        if content_disposition and 'filename=' in content_disposition:
            filename_match = re.search(r'filename[*]?=([^;]+)', content_disposition)
            if filename_match:
                filename = filename_match.group(1).strip('"\'')
                return filename
        
        # Fallback to URL-based filename
        parsed_url = urllib.parse.urlparse(url)
        filename = Path(parsed_url.path).name or 'downloaded_file'
        
        # Add extension if missing based on content type
        if '.' not in filename:
            content_type = response_headers.get('content-type', '').lower()
            if 'image' in content_type:
                if 'jpeg' in content_type or 'jpg' in content_type:
                    filename += '.jpg'
                elif 'png' in content_type:
                    filename += '.png'
                elif 'gif' in content_type:
                    filename += '.gif'
                else:
                    filename += '.jpg'  # default
            elif 'video' in content_type:
                if 'mp4' in content_type:
                    filename += '.mp4'
                elif 'webm' in content_type:
                    filename += '.webm'
                else:
                    filename += '.mp4'  # default
            elif 'zip' in content_type or 'archive' in content_type:
                filename += '.zip'
            elif 'pdf' in content_type:
                filename += '.pdf'
        
        return filename
    
    def download_file(self, url: str, destination: Path, filename: Optional[str] = None) -> bool:
        """
        Download a file from URL to destination using urllib.
        
        Args:
            url: URL to download from
            destination: Directory to save file
            filename: Optional custom filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.verbose:
                print(f"    📥 Attempting to download: {url}")
            
            # Handle Google Drive URLs
            download_url = url
            if 'drive.google.com' in url:
                parsed_url = self.parse_google_drive_url(url)
                if not parsed_url:
                    if self.verbose:
                        print(f"    ❌ Could not parse Google Drive URL: {url}")
                    return False
                download_url = parsed_url
            
            # Make request
            request = urllib.request.Request(download_url)
            
            try:
                response = self.opener.open(request, timeout=30)
            except urllib.error.HTTPError as e:
                if self.verbose:
                    print(f"    ❌ HTTP Error {e.code}: {e.reason}")
                return False
            except urllib.error.URLError as e:
                if self.verbose:
                    print(f"    ❌ URL Error: {e.reason}")
                return False
            
            # Handle Google Drive's virus scan warning for large files
            content = response.read()
            content_str = content.decode('utf-8', errors='ignore')
            
            if 'drive.google.com' in download_url and 'virus scan warning' in content_str.lower():
                # Try to get the actual download link from the warning page
                confirm_match = re.search(r'confirm=([a-zA-Z0-9_-]+)', content_str)
                if confirm_match:
                    confirm_token = confirm_match.group(1)
                    download_url = f"{download_url}&confirm={confirm_token}"
                    
                    # Make new request with confirmation
                    request = urllib.request.Request(download_url)
                    try:
                        response = self.opener.open(request, timeout=30)
                        content = response.read()
                    except Exception as e:
                        if self.verbose:
                            print(f"    ❌ Error with confirmation token: {e}")
                        return False
            
            # Determine filename
            if not filename:
                filename = self.get_filename_from_url(download_url, dict(response.headers))
            
            # Ensure destination directory exists
            destination.mkdir(parents=True, exist_ok=True)
            
            # Save file
            file_path = destination / filename
            with open(file_path, 'wb') as f:
                f.write(content)
            
            file_size = len(content)
            if self.verbose:
                print(f"    ✅ Downloaded: {filename} ({file_size} bytes)")
            
            return True
            
        except Exception as e:
            if self.verbose:
                print(f"    ❌ Download failed: {e}")
            return False
    
    def process_post_links(self, post_dir: Path, artist_name: str, post_title: str) -> List[str]:
        """
        Process all links in a post and download available content.
        
        Args:
            post_dir: Path to post directory
            artist_name: Name of the artist
            post_title: Title of the post
            
        Returns:
            List of successfully downloaded files
        """
        # Read the links file
        text_content = read_post_text(post_dir)
        if not text_content:
            return []
        
        # Extract URLs
        urls = self.extract_links_from_text(text_content)
        if not urls:
            return []
        
        if self.verbose:
            print(f"  🔗 Found {len(urls)} links in {post_title}")
        
        # Create downloads directory
        downloads_dir = post_dir / "downloads"
        downloaded_files = []
        
        for url in urls:
            # Skip certain URLs that aren't direct content
            skip_patterns = [
                'patreon.com/c/',  # shop links
                '/shop',           # shop links
                'twitter.com',     # social media
                'instagram.com',   # social media
                'facebook.com',    # social media
                'discord.gg',      # social media
            ]
            
            if any(skip in url.lower() for skip in skip_patterns):
                if self.verbose:
                    print(f"    ⏭️  Skipping non-content link: {url}")
                continue
            
            # Attempt download
            if self.download_file(url, downloads_dir):
                downloaded_files.append(url)
        
        return downloaded_files


class EnhancedArtGalleryGenerator(ArtGalleryGenerator):
    """Enhanced gallery generator with optional download capabilities."""
    
    def __init__(self, art_directory: Path, output_directory: str = "gallery", 
                 verbose: bool = False, download_content: bool = False):
        super().__init__(art_directory, output_directory, verbose)
        self.download_content = download_content
        self.downloader = ContentDownloader(verbose) if download_content else None
    
    def scan_posts(self):
        """Enhanced post scanning with optional content downloading."""
        posts = []
        download_summary = {"attempted": 0, "successful": 0, "failed": 0}
        
        if not self.media_processor.ffmpeg_available:
            if self.verbose:
                print("⚠️  Warning: ffmpeg not found. Video thumbnails will not be generated.")
                print("   Install ffmpeg to enable video thumbnail generation.")
        
        for artist_dir in self.art_dir.iterdir():
            if not artist_dir.is_dir():
                continue
                
            artist_name = artist_dir.name
            if self.verbose:
                print(f"🎨 Processing artist: {artist_name}")
            
            for post_dir in artist_dir.iterdir():
                if not post_dir.is_dir():
                    continue
                
                if self.verbose:
                    print(f"  📁 Processing post: {post_dir.name}")
                
                # Download content if requested
                if self.download_content and self.downloader:
                    try:
                        downloaded = self.downloader.process_post_links(
                            post_dir, artist_name, post_dir.name
                        )
                        download_summary["attempted"] += 1
                        if downloaded:
                            download_summary["successful"] += 1
                        else:
                            download_summary["failed"] += 1
                    except Exception as e:
                        if self.verbose:
                            print(f"    ❌ Download error: {e}")
                        download_summary["failed"] += 1
                
                # Continue with normal post processing
                from gallery.utils import parse_folder_name
                date_obj, title = parse_folder_name(post_dir.name)
                post_text = read_post_text(post_dir)
                media_files = self.media_processor.get_media_files(post_dir)
                
                if media_files:
                    copied_media = self.media_processor.copy_media_files(
                        artist_name, title, media_files
                    )
                    
                    thumbnail = self.media_processor.select_thumbnail(copied_media)
                    
                    posts.append({
                        'artist': artist_name,
                        'title': title,
                        'date': date_obj.isoformat(),
                        'text': post_text,
                        'media': copied_media,
                        'thumbnail': thumbnail
                    })
        
        # Print download summary
        if self.download_content and self.verbose:
            print(f"\n📊 Download Summary:")
            print(f"   Posts processed: {download_summary['attempted']}")
            print(f"   Successful downloads: {download_summary['successful']}")
            print(f"   Failed downloads: {download_summary['failed']}")
        
        posts.sort(key=lambda x: x['date'], reverse=True)
        return posts


def main():
    """Main entry point for the gallery generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate an art gallery from organized directories')
    parser.add_argument('art_directory', 
                       help='Path to the directory containing artist folders')
    parser.add_argument('-o', '--output', 
                       default='gallery',
                       help='Output directory for the generated gallery (default: gallery)')
    parser.add_argument('-v', '--verbose', 
                       action='store_true',
                       help='Enable verbose output')
    parser.add_argument('-d', '--download', 
                       action='store_true',
                       help='Attempt to download content from links in posts (Google Drive links only)')
    
    args = parser.parse_args()
    
    # Validate input directory
    art_dir = Path(args.art_directory)
    if not art_dir.exists():
        print(f"Error: Art directory '{art_dir}' does not exist")
        sys.exit(1)
    
    if not art_dir.is_dir():
        print(f"Error: '{art_dir}' is not a directory")
        sys.exit(1)
    
    # Create generator - enhanced if download requested, standard otherwise
    if args.download:
        generator = EnhancedArtGalleryGenerator(
            art_dir, 
            args.output, 
            verbose=args.verbose, 
            download_content=True
        )
    else:
        generator = ArtGalleryGenerator(art_dir, args.output, verbose=args.verbose)
    
    try:
        generator.generate()
        print(f"\n✅ Gallery successfully generated!")
        print(f"📁 Output: {Path(args.output).absolute()}")
        print(f"🌐 Open: file://{(Path(args.output) / 'index.html').absolute()}")
        
        if args.download:
            print(f"\n💡 Downloaded content is saved in 'downloads' folders within each post directory.")
            print(f"🔍 Note: Only Google Drive links are downloaded automatically.")
    
    except Exception as e:
        print(f"❌ Error generating gallery: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
