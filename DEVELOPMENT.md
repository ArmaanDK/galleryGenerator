# Development Guide

This guide explains the technical architecture and design decisions for developers working on the Art Gallery Generator.

## Architecture Overview

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    gallery_generator.py                      │
│                  (CLI & Orchestration)                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                ┌───────────▼───────────┐
                │  Argument Processing  │
                │  Mode Selection       │
                └───────────┬───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐  ┌──────────────────┐  ┌──────────────┐
│   Standard    │  │    Enhanced      │  │   Enhanced   │
│   Generator   │  │    Generator     │  │   Generator  │
│               │  │  (ZIP only)      │  │ (ZIP + DL)   │
└───────────────┘  └────────┬─────────┘  └──────┬───────┘
                            │                    │
                    ┌───────▼────────┐   ┌──────▼─────┐
                    │ Enhanced Media │   │ Downloader │
                    │   Processor    │   └────────────┘
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │ Video Processor│
                    └────────────────┘
```

### Data Flow

1. **Input Processing**
   - User provides art directory path
   - Scanner walks through directory structure
   - Folders parsed for date and title

2. **Media Processing**
   - ZIP files extracted (if enabled)
   - System files filtered out
   - Media files identified and cataloged

3. **Content Enhancement**
   - Video thumbnails generated (if ffmpeg available)
   - Content downloaded from links (if enabled)
   - Files copied to output directory

4. **Gallery Generation**
   - Template loaded and populated
   - JSON data embedded in HTML
   - Static files written to output

## Module Responsibilities

### `gallery_generator.py`
**Purpose**: Main entry point and CLI interface

**Responsibilities**:
- Parse command line arguments
- Select appropriate generator mode
- Handle errors and display results
- Provide user-friendly output

**Key Functions**:
- `main()` - Entry point

**Dependencies**: All generator classes

---

### `config.py`
**Purpose**: Central configuration

**Responsibilities**:
- Define supported file formats
- Set default values
- Configure extraction behavior

**Key Constants**:
- `SUPPORTED_IMAGE_FORMATS` - Displayable image types
- `SUPPORTED_VIDEO_FORMATS` - Displayable video types
- `EXTRACTABLE_ARTWORK_FORMATS` - ZIP extractable formats
- `THUMBNAIL_SETTINGS` - Video thumbnail configuration

**No dependencies**

---

### `utils.py`
**Purpose**: Helper functions

**Responsibilities**:
- Parse folder names for dates
- Clean text for JavaScript embedding
- Check for ffmpeg availability
- Determine media types

**Key Functions**:
- `parse_folder_name(folder_name)` - Extract date and title
- `clean_text_for_js(content)` - Escape text for JS
- `check_ffmpeg()` - Verify ffmpeg installation
- `get_media_type(file_path)` - Identify file type

**Dependencies**: config.py

---

### `video.py`
**Purpose**: Video thumbnail generation

**Responsibilities**:
- Generate thumbnails using ffmpeg
- Calculate optimal timestamp
- Handle video duration detection

**Key Classes**:
- `VideoProcessor` - Handles all video operations

**Key Methods**:
- `generate_thumbnail()` - Create thumbnail from video
- `get_video_duration()` - Get video length
- `get_optimal_thumbnail_timestamp()` - Calculate best frame

**Dependencies**: config.py

---

### `media.py`
**Purpose**: Standard media file handling

**Responsibilities**:
- List media files in directories
- Copy files to output
- Generate video thumbnails
- Select post thumbnails

**Key Classes**:
- `MediaProcessor` - Standard media operations

**Key Methods**:
- `get_media_files()` - List all media
- `copy_media_files()` - Copy to output
- `select_thumbnail()` - Choose best thumbnail

**Dependencies**: utils.py, video.py

---

### `enhanced_media.py`
**Purpose**: Enhanced media processing with ZIP extraction

**Responsibilities**:
- Extract ZIP files
- Filter system files (AppleDouble, etc.)
- Preserve artwork source files
- Flatten directory structures
- Clean up empty directories

**Key Classes**:
- `EnhancedMediaProcessor` - Enhanced media operations

**Key Methods**:
- `extract_zip_files()` - Extract and organize ZIPs
- `_should_skip_file()` - System file filtering
- `get_extraction_summary()` - Statistics on extracted files

**Dependencies**: utils.py, video.py

---

### `generator.py`
**Purpose**: Core gallery generation

**Responsibilities**:
- Scan post directories
- Coordinate media processing
- Generate HTML output

**Key Classes**:
- `ArtGalleryGenerator` - Standard generator

**Key Methods**:
- `scan_posts()` - Walk directory structure
- `generate()` - Create gallery

**Dependencies**: utils.py, media.py, template_loader.py

---

### `enhanced_generator.py`
**Purpose**: Enhanced gallery with ZIP and downloads

**Responsibilities**:
- Extend standard generator
- Coordinate ZIP extraction
- Coordinate content downloading
- Track statistics
- Provide detailed reporting

**Key Classes**:
- `EnhancedArtGalleryGenerator` - Full-featured generator

**Key Methods**:
- `scan_posts()` - Enhanced scanning with ZIP/download
- `get_extraction_report()` - Detailed statistics

**Dependencies**: utils.py, enhanced_media.py, downloader.py, template_loader.py

---

### `downloader.py`
**Purpose**: Content downloading from URLs

**Responsibilities**:
- Parse URLs from text files
- Download from Google Drive
- Handle download errors
- Filter non-content links

**Key Classes**:
- `ContentDownloader` - Download operations

**Key Methods**:
- `download_file()` - Download single file
- `parse_google_drive_url()` - Convert share links
- `process_post_links()` - Process all links in post

**Dependencies**: utils.py

---

### `template_loader.py`
**Purpose**: HTML template management

**Responsibilities**:
- Load HTML templates
- Load CSS styles
- Load JavaScript code
- Render final HTML

**Key Classes**:
- `TemplateLoader` - Template operations

**Key Methods**:
- `load_template()` - Load HTML
- `render_gallery()` - Generate final HTML

**Dependencies**: None (uses default templates as fallback)

## Design Patterns

### Strategy Pattern
Different generator classes implement the same interface but with different strategies:
- `ArtGalleryGenerator` - Basic strategy
- `EnhancedArtGalleryGenerator` - Enhanced strategy

### Dependency Injection
Components receive dependencies through constructor:
```python
class EnhancedArtGalleryGenerator:
    def __init__(self, art_directory, output_directory, verbose=False):
        self.media_processor = EnhancedMediaProcessor(...)
        self.downloader = ContentDownloader(...)
