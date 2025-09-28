# Art Gallery Generator

A Python tool that generates beautiful static HTML galleries from organized art directories with automatic video thumbnail generation and optional content downloading from links.

## Features

- 🎨 **Beautiful responsive gallery** with dark/light theme support
- 🖼️ **Automatic video thumbnails** using ffmpeg
- 📥 **Automatic content downloading** from Google Drive links in posts
- 🔍 **Advanced filtering** by artist, media type, and search terms
- 📱 **Mobile-friendly** responsive design
- 🖱️ **Interactive media viewer** with zoom and pan functionality
- ⌨️ **Keyboard navigation** for easy browsing
- 📁 **Flexible organization** supporting various folder naming schemes

## Project Structure

```
art-gallery-generator/
├── gallery_generator.py          # Main entry point (original)
├── builtin_gallery_generator.py  # Enhanced version with download support
├── src/
│   └── gallery/
│       ├── __init__.py
│       ├── config.py             # Configuration settings
│       ├── utils.py              # Utility functions
│       ├── video.py              # Video processing
│       ├── media.py              # Media file handling
│       ├── generator.py          # Core gallery generator
│       ├── template_loader.py    # Template management
│       ├── templates/
│       │   └── gallery_template.html
│       └── static/
│           ├── styles.css        # Optional custom CSS
│           └── gallery.js        # Optional custom JS
├── requirements.txt
└── README.md
```

## Installation

1. **Clone or download** this project
2. **Install Python dependencies** (optional, for enhanced features):
   ```bash
   # Create virtual environment (recommended)
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install optional dependencies
   pip install -r requirements.txt
   ```
3. **Install ffmpeg** (optional, for video thumbnails):
   - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg` or `sudo yum install ffmpeg`

## Usage

### Basic Gallery Generation

```bash
# Standard gallery generation (no external dependencies required)
python3 gallery_generator.py /path/to/your/art/directory

# With custom output directory and verbose output
python3 gallery_generator.py /path/to/art --output my_gallery --verbose
```

### Enhanced Gallery with Content Downloading

```bash
# Generate gallery and download content from Google Drive links
python3 builtin_gallery_generator.py /path/to/art --download --verbose

# Standard gallery generation (without downloads)
python3 builtin_gallery_generator.py /path/to/art --verbose
```

### Options

#### Standard Gallery Generator (`gallery_generator.py`)
- `art_directory`: Path to your organized art directory (required)
- `-o, --output`: Output directory name (default: "gallery")
- `-v, --verbose`: Enable detailed output during generation

#### Enhanced Gallery Generator (`builtin_gallery_generator.py`)
- `art_directory`: Path to your organized art directory (required)
- `-o, --output`: Output directory name (default: "gallery")
- `-v, --verbose`: Enable detailed output during generation
- `-d, --download`: Attempt to download content from links in posts

## Directory Structure

Your art directory should be organized like this:

```
Art/
├── ArtistName1/
│   ├── 2024-01-15 Artwork Title/
│   │   ├── image1.jpg
│   │   ├── image2.png
│   │   ├── video.mp4
│   │   ├── links-description.txt    # Optional description with links
│   │   └── downloads/               # Auto-created when using --download
│   │       ├── reward1.zip
│   │       └── bonus_content.jpg
│   └── 2024-02-20 Another Artwork/
│       └── artwork.gif
└── ArtistName2/
    └── 2024-03-10 Cool Animation/
        ├── animation.mp4
        ├── links-info.txt
        └── downloads/
            └── full_resolution.png
```

### Folder Naming

The generator supports these folder naming patterns:
- `YYYY-MM-DD Title`
- `YYYY-MM-DD HH-MM-Title`
- Any other format (will use folder name as title)

### Supported File Types

- **Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- **Videos:** `.mp4`, `.webm`, `.mov`, `.avi`

### Links File Format

Create `links-*.txt` files in post directories with content like:

```
https://drive.google.com/file/d/1BwzxRSZNmy_ynmRuGOVmIVQnW1SDg3Nl/view?usp=sharing
https://www.patreon.com/c/leaflit/shop

Please download this month rewards in the link, it will be deleted at the end of THIS month!

DOWNLOAD HERE: https://drive.google.com/file/d/1BwzxRSZNmy_ynmRuGOVmIVQnW1SDg3Nl/view?usp=sharing

Want to get the content but it's not available anymore? Please check out my shop: https://www.patreon.com/c/leaflit/shop
```

## Features in Detail

### Content Downloading
- **Automatic Google Drive downloads** from public share links
- **Smart link filtering** - skips shop links and social media URLs
- **Organized storage** - downloads saved to `downloads/` folder in each post directory
- **No external dependencies** - uses Python's built-in urllib library
- **Safe operation** - never modifies your original art files

### Video Thumbnails
- Automatically generated at 10% into video duration
- Cached for performance
- Graceful fallback when ffmpeg unavailable

### Gallery Features
- **Search:** Find posts by title, artist, or description
- **Filter by media type:** Images, GIFs, videos, or mixed content
- **Sorting:** By date, artist, or title (ascending/descending)
- **Theme toggle:** Automatic dark/light mode with system preference detection

### Media Viewer
- **Zoom and pan** for images
- **Keyboard navigation:** Arrow keys, +/- for zoom, F for fit-to-window
- **Touch support** for mobile devices
- **Video controls** with native HTML5 player

## Download Functionality

### What Gets Downloaded
- ✅ **Google Drive public files** (automatically converted to direct download links)
- ✅ **Direct file URLs** (images, videos, archives)
- ❌ **Patreon shop links** (skipped automatically)
- ❌ **Social media links** (skipped automatically)
- ❌ **Private or expired links** (will fail gracefully)

### Download Process
1. **Scans** `links-*.txt` files in each post directory
2. **Extracts** all URLs from the text content
3. **Filters** to downloadable content (skips shop/social links)
4. **Downloads** files to `post_directory/downloads/`
5. **Reports** success/failure for each attempt

### Download Limitations
- **Google Drive large files** may require manual confirmation
- **Rate limiting** may occur with many rapid downloads
- **Authentication required** content (private Patreon posts) won't download
- **Expired links** will be reported as failed downloads

## Customization

### Custom CSS
Create `src/gallery/static/styles.css` to override default styles.

### Custom JavaScript
Create `src/gallery/static/gallery.js` to extend functionality.

### Custom Template
Modify `src/gallery/templates/gallery_template.html` for layout changes.

### Configuration
Edit `src/gallery/config.py` to change:
- Supported file formats
- Thumbnail settings
- Gallery title and defaults

## Requirements

- **Python 3.7+** (required)
- **ffmpeg** (optional, for video thumbnails)
- **Virtual environment** (recommended for best practices)

## Workflow Examples

### Basic Workflow
```bash
# Generate gallery without downloads
python3 gallery_generator.py ~/Art --verbose
```

### Enhanced Workflow
```bash
# Generate gallery and download available content
python3 builtin_gallery_generator.py ~/Art --download --verbose
```

### Mixed Workflow
```bash
# First, try downloading content
python3 builtin_gallery_generator.py ~/Art --download --verbose

# Then generate final gallery (if downloads change your content)
python3 gallery_generator.py ~/Art --verbose
```

## Troubleshooting

### Content Download Issues
- **"externally-managed-environment" error**: Use virtual environment or the built-in version
- **Google Drive downloads fail**: Check if files are public; large files may need manual download
- **No downloads occurring**: Ensure your `links-*.txt` files contain valid URLs
- **Downloads timeout**: Try again later; Google Drive may be rate-limiting

### Video thumbnails not generating
- Ensure ffmpeg is installed and in your system PATH
- Check that video files are in supported formats
- Run with `--verbose` to see detailed error messages

### Large galleries load slowly
- Consider reducing image sizes before processing
- Video thumbnail generation may take time for many videos
- The generated gallery uses lazy loading for optimal performance

### Permission errors
- Ensure you have write permissions to the output directory
- On some systems, you may need to run with elevated permissions

## Version Differences

| Feature | `gallery_generator.py` | `builtin_gallery_generator.py` |
|---------|----------------------|--------------------------------|
| Gallery Generation | ✅ | ✅ |
| Video Thumbnails | ✅ | ✅ |
| Content Downloads | ❌ | ✅ |
| External Dependencies | None | None |
| Google Drive Support | ❌ | ✅ |
| Link Analysis | ❌ | ✅ |

## License

This project is open source. Feel free to modify and distribute as needed.
