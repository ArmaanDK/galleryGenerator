# Art Gallery Generator

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

A Python tool that generates beautiful static HTML galleries from organized art directories. Features automatic ZIP extraction, video thumbnail generation, content downloading, and comprehensive file preservation.

## ✨ Features

- 🎨 **Beautiful responsive gallery** with dark/light theme
- 📦 **Smart ZIP extraction** - Preserves .psd, .clip, .ai, and 30+ artwork formats
- 🔍 **System file filtering** - Automatically ignores AppleDouble files, .DS_Store, etc.
- 📥 **Content downloading** - Fetches files from Google Drive links
- 🎬 **Video thumbnails** - Automatic generation with ffmpeg
- 🔎 **Advanced filtering** - Search by artist, media type, date
- 📱 **Mobile-friendly** - Responsive design for all devices
- 🖱️ **Interactive viewer** - Zoom, pan, keyboard navigation

## 🚀 Quick Start

```bash
# Basic usage (ZIP extraction enabled by default)
python3 gallery_generator.py /path/to/art --verbose

# With content downloading
python3 gallery_generator.py /path/to/art --download --verbose

# Custom output directory
python3 gallery_generator.py /path/to/art -o my_gallery --verbose
```

## 📋 Installation

### Requirements
- **Python 3.7+** (required)
- **ffmpeg** (optional, for video thumbnails)

### Setup

1. **Clone or download** this repository

2. **Install ffmpeg** (optional but recommended):
   ```bash
   # macOS
   brew install ffmpeg
   
   # Linux (Debian/Ubuntu)
   sudo apt install ffmpeg
   
   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

3. **Run the generator**:
   ```bash
   python3 gallery_generator.py /path/to/your/art --verbose
   ```

That's it! No Python dependencies required - uses only the standard library.

## 📁 Directory Structure

Your art directory should be organized like this:

```
Art/
├── ArtistName1/
│   ├── 2024-01-15 Artwork Title/
│   │   ├── image1.jpg
│   │   ├── image2.png
│   │   ├── artwork_pack.zip         # Auto-extracted
│   │   ├── links-description.txt    # Optional, for downloads
│   │   ├── extracted/               # Created during ZIP extraction
│   │   │   ├── character.psd        # Preserved source file
│   │   │   ├── sketch.clip          # Preserved source file
│   │   │   └── final.png            # Appears in gallery
│   │   └── downloads/               # Created with --download
│   │       └── bonus_content.zip    # Downloaded from links
│   └── 2024-02-20 Another Artwork/
│       └── artwork.gif
└── ArtistName2/
    └── 2024-03-10 Animation/
        ├── animation.mp4
        └── source_files.zip
```

### Folder Naming

Supported formats:
- `YYYY-MM-DD Title` (e.g., `2024-01-15 Character Design`)
- `YYYY-MM-DD HH-MM-Title` (e.g., `2024-01-15 14-30-Artwork`)
- Any other format (uses folder name as title)

## 🎯 Command Line Options

```bash
python3 gallery_generator.py <art_directory> [OPTIONS]
```

**Options:**
- `-o, --output <dir>` - Output directory (default: "gallery")
- `-v, --verbose` - Show detailed progress
- `--extract-zips` - Extract ZIP files (default: enabled)
- `--no-extract-zips` - Disable ZIP extraction
- `-d, --download` - Download content from links in posts

**Examples:**

```bash
# Default: ZIP extraction enabled
python3 gallery_generator.py ~/Art --verbose

# With downloads from Google Drive
python3 gallery_generator.py ~/Art --download --verbose

# Standard mode (no ZIP processing)
python3 gallery_generator.py ~/Art --no-extract-zips --verbose

# Custom output with all features
python3 gallery_generator.py ~/Art -o MyGallery --download -v
```

## 📄 Supported File Types

### Displayable in Gallery
- **Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.tiff`
- **Videos:** `.mp4`, `.webm`, `.mov`, `.avi`, `.mkv`

### Extracted and Preserved from ZIPs
When ZIP extraction is enabled, these files are extracted and saved for archival:

- **Digital Art:** `.psd`, `.clip`, `.sai`, `.xcf`, `.kra`, `.ora`
- **Design:** `.ai`, `.sketch`, `.fig`, `.afdesign`, `.afphoto`
- **3D:** `.blend`, `.c4d`, `.max`, `.ma`, `.mb`, `.fbx`, `.obj`
- **Vector:** `.svg`, `.eps`
- **Documents:** `.pdf`, `.txt`, `.md`, `.rtf`
- **All displayable formats** (images, videos)

### Automatically Filtered
- **AppleDouble files:** `._filename` (macOS resource forks)
- **System files:** `.DS_Store`, `Thumbs.db`, `desktop.ini`
- **Hidden files:** Any file starting with `.`

## 📥 Content Downloading

Create `links-*.txt` files in post directories to enable downloading:

```txt
https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing

Download the rewards pack above!

DOWNLOAD HERE: https://drive.google.com/file/d/ANOTHER_FILE_ID/view

Shop: https://www.patreon.com/c/artist/shop
```

**What gets downloaded:**
- ✅ Google Drive public files (converted to direct download)
- ✅ Direct file URLs
- ❌ Shop links (automatically skipped)
- ❌ Social media links (automatically skipped)

## 🎨 Customization

### Modify Appearance
Edit these files to customize your gallery:
- `src/gallery/templates/gallery_template.html` - HTML structure
- `src/gallery/static/styles.css` - CSS styling
- `src/gallery/static/gallery.js` - JavaScript functionality

### Change Settings
Edit `src/gallery/config.py`:
```python
# Gallery title
GALLERY_TITLE = "My Art Portfolio"

# Thumbnail timestamp (10% into video by default)
THUMBNAIL_TIMESTAMP_PERCENT = 0.15  # 15% instead

# Add custom file formats
EXTRACTABLE_ARTWORK_FORMATS.add('.procreate')
```

## 🔧 How It Works

### Enhanced Mode (Default)
```bash
python3 gallery_generator.py ~/Art --verbose
```
- ✅ ZIP extraction enabled
- ✅ AppleDouble filtering
- ✅ Source file preservation
- ❌ Content downloading (unless `--download` specified)

### Full-Featured Mode
```bash
python3 gallery_generator.py ~/Art --download --verbose
```
- ✅ Everything from Enhanced Mode
- ✅ Downloads from Google Drive links

### Standard Mode
```bash
python3 gallery_generator.py ~/Art --no-extract-zips --verbose
```
- ✅ Basic gallery generation
- ❌ No ZIP processing
- ❌ No downloads

## 🐛 Troubleshooting

### ZIP files not extracting
- Ensure `--extract-zips` flag is set (it's default)
- Check if ZIP is password-protected
- Use `--verbose` to see detailed error messages

### Thumbnails showing system files
- This should be fixed automatically (AppleDouble filtering)
- If issues persist, please report them

### Downloads failing
- Verify files are publicly accessible
- Check internet connection
- Google Drive large files may require manual download

### Video thumbnails not generating
- Install ffmpeg: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)
- Verify with: `ffmpeg -version`
- Use `--verbose` to see specific errors

### Gallery loads slowly
- This is normal with many high-resolution images
- Gallery uses lazy loading for optimization
- Consider reducing image sizes before processing

## 👥 For Contributors

Want to help improve the project?

- 🚀 [**Quick Start Guide**](QUICKSTART.md) - Get started in 5 minutes
- 📖 [**Contributing Guide**](CONTRIBUTING.md) - Detailed contribution process
- 🔧 [**Development Guide**](DEVELOPMENT.md) - Technical architecture
- 📝 [**Changelog**](CHANGELOG.md) - Version history

Even if you're new to Python, you can contribute! Check out the guides above.

## 📊 Project Structure

```
art-gallery-generator/
├── gallery_generator.py          # Main entry point
├── src/gallery/
│   ├── config.py                 # Configuration
│   ├── enhanced_generator.py     # Full-featured generator
│   ├── enhanced_media.py         # ZIP extraction & filtering
│   ├── downloader.py             # Content downloading
│   ├── utils.py                  # Helper functions
│   ├── video.py                  # Video processing
│   ├── template_loader.py        # HTML generation
│   ├── templates/                # HTML templates
│   └── static/                   # CSS & JavaScript
├── CONTRIBUTING.md               # Contribution guide
├── DEVELOPMENT.md                # Technical docs
├── CHANGELOG.md                  # Version history
└── README.md                     # This file
```

## 📜 License

This project is open source under the MIT License. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

Built with Python's standard library. Optional features use:
- **ffmpeg** for video thumbnail generation
- No other external dependencies required!

---

**Questions?** Open an issue or check the [Contributing Guide](CONTRIBUTING.md) for help.
