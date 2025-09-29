"""
Content downloading functionality for the Art Gallery Generator
"""

import re
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import List, Optional

from .utils import read_post_text


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
        """Convert Google Drive share URL to direct download URL."""
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
        content_disposition = response_headers.get('Content-Disposition', '')
        if content_disposition and 'filename=' in content_disposition:
            filename_match = re.search(r'filename[*]?=([^;]+)', content_disposition)
            if filename_match:
                filename = filename_match.group(1).strip('"\'')
                return filename
        
        parsed_url = urllib.parse.urlparse(url)
        filename = Path(parsed_url.path).name or 'downloaded_file'
        
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
                    filename += '.jpg'
            elif 'video' in content_type:
                if 'mp4' in content_type:
                    filename += '.mp4'
                elif 'webm' in content_type:
                    filename += '.webm'
                else:
                    filename += '.mp4'
            elif 'zip' in content_type or 'archive' in content_type:
                filename += '.zip'
            elif 'pdf' in content_type:
                filename += '.pdf'
        
        return filename
    
    def download_file(self, url: str, destination: Path, filename: Optional[str] = None) -> bool:
        """Download a file from URL to destination using urllib."""
        try:
            if self.verbose:
                print(f"    📥 Attempting to download: {url}")
            
            download_url = url
            if 'drive.google.com' in url:
                parsed_url = self.parse_google_drive_url(url)
                if not parsed_url:
                    if self.verbose:
                        print(f"    ❌ Could not parse Google Drive URL: {url}")
                    return False
                download_url = parsed_url
            
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
            
            content = response.read()
            content_str = content.decode('utf-8', errors='ignore')
            
            if 'drive.google.com' in download_url and 'virus scan warning' in content_str.lower():
                confirm_match = re.search(r'confirm=([a-zA-Z0-9_-]+)', content_str)
                if confirm_match:
                    confirm_token = confirm_match.group(1)
                    download_url = f"{download_url}&confirm={confirm_token}"
                    
                    request = urllib.request.Request(download_url)
                    try:
                        response = self.opener.open(request, timeout=30)
                        content = response.read()
                    except Exception as e:
                        if self.verbose:
                            print(f"    ❌ Error with confirmation token: {e}")
                        return False
            
            if not filename:
                filename = self.get_filename_from_url(download_url, dict(response.headers))
            
            destination.mkdir(parents=True, exist_ok=True)
            
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
        """Process all links in a post and download available content."""
        text_content = read_post_text(post_dir)
        if not text_content:
            return []
        
        urls = self.extract_links_from_text(text_content)
        if not urls:
            return []
        
        if self.verbose:
            print(f"  🔗 Found {len(urls)} links in {post_title}")
        
        downloads_dir = post_dir / "downloads"
        downloaded_files = []
        
        for url in urls:
            skip_patterns = [
                'patreon.com/c/',
                '/shop',
                'twitter.com',
                'instagram.com',
                'facebook.com',
                'discord.gg',
            ]
            
            if any(skip in url.lower() for skip in skip_patterns):
                if self.verbose:
                    print(f"    ⭐ Skipping non-content link: {url}")
                continue
            
            if self.download_file(url, downloads_dir):
                downloaded_files.append(url)
        
        return downloaded_files