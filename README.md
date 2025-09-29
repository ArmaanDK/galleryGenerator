# Art Gallery Generator

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code Style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

A Python tool that generates beautiful static HTML galleries from organized art directories with automatic video thumbnail generation, ZIP extraction, comprehensive file preservation, and optional content downloading.

## 👥 For Contributors

New to the project or want to help improve it?

- 🚀 [**Quick Start Guide**](QUICKSTART.md) - Get started in 5 minutes!
- 📖 [**Contributing Guide**](CONTRIBUTING.md) - Detailed contribution process
- 🔧 [**Development Guide**](DEVELOPMENT.md) - Technical architecture and design
- 💡 [**Good First Issues**](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) - Easy tasks to start with
- 📝 [**Changelog**](CHANGELOG.md) - See what's new in each version

**Even if you're new to Python, you can contribute!** Check out the guides above.

---

## Features

- 🎨 **Beautiful responsive gallery** with dark/light theme support
- 🖼️ **Automatic video thumbnails** using ffmpeg
- 📦 **Smart ZIP extraction** preserves .psd, .clip, .ai and other artwork files
- 🔍 **System file filtering** ignores AppleDouble files, .DS_Store, Thumbs.db
- 📥 **Automatic content downloading** from Google Drive links in posts
- 🔍 **Advanced filtering** by artist, media type, and search terms
- 📱 **Mobile-friendly** responsive design
- 🖱️ **Interactive media viewer** with zoom and pan functionality
- ⌨️ **Keyboard navigation** for easy browsing
- 📁 **Flexible organization** supporting various folder naming schemes

## Project Structure

```
art-gallery-generator/
├── gallery_generator.py          # Main entry point with full feature support
├── src/
│   └── gallery/
│       ├── __init__.py
│       ├── config.py             # Configuration settings
│       ├── utils.py              # Utility functions
│       ├── video.py              # Video processing
│       ├── media.py              # Standard media file handling
│       ├── enhanced_media.py     # Enhanced media processing with ZIP extraction
│       ├── generator.py          # Core gallery generator
│       ├── enhanced_generator.py # Enhanced generator with ZIP & download support
│       ├── downloader.py         # Content downloading functionality
│       ├── template_loader.py    # Template management
│       ├── templates/
│       │   ├── default_template.py
│       │   └── gallery_template.html
│       └── static/
│           ├── default_styles.py
│           ├── default_gallery.py
│           ├── styles.css        # Optional custom CSS
│           └── gallery.js        # Optional custom JS
├── requirements.txt
└── README.md
```

## Installation

1. **Clone or download** this project
2. **Install Python dependencies** (optional, but recommended):
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

## Quick Start

```bash
# Basic usage with all features enabled (default)
python3 gallery_generator.py /path/to/your/art/directory

# With verbose output to see what's happening
python3 gallery_generator.py /path/to/art --verbose

# With custom output directory
python3 gallery_generator.py /path/to/art --output my_gallery --verbose
```

## Usage

### Command Line Options

```bash
python3 gallery_generator.py <art_directory> [OPTIONS]
```

**Required:**
- `art_directory` - Path to your organized art directory

**Optional:**
- `-o, --output <directory>` - Output directory name (default: "gallery")
- `-v, --verbose` - Enable detailed output during generation
- `--extract-zips` - Extract ZIP files and preserve all content (default: enabled)
- `--no-extract-zips` - Disable ZIP extraction (standard mode)
- `-d, --download` - Download content from links in posts (requires enhanced generator)

### Usage Examples

```bash
# Default mode: ZIP extraction enabled, no downloads
python3 gallery_generator.py ~/Art --verbose

# With content downloading from Google Drive links
python3 gallery_generator.py ~/Art --download --verbose

# Custom output directory with all features
python3 gallery_generator.py ~/Art -o MyGallery --download --verbose

# Standard mode without ZIP extraction
python3 gallery_generator.py ~/Art --no-extract-zips --verbose

# Just ZIP extraction, no downloads
python3 gallery_generator.py ~/Art --extract-zips --verbose
```

## Directory Structure

Your art directory should be organized like this:

```
Art/
├── ArtistName1/
│   ├── 2024-01-15 Artwork Title/
│   │   ├── image1.jpg
│   │   ├── image2.png
│   │   ├── video.mp4
│   │   ├── artwork_pack.zip         # Automatically extracted with --extract-zips
│   │   ├── links-description.txt    # Optional description with download links
│   │   ├── extracted/               # Auto-created during ZIP extraction
│   │   │   ├── character_sheet.psd  # Preserved artwork source files
│   │   │   ├── animation.clip       # Preserved artwork source files
│   │   │   ├── final_render.png     # Appears in gallery
│   │   │   └── bonus_video.mp4      # Appears in gallery
│   │   └── downloads/               # Auto-created with --download
│   │       ├── reward1.zip          # Downloaded from Google Drive
│   │       └── bonus_content.jpg    # Downloaded from Google Drive
│   └── 2024-02-20 Another Artwork/
│       └── artwork.gif
└── ArtistName2/
    └── 2024-03-10 Cool Animation/
        ├── animation.mp4
        ├── source_files.zip
        ├── links-info.txt
        └── extracted/
            ├── project.blend        # 3D source file preserved
            ├── textures.psd         # Texture source preserved
            └── final_animation.mp4  # Appears in gallery
```

### Folder Naming

The generator supports these folder naming patterns:
- `YYYY-MM-DD Title` (e.g., `2024-01-15 Character Design`)
- `YYYY-MM-DD HH-MM-Title` (e.g., `2024-01-15 14-30-Artwork`)
- Any other format (will use folder name as title)

### Supported File Types

#### **Displayable in Gallery:**
- **Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.tiff`
- **Videos:** `.mp4`, `.webm`, `.mov`, `.avi`, `.mkv`

#### **Extracted and Preserved from ZIP files:**
- **Digital Art Software:**
  - `.psd` (Photoshop), `.clip` (Clip Studio Paint), `.sai` (Paint Tool SAI)
  - `.xcf` (GIMP), `.kra` (Krita), `.ora` (OpenRaster)
- **Design Software:**
  - `.ai` (Illustrator), `.sketch` (Sketch), `.fig` (Figma)
  - `.afdesign`, `.afphoto`, `.afpub` (Affinity Suite)
- **3D Software:**
  - `.blend` (Blender), `.c4d` (Cinema 4D), `.max` (3ds Max)
  - `.ma`, `.mb` (Maya), `.fbx`, `.obj`
- **Documents:**
  - `.pdf`, `.txt`, `.md`, `.rtf`, `.doc`, `.docx`
- **Vector Graphics:**
  - `.svg`, `.eps`, `.dwg`, `.dxf`
- **All displayable media types** (images, videos, GIFs)

#### **Automatically Filtered Out:**
- **AppleDouble Files:** `._filename` (macOS resource forks - fixes thumbnail issues!)
- **System Files:** `.DS_Store`, `Thumbs.db`, `desktop.ini`
- **Compression Artifacts:** `__MACOSX/` folders and contents
- **Hidden Files:** Any file starting with `.`

### Links File Format

Create `links-*.txt` files in post directories to enable content downloading:

```
https://drive.google.com/file/d/1V1stk-hBzXXuyhOs-e2PjoR86GZxSdJf/view?usp=sharing
https://www.patreon.com/c/artist/shop

Download rewards from the link above! Available until end of month.

DOWNLOAD HERE: https://drive.google.com/file/d/1V1stk-hBzXXuyhOs-e2PjoR86GZxSdJf/view?usp=sharing

Check out my shop for more: https://www.patreon.com/c/artist/shop
```

**Note:** Only Google Drive links will be downloaded. Shop links and social media URLs are automatically skipped.

## Features in Detail

### ZIP Extraction and File Preservation
- **Automatic extraction** of ZIP files found in post directories
- **Comprehensive file support** - preserves 30+ artwork file formats
- **Smart organization** - extracts to dedicated `extracted/` folders
- **Non-destructive** - original ZIP files are preserved
- **Gallery integration** - extracted images/videos appear in gallery
- **Archival storage** - source files (.psd, .clip, etc.) saved for future access
- **Conflict handling** - automatically resolves filename conflicts
- **System file filtering** - skips AppleDouble files, .DS_Store, etc.
- **Subdirectory flattening** - moves files from nested folders to root of extracted/
- **Empty directory cleanup** - removes empty folders after extraction

### Content Downloading
- **Automatic Google Drive downloads** from public share links
- **Smart link filtering** - skips shop links and social media URLs
- **Organized storage** - downloads saved to `downloads/` folder in each post directory
- **No external dependencies** - uses Python's built-in urllib library
- **Safe operation** - never modifies your original art files
- **Large file handling** - handles Google Drive virus scan warnings
- **Error handling** - gracefully handles failed downloads and reports status
- **Progress reporting** - shows download status with verbose mode

### Video Thumbnails
- **Automatically generated** at 10% into video duration (configurable)
- **Smart timing** - uses optimal timestamp between 1-5 seconds
- **Cached for performance** - thumbnails generated once
- **Graceful fallback** - works without ffmpeg (videos just won't have thumbnails)
- **Format support** - handles .mp4, .webm, .mov, .avi, .mkv

### Gallery Features
- **Search:** Find posts by title, artist, or description
- **Filter by media type:** Images, GIFs, videos, or mixed content
- **Sorting:** By date, artist, or title (ascending/descending)
- **Theme toggle:** Automatic dark/light mode with system preference detection
- **Lazy loading:** Optimized performance for large galleries
- **Responsive design:** Works on desktop, tablet, and mobile

### Media Viewer
- **Zoom and pan** for images with mouse drag support
- **Keyboard navigation:** Arrow keys, +/- for zoom, F for fit-to-window, Escape to close
- **Touch support** for mobile devices
- **Video controls** with native HTML5 player
- **Fullscreen mode** - F11 or button to enter fullscreen viewing
- **Media navigation** - thumbnails and arrows for multi-image posts

## Modes of Operation

### Enhanced Mode (Default)
**Enabled by default** - ZIP extraction + AppleDouble filtering

```bash
python3 gallery_generator.py /path/to/art --verbose
# OR explicitly:
python3 gallery_generator.py /path/to/art --extract-zips --verbose
```

**Features:**
- ✅ ZIP extraction enabled
- ✅ AppleDouble file filtering
- ✅ Comprehensive file preservation
- ✅ All standard gallery features
- ❌ Content downloading (unless --download specified)

### Enhanced Mode with Downloads
**Full feature set** - ZIP extraction + content downloading

```bash
python3 gallery_generator.py /path/to/art --download --verbose
```

**Features:**
- ✅ ZIP extraction enabled
- ✅ Content downloading from Google Drive links
- ✅ AppleDouble file filtering
- ✅ Comprehensive file preservation
- ✅ All standard gallery features

### Standard Mode
**Legacy compatibility** - no ZIP processing

```bash
python3 gallery_generator.py /path/to/art --no-extract-zips --verbose
```

**Features:**
- ❌ No ZIP extraction
- ✅ Standard media file handling
- ✅ Standard gallery features
- ❌ No content downloading

## ZIP Extraction Examples

### What Gets Extracted and Preserved

**Before Processing:**
```
2024-01-15 Character Design/
├── preview.jpg
├── character_pack.zip    # Contains: design.psd, sketch.clip, final.png, notes.txt
└── links-info.txt
```

**After Processing (with `--extract-zips`):**
```
2024-01-15 Character Design/
├── preview.jpg                    # Original files untouched
├── character_pack.zip            # Original ZIP preserved
├── links-info.txt               # Original files untouched
└── extracted/                   # Auto-created extraction folder
    ├── design.psd               # ✅ Photoshop file preserved
    ├── sketch.clip              # ✅ Clip Studio file preserved
    ├── final.png                # ✅ Shows in gallery
    └── notes.txt                # ✅ Text file preserved
```

**Gallery Display:**
- **Thumbnail:** Uses `preview.jpg` or `extracted/final.png`
- **Media Viewer:** Shows `preview.jpg` and `[extracted] final.png`
- **Preserved Files:** `design.psd`, `sketch.clip`, `notes.txt` saved in extracted/ but not displayed in gallery

### Complete Example with All Features

**Before:**
```
2024-03-10 March Rewards/
├── preview.jpg
├── rewards_pack.zip        # Contains PSD, CLIP, final images
└── links-march.txt         # Contains Google Drive download link
```

**After Processing (with `--download --extract-zips`):**
```
2024-03-10 March Rewards/
├── preview.jpg
├── rewards_pack.zip
├── links-march.txt
├── extracted/              # From ZIP extraction
│   ├── character.psd
│   ├── lineart.clip
│   ├── final_1.png         # Appears in gallery
│   └── final_2.png         # Appears in gallery
└── downloads/              # From link downloading
    ├── bonus_pack.zip
    └── wallpaper.jpg       # Appears in gallery
```

**Gallery Shows:**
- `preview.jpg`
- `[extracted] final_1.png`
- `[extracted] final_2.png`
- `[downloads] wallpaper.jpg` (if extracted from bonus_pack.zip)

**Preserved for Access:**
- `character.psd`, `lineart.clip` in `extracted/`
- `bonus_pack.zip` in `downloads/`

## Download Functionality

### What Gets Downloaded

✅ **Downloaded:**
- Google Drive public files (automatically converted to direct download links)
- Direct file URLs (images, videos, archives)

❌ **Automatically Skipped:**
- Patreon shop links (`patreon.com/c/`, `/shop`)
- Social media links (Twitter, Instagram, Facebook, Discord)
- Private or expired links (reported as failed)

### Download Process

1. **Scans** `links-*.txt` files in each post directory
2. **Extracts** all URLs from the text content
3. **Filters** downloadable content (skips shop/social links)
4. **Downloads** files to `post_directory/downloads/`
5. **Reports** success/failure for each attempt

### Download Limitations

- **Google Drive large files** may require manual confirmation
- **Rate limiting** may occur with many rapid downloads
- **Authentication required** content won't download (private links)
- **Expired links** will be reported as failed downloads
- **Only Google Drive supported** - other cloud storage services not yet supported

## Customization

### Custom CSS
Create `src/gallery/static/styles.css` to override default styles:

```css
:root {
    --accent-color: #your-color;
    --bg-primary: #your-bg-color;
}
```

### Custom JavaScript
Create `src/gallery/static/gallery.js` to extend functionality.

### Custom Template
Modify `src/gallery/templates/gallery_template.html` for layout changes.

### Configuration
Edit `src/gallery/config.py` to change:
- Supported file formats
- ZIP extraction settings
- Thumbnail generation settings (timestamp, size)
- Gallery title and defaults
- Extraction behavior (flatten structure, file size limits, etc.)

**Example Configuration Changes:**

```python
# In config.py

# Change gallery title
GALLERY_TITLE = "My Art Portfolio"

# Change thumbnail timestamp
THUMBNAIL_TIMESTAMP_PERCENT = 0.15  # 15% into video instead of 10%

# Add custom extractable formats
EXTRACTABLE_ARTWORK_FORMATS.add('.procreate')  # Add Procreate files
```

## Requirements

- **Python 3.7+** (required)
- **ffmpeg** (optional, for video thumbnails)
- **Internet connection** (optional, for content downloading)
- **Virtual environment** (recommended for best practices)

## Troubleshooting

### ZIP Extraction Issues
- **"No extractable files found"**: ZIP contains only non-media files or unsupported formats
- **"Failed to extract"**: Check if ZIP file is corrupted or password-protected
- **Large memory usage**: Processing many large ZIP files simultaneously - consider processing in batches
- **Files not appearing in gallery**: Check if they're displayable formats (.jpg, .png, .mp4, etc.) - other formats are preserved but not shown

### AppleDouble/Thumbnail Issues
- **Thumbnails not showing**: AppleDouble files (`._filename`) are now automatically filtered
- **Gallery shows broken images**: System files were being used as media - now fixed with automatic filtering
- **Duplicate entries**: Ensure you're not manually including both `filename` and `._filename`

### Content Download Issues
- **"ContentDownloader not available"**: Ensure `downloader.py` is in `src/gallery/` directory
- **Google Drive downloads fail**: 
  - Check if files are public (share link must have viewing permissions)
  - Large files may need manual download
  - Rate limiting may occur - wait and try again
- **No downloads occurring**: 
  - Ensure your `links-*.txt` files contain valid URLs
  - Check that links aren't shop/social media URLs (these are skipped)
  - Use `--verbose` to see what's happening
- **Download timeouts**: Large files may timeout - increase timeout in `downloader.py` if needed

### Video Thumbnails Not Generating
- **Check ffmpeg installation**: Run `ffmpeg -version` in terminal
- **Ensure ffmpeg is in PATH**: System must be able to find ffmpeg command
- **Check video formats**: Some formats may not be supported
- **Use verbose mode**: Run with `--verbose` to see detailed error messages
- **File permissions**: Ensure write permissions to output directory

### Large Galleries Load Slowly
- **Reduce image sizes**: Process images to smaller dimensions before adding to gallery
- **Video thumbnail generation**: Takes time for many videos - be patient
- **Lazy loading**: Gallery uses lazy loading, so initial load should be fast
- **Browser caching**: Subsequent loads will be faster

### Permission Errors
- **Output directory**: Ensure write permissions to output directory
- **Source files**: Ensure read permissions for art directory
- **System permissions**: Some systems may require elevated permissions

### General Debugging
```bash
# Run with verbose output to see detailed information
python3 gallery_generator.py /path/to/art --verbose

# Check what mode is being used
python3 gallery_generator.py /path/to/art --verbose | head -n 5

# Test without any features
python3 gallery_generator.py /path/to/art --no-extract-zips --verbose
```

## Performance Considerations

- **Large ZIP files**: Processing may take time; progress shown with `--verbose`
- **Many files**: ZIP extraction processes files sequentially for stability
- **Memory usage**: Large ZIP files processed efficiently to minimize memory usage
- **Disk space**: Original ZIP files preserved, ensure adequate disk space (roughly 2x ZIP size)
- **Download speed**: Dependent on internet connection and source server
- **Thumbnail generation**: ffmpeg processing can be CPU intensive for many videos

## Security Notes

- **ZIP extraction**: Only extracts to designated `extracted/` folders within post directories
- **Path traversal protection**: Prevents extraction outside intended directories
- **File filtering**: Automatically skips potentially harmful system files
- **No executable extraction**: Executables and scripts are not extracted from ZIP files
- **Download safety**: Only downloads from explicitly provided URLs in text files
- **No authentication**: Does not store or transmit any credentials

## Architecture

The project follows a clean, modular design:

```
┌──────────────────────────────┐
│ gallery_generator.py         │  ← Main entry point
└──────────┬───────────────────┘
           │
    ┌──────▼───────┐
    │  Mode Check  │  ← --extract-zips? --download?
    └──────┬───────┘
           │
  ┌────────▼─────────┐
  │  Enhanced Mode?  │
  └────────┬─────────┘
           │
    ┌──────▼──────────────────────┐
    │ EnhancedArtGalleryGenerator │
    │  (ZIP + Download support)   │
    └──────┬──────────────────────┘
           │
     ┌─────▼─────────┐
     │ Components:   │
     ├───────────────┤
     │ enhanced_media│  ← ZIP extraction & filtering
     │ downloader    │  ← Content downloading
     │ template_loader│  ← HTML generation
     └───────────────┘
```

**Key Design Principles:**
- **Clean separation** of concerns
- **Easy maintenance** and testing
- **Simple extension** for new features
- **No code duplication** between modes
- **Backward compatibility** with existing installations
- **Optional features** - everything can be disabled

## Workflow Examples

### Basic Workflow (Default)
```bash
# Generate gallery with ZIP extraction
python3 gallery_generator.py ~/Art --verbose

# Output:
# 🔧 Using enhanced generator with ZIP extraction
# 📦 ZIP files processed, artwork files preserved
# ✅ Gallery successfully generated!
```

### Full Feature Workflow
```bash
# Generate gallery with ZIP extraction AND content downloads
python3 gallery_generator.py ~/Art --download --verbose

# Output:
# 🔧 Using enhanced generator with ZIP extraction and download support
# 📥 Downloading content from links...
# 📦 Extracting ZIP files...
# ✅ Gallery successfully generated!
```

### Standard Workflow (Legacy)
```bash
# Generate gallery without ZIP extraction
python3 gallery_generator.py ~/Art --no-extract-zips --verbose

# Output:
# 🔧 Using standard generator (no ZIP extraction)
# ✅ Gallery successfully generated!
```

### Production Workflow
```bash
# Full featured gallery for production use
python3 gallery_generator.py ~/ArtProjects \
    --output ~/WebServer/public/gallery \
    --download \
    --verbose

# Then view the gallery
open ~/WebServer/public/gallery/index.html
```

## License

This project is open source. Feel free to modify and distribute as needed.

## Contributing

Contributions are welcome! Areas for improvement:
- Additional cloud storage support (Dropbox, OneDrive, etc.)
- Batch processing optimization
- Additional artwork format support
- Gallery template themes
- Advanced filtering options

## Changelog

### Version 1.1.0
- ✅ Added ZIP extraction with comprehensive file preservation
- ✅ Added AppleDouble file filtering (fixes thumbnail issues)
- ✅ Added automatic content downloading from Google Drive
- ✅ Enhanced error handling and reporting
- ✅ Improved documentation

### Version 1.0.0
- Initial release with basic gallery generation
- Video thumbnail support
- Dark/light theme toggle
- Responsive design

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

### Basic Gallery Generation (with ZIP extraction)

```bash
# Standard gallery generation with ZIP extraction (default mode)
python3 gallery_generator.py /path/to/your/art/directory

# With custom output directory and verbose output
python3 gallery_generator.py /path/to/art --output my_gallery --verbose
```

### Gallery Generation Options

```bash
# Enable ZIP extraction explicitly (default behavior)
python3 gallery_generator.py /path/to/art --extract-zips --verbose

# Disable ZIP extraction (standard mode)
python3 gallery_generator.py /path/to/art --no-extract-zips --verbose

# With content downloading from Google Drive links
python3 gallery_generator.py /path/to/art --download --verbose
```

### Command Line Options

- `art_directory`: Path to your organized art directory (required)
- `-o, --output`: Output directory name (default: "gallery")
- `-v, --verbose`: Enable detailed output during generation
- `--extract-zips`: Extract ZIP files and preserve all content (default)
- `--no-extract-zips`: Disable ZIP extraction (standard mode)
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
│   │   ├── artwork_pack.zip         # ZIP files are automatically extracted
│   │   ├── links-description.txt    # Optional description with links
│   │   ├── extracted/               # Auto-created when ZIP extraction enabled
│   │   │   ├── character_sheet.psd  # Preserved artwork files
│   │   │   ├── animation.clip       # Preserved artwork files
│   │   │   ├── final_render.png     # Appears in gallery
│   │   │   └── bonus_video.mp4      # Appears in gallery
│   │   └── downloads/               # Auto-created when using --download
│   │       ├── reward1.zip
│   │       └── bonus_content.jpg
│   └── 2024-02-20 Another Artwork/
│       └── artwork.gif
└── ArtistName2/
    └── 2024-03-10 Cool Animation/
        ├── animation.mp4
        ├── source_files.zip
        ├── links-info.txt
        └── extracted/
            ├── project.blend        # 3D source file preserved
            ├── textures.psd         # Texture source preserved
            └── final_animation.mp4  # Appears in gallery
```

### Folder Naming

The generator supports these folder naming patterns:
- `YYYY-MM-DD Title`
- `YYYY-MM-DD HH-MM-Title`
- Any other format (will use folder name as title)

### Supported File Types

#### **Displayable in Gallery:**
- **Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- **Videos:** `.mp4`, `.webm`, `.mov`, `.avi`

#### **Extracted and Preserved from ZIP files:**
- **Artwork Files:** `.psd`, `.clip`, `.ai`, `.xcf`, `.kra`, `.sai`, `.sketch`
- **Design Files:** `.fig`, `.afdesign`, `.afphoto`, `.blend`, `.c4d`
- **Documents:** `.pdf`, `.txt`, `.md`, `.rtf`
- **All displayable media types** (images, videos)

#### **Automatically Filtered Out:**
- **AppleDouble Files:** `._filename` (fixes thumbnail issues on macOS)
- **System Files:** `.DS_Store`, `Thumbs.db`, `desktop.ini`
- **Compression Artifacts:** `__MACOSX/` folders

### Links File Format

Create `links-*.txt` files in post directories with content like:

```
https://drive.google.com/file/d/1V1stk-hBzXXuyhOs-e2PjoR86GZxSdJf/view?usp=sharing
https://www.patreon.com/c/leaflit/shop

Please download this month rewards in the link, it will be deleted at the end of THIS month!

DOWNLOAD HERE: https://drive.google.com/file/d/1V1stk-hBzXXuyhOs-e2PjoR86GZxSdJf/view?usp=sharing

Want to get the content but it's not available anymore? Please check out my shop: https://www.patreon.com/c/leaflit/shop
```

## Features in Detail

### ZIP Extraction and File Preservation
- **Automatic extraction** of ZIP files found in post directories
- **Comprehensive file support** - preserves 20+ artwork file formats
- **Smart organization** - extracts to dedicated `extracted/` folders
- **Non-destructive** - original ZIP files are preserved
- **Gallery integration** - extracted images/videos appear in gallery
- **Archival storage** - source files (.psd, .clip, etc.) saved for future access
- **Conflict handling** - automatically resolves filename conflicts
- **System file filtering** - skips AppleDouble files, .DS_Store, etc.

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

## ZIP Extraction Examples

### What Gets Extracted and Preserved

**Before Processing:**
```
2024-01-15 Character Design/
├── preview.jpg
├── character_pack.zip    # Contains: design.psd, sketch.clip, final.png, notes.txt
└── links-info.txt
```

**After Processing (with --extract-zips):**
```
2024-01-15 Character Design/
├── preview.jpg                    # Original files untouched
├── character_pack.zip            # Original ZIP preserved
├── links-info.txt               # Original files untouched
└── extracted/                   # Auto-created extraction folder
    ├── design.psd               # ✅ Photoshop file preserved
    ├── sketch.clip              # ✅ Clip Studio file preserved
    ├── final.png                # ✅ Shows in gallery
    └── notes.txt                # ✅ Text file preserved
```

**Gallery Display:**
- **Thumbnail:** Uses `preview.jpg` or `extracted/final.png`
- **Media Viewer:** Shows `preview.jpg` and `[extracted] final.png`
- **Preserved Files:** `design.psd`, `sketch.clip`, `notes.txt` saved but not displayed

### Supported Artwork Formats in ZIP Files

```python
# Artwork source files (preserved for future use)
.psd, .clip, .ai, .xcf, .kra, .sai, .sketch, .fig, .afdesign, .afphoto
.blend, .c4d, .max, .ma, .mb, .dwg, .dxf

# Media files (displayed in gallery)
.jpg, .jpeg, .png, .gif, .webp, .mp4, .webm, .mov, .avi

# Document files (preserved)
.pdf, .txt, .md, .rtf, .doc, .docx
```

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

## Modes of Operation

### Enhanced Mode (Default)
```bash
python gallery_generator.py /path/to/art --verbose
```
- ✅ ZIP extraction enabled
- ✅ AppleDouble file filtering
- ✅ Comprehensive file preservation
- ✅ All standard gallery features

### Standard Mode
```bash
python gallery_generator.py /path/to/art --no-extract-zips --verbose
```
- ❌ No ZIP extraction
- ✅ AppleDouble file filtering (when using enhanced media processor)
- ✅ Standard gallery features

### Download Mode
```bash
python gallery_generator.py /path/to/art --download --verbose
```
- ✅ ZIP extraction enabled
- ✅ Content downloading from links
- ✅ All enhanced features

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
- ZIP extraction settings
- Thumbnail settings
- Gallery title and defaults

## Requirements

- **Python 3.7+** (required)
- **ffmpeg** (optional, for video thumbnails)
- **Virtual environment** (recommended for best practices)

## Workflow Examples

### Basic Workflow (Default)
```bash
# Generate gallery with ZIP extraction
python3 gallery_generator.py ~/Art --verbose
```

### Enhanced Workflow with Downloads
```bash
# Generate gallery with ZIP extraction and content downloads
python3 gallery_generator.py ~/Art --download --verbose
```

### Standard Workflow (No ZIP Processing)
```bash
# Generate gallery without ZIP extraction
python3 gallery_generator.py ~/Art --no-extract-zips --verbose
```

## Troubleshooting

### ZIP Extraction Issues
- **"No extractable files found"**: ZIP may contain only non-media files
- **"Failed to extract"**: Check if ZIP file is corrupted or password-protected
- **Large memory usage**: Processing many large ZIP files simultaneously

### AppleDouble/Thumbnail Issues
- **Thumbnails not showing**: Check for `._` files in directories (now automatically filtered)
- **Gallery shows broken images**: System files were being used as media (now fixed)

### Content Download Issues
- **"externally-managed-environment" error**: Use virtual environment
- **Google Drive downloads fail**: Check if files are public; large files may need manual download
- **No downloads occurring**: Ensure your `links-*.txt` files contain valid URLs

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

## Architecture

The project follows a clean, modular design:

```
┌─────────────────────────┐
│ gallery_generator.py    │  ← Main entry point (argument parsing)
└──────────┬──────────────┘
           │
    ┌──────▼──────┐
    │   Mode?     │  ← Decision point based on --extract-zips flag
    └──────┬──────┘
           │
  ┌────────▼────────┐
  │ No │         │ Yes │
  ▼    │         ▼     │
┌─────────────┐ ┌──────────────────┐
│ generator.py│ │enhanced_generator.py│
│ (standard)  │ │   (with ZIP extraction)   │
└─────────────┘ └──────────┬───────────┘
                           │
                ┌─────────▼─────────┐
                │enhanced_media.py  │  ← ZIP extraction & file filtering
                │ (EnhancedMediaProcessor) │
                └───────────────────┘
```

This design ensures:
- **Clean separation** of concerns
- **Easy maintenance** and testing
- **Simple extension** for new features
- **No code duplication** between modes
- **Backward compatibility** with existing installations

## Performance Considerations

- **Large ZIP files**: Processing may take time; progress is shown with `--verbose`
- **Many files**: ZIP extraction processes files sequentially for stability
- **Memory usage**: Large ZIP files are processed in chunks to minimize memory usage
- **Disk space**: Original ZIP files are preserved, so ensure adequate disk space

## Security Notes

- **ZIP extraction**: Only extracts to designated `extracted/` folders within post directories
- **File filtering**: Automatically skips potentially harmful system files
- **Path traversal protection**: Prevents extraction outside intended directories
- **No executable extraction**: Executables and scripts are not extracted from ZIP files

## License

This project is open source. Feel free to modify and distribute as needed.