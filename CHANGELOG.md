# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Centralized File Filtering**: New `should_skip_file()` function in utils.py
  - Single source of truth for all file filtering across the application
  - Consistent behavior in all modules (media, enhanced_media, video)
  - Better verbose logging shows when system files are skipped

### Changed
- **Enhanced AppleDouble Filtering**: Complete pipeline coverage
  - Now filters AppleDouble files (`._filename`) in all processing stages
  - Filters during directory scanning (media.py, enhanced_media.py)
  - Filters during ZIP extraction (both standard and enhanced modes)
  - Filters before video thumbnail generation (video.py)
  - Eliminates broken thumbnails caused by macOS resource fork files
  
- **Improved get_media_type()**: Now calls centralized filtering first
  - Returns None for system files before checking media type
  - Prevents system files from being processed as media

- **Better Error Prevention**: Proactive filtering vs reactive handling
  - System files never enter processing pipeline
  - Reduces wasted CPU cycles on invalid files
  - Cleaner verbose output with skip notifications

### Fixed
- AppleDouble files no longer appear as thumbnails in gallery
- Video processor no longer attempts to generate thumbnails from `._video.mp4` files
- ZIP extraction properly skips `._` files and `__MACOSX` folders
- Standard mode (--no-extract-zips) now has same filtering as enhanced mode
- Consistent system file filtering across all gallery generation modes

### To Do
- Add automated tests
- Add batch processing support
- Add image optimization
- Support additional cloud storage providers

---

## [1.1.0] - 2025-01-XX

### Added
- **ZIP Extraction**: Automatically extracts ZIP files and preserves artwork source files
  - Supports 30+ file formats including `.psd`, `.clip`, `.ai`, `.xcf`, `.kra`, `.blend`
  - Extracts to dedicated `extracted/` folders within each post
  - Preserves original ZIP files for backup
  - Automatically flattens nested directory structures
  - Handles filename conflicts intelligently

- **AppleDouble File Filtering**: Fixes thumbnail issues on macOS
  - Automatically filters `._` prefixed files (AppleDouble resource forks)
  - Filters `.DS_Store`, `Thumbs.db`, and other system files
  - Prevents broken thumbnails in gallery

- **Content Downloading**: Download files from links in posts
  - Automatic Google Drive download support
  - Converts share links to direct download links
  - Handles Google Drive virus scan warnings for large files
  - Skips non-content links (shop links, social media)
  - Downloads saved to `downloads/` folders
  - Comprehensive error handling and reporting

- **Enhanced CLI Options**:
  - `--extract-zips` - Enable ZIP extraction (default)
  - `--no-extract-zips` - Disable ZIP extraction
  - `--download` - Enable content downloading
  - `-o, --output` - Specify custom output directory

- **Comprehensive Statistics**:
  - ZIP extraction reporting (files processed, extracted, preserved)
  - Download statistics (posts processed, files downloaded)
  - Detailed verbose output for debugging

- **Documentation**:
  - Added CONTRIBUTING.md for new contributors
  - Added DEVELOPMENT.md for technical details
  - Enhanced README.md with examples and troubleshooting
  - Added detailed inline code comments

### Changed
- **Module Architecture**: Split into modular components
  - `enhanced_media.py` - ZIP extraction and filtering
  - `enhanced_generator.py` - Full-featured generator
  - `downloader.py` - Content downloading
  - Original modules preserved for backward compatibility

- **Error Handling**: Improved graceful degradation
  - Features work independently (can have ZIP without downloads, etc.)
  - Better error messages and user feedback
  - Continues processing even if individual operations fail

- **Performance**: Optimized file processing
  - Sequential processing prevents memory issues
  - Efficient ZIP extraction with conflict resolution
  - Smart caching of video thumbnails

### Fixed
- AppleDouble files (`._filename`) no longer used as thumbnails
- System files properly filtered from media processing
- Nested ZIP directories now properly flattened
- Video thumbnail generation more reliable
- UTF-8 encoding issues in text files

---

## [1.0.0] - 2024-XX-XX

### Added
- Initial release
- Basic gallery generation from organized directories
- Automatic video thumbnail generation with ffmpeg
- Dark/light theme toggle
- Responsive design for mobile and desktop
- Advanced filtering by artist, media type, search terms
- Interactive media viewer with zoom and pan
- Keyboard navigation support
- Flexible folder naming support

### Features
- Supports images: `.jpg`, `.png`, `.gif`, `.webp`
- Supports videos: `.mp4`, `.webm`, `.mov`, `.avi`
- Artist and post organization
- Date parsing from folder names
- Text content from `links-*.txt` files
- Single-file HTML output

---

## Release Type Definitions

### Major (X.0.0)
- Breaking changes
- Major architectural changes
- Incompatible API changes

### Minor (1.X.0)
- New features
- Non-breaking changes
- Backward compatible improvements

### Patch (1.1.X)
- Bug fixes
- Security patches
- Minor improvements

---

## How to Contribute to Changelog

When making changes:

1. **Add entry under `[Unreleased]`**
2. **Use appropriate category**:
   - `Added` - New features
   - `Changed` - Changes to existing functionality
   - `Deprecated` - Soon-to-be removed features
   - `Removed` - Removed features
   - `Fixed` - Bug fixes
   - `Security` - Security fixes

3. **Be descriptive**:
   ```markdown
   ### Added
   - **Feature Name**: Brief description
     - Sub-detail 1
     - Sub-detail 2
   ```

4. **Link to issues** if applicable:
   ```markdown
   - Fixed thumbnail generation bug (#123)
   ```

---

## Questions?

- See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- See [README.md](README.md) for usage instructions
- Open an issue for questions or feature requests