```

### Factory Pattern
Main script selects which generator to create based on options:
```python
if extract_zips or args.download:
    generator = EnhancedArtGalleryGenerator(...)
else:
    generator = ArtGalleryGenerator(...)
```

## Key Design Decisions

### Why Separate Media Processors?
- **Backward compatibility**: Standard processor for existing users
- **Feature isolation**: ZIP extraction is complex, keep it separate
- **Testing**: Easier to test features independently

### Why Use Path Objects?
- **Cross-platform**: Works on Windows, macOS, Linux
- **Type safety**: Caught at development time
- **Cleaner code**: `path / "subdir"` vs `os.path.join(path, "subdir")`

### Why No Database?
- **Simplicity**: Static site generator, no server needed
- **Portability**: Gallery is just HTML/CSS/JS files
- **Performance**: No database queries at runtime

### Why JSON in HTML?
- **Single file deployment**: Everything in index.html
- **No AJAX needed**: Works without web server
- **Fast loading**: All data loads with page

## Error Handling Strategy

### Fail Gracefully
Features should degrade gracefully when unavailable:
```python
if self.ffmpeg_available:
    generate_thumbnail()
else:
    # Continue without thumbnails
    pass
```

### Verbose Reporting
Always provide feedback in verbose mode:
```python
if self.verbose:
    print(f"✅ Successfully processed {count} files")
```

### Try-Except Patterns
```python
try:
    # Attempt operation
    download_file(url)
except Exception as e:
    if self.verbose:
        print(f"❌ Failed: {e}")
    # Continue processing other files
    continue
```

## Performance Considerations

### Sequential Processing
- Files processed one at a time
- Prevents memory issues with large ZIP files
- Simplifies error handling

### Lazy Loading
- Gallery uses lazy image loading
- Only loads images as user scrolls
- Improves initial page load

### Caching
- Video thumbnails cached in output
- Not regenerated on subsequent runs
- User can delete output to regenerate

## Testing Strategy

### Manual Testing
Currently relies on manual testing:
1. Create test directory structure
2. Run generator with various options
3. Verify output in browser

### Future: Automated Tests
Consider adding:
- Unit tests for utility functions
- Integration tests for generators
- Visual regression tests for gallery

### Test Data
Keep test art directories:
```
test_data/
├── simple/              # Basic test case
├── complex/             # Multiple artists, formats
├── edge_cases/          # Special characters, etc.
└── performance/         # Large number of files
```

## Adding New Features

### Checklist for New Features

1. **Design**
   - [ ] Determine which module should contain feature
   - [ ] Check if it needs new dependencies
   - [ ] Consider backward compatibility

2. **Implementation**
   - [ ] Add to appropriate module
   - [ ] Update config.py if needed
   - [ ] Add verbose logging
   - [ ] Handle errors gracefully

3. **Integration**
   - [ ] Update CLI arguments if needed
   - [ ] Update enhanced generator if applicable
   - [ ] Ensure works with existing features

4. **Documentation**
   - [ ] Add docstrings
   - [ ] Update README.md
   - [ ] Update CONTRIBUTING.md examples
   - [ ] Add to CHANGELOG.md

5. **Testing**
   - [ ] Test with minimal setup
   - [ ] Test with full features
   - [ ] Test error cases
   - [ ] Test on different platforms (if possible)

### Example: Adding Dropbox Download Support

1. **Update `downloader.py`**:
   ```python
   def parse_dropbox_url(self, url: str) -> Optional[str]:
       """Convert Dropbox share URL to direct download."""
       if 'dropbox.com' in url:
           # Add ?dl=1 to force download
           return url.replace('?dl=0', '?dl=1')
       return None
   ```

2. **Integrate in `download_file()`**:
   ```python
   if 'dropbox.com' in url:
       download_url = self.parse_dropbox_url(url)
   ```

3. **Test with real Dropbox links**

4. **Update README** to mention Dropbox support

## Debugging Tips

### Enable Verbose Mode
Always use `--verbose` when debugging:
```bash
python3 gallery_generator.py test_art --verbose
```

### Add Debug Prints
Temporarily add prints to understand flow:
```python
print(f"DEBUG: Processing file: {file_path}")
print(f"DEBUG: Media type: {media_type}")
```

### Use Python Debugger
```python
import pdb; pdb.set_trace()  # Breakpoint
```

### Check Generated Files
Look at output structure:
```bash
tree gallery/
cat gallery/index.html | grep "posts ="
```

### Common Issues

**Issue**: Files not appearing in gallery
- Check if file format in `SUPPORTED_*_FORMATS`
- Verify file isn't being filtered by `_should_skip_file()`
- Check verbose output for copy errors

**Issue**: ZIP extraction not working
- Verify `--extract-zips` flag used
- Check if ZIP is password protected
- Look for error messages in verbose output

**Issue**: Downloads failing
- Test URL manually in browser
- Check if `downloader.py` exists
- Verify internet connection

## Code Organization Principles

### Single Responsibility
Each class/function should do one thing:
```python
# Good - focused function
def parse_folder_name(folder_name: str) -> Tuple[datetime, str]:
    """Extract date and title from folder name."""
    # Just parsing logic
    
# Bad - too many responsibilities
def process_folder(folder_name: str):
    """Parse name, copy files, generate HTML..."""
    # Doing too much
```

### Don't Repeat Yourself (DRY)
```python
# Good - shared function
def should_skip_file(file_path: Path) -> bool:
    """Check if file should be skipped."""
    return file_path.name.startswith('._')

# Bad - duplicated logic
# ... in multiple places
if file_path.name.startswith('._'):
    continue
```

### Explicit is Better Than Implicit
```python
# Good - clear what's happening
def extract_zip_files(self, post_dir: Path) -> bool:
    """Returns True if any files were extracted."""
    
# Bad - unclear return meaning
def extract_zip_files(self, post_dir: Path):
    """Process ZIPs."""
```

## Future Enhancements

### Potential Features
- **Batch processing**: Process multiple art directories
- **Incremental updates**: Only process changed files
- **Cloud storage support**: OneDrive, Dropbox, etc.
- **Image optimization**: Automatic resize/compress
- **Social media integration**: Post updates automatically
- **Analytics**: Track gallery views
- **Comments system**: Allow viewer feedback
- **Password protection**: Private galleries

### Technical Debt
- Add automated tests
- Extract hardcoded strings to config
- Add type checking with mypy
- Add linting with pylint/flake8
- Create developer Docker container

## Resources

### Python Concepts Used
- **Pathlib**: Modern path handling
- **Type hints**: Function signatures
- **Context managers**: `with` statements
- **List comprehensions**: Concise filtering
- **F-strings**: String formatting
- **Dataclasses**: Structured data (potential future use)

### External Tools
- **ffmpeg**: Video processing
- **urllib**: HTTP downloads
- **zipfile**: Archive extraction
- **json**: Data serialization

### Learning Resources
- [Python Pathlib Guide](https://docs.python.org/3/library/pathlib.html)
- [Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [PEP 8 Style Guide](https://pep8.org/)
- [Real Python Tutorials](https://realpython.com/)

## Getting Help

- **Read the code**: It's well-commented
- **Check examples**: Look at existing implementations
- **Ask questions**: Open an issue with "question" label
- **Rubber duck**: Explain problem out loud (seriously, it helps!)

Happy coding! 🎉