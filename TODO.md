# TODO

## High Priority
- [ ] Make gallery persistent, running script only adds new content
- [x] ~~Completely ignore AppleDouble files, including zip extraction and thumbnail generation~~ ✅ **COMPLETED**
  - Added centralized `should_skip_file()` function in utils.py
  - Filters AppleDouble files in all processing stages:
    - Directory scanning (media.py, enhanced_media.py)
    - ZIP extraction (both standard and enhanced modes)
    - Video thumbnail generation (video.py)
  - Comprehensive system file filtering (._files, .DS_Store, Thumbs.db, etc.)

## Medium Priority
- [ ] Add persistent "Favorites" feature and filter
- [ ] Optimize large file handling
- [ ] Make files that can't be displayed accessible via download (e.g., .clip, .psd)
- [ ] Create a list of links found in posts, note links which were successfully downloaded

## Low Priority
- [ ] Add more gallery themes
- [ ] Create Docker container
- [ ] Make zoom feature more intuitive

---

## Completed Tasks

### v1.1.0 (Unreleased)
- [x] Completely ignore AppleDouble files throughout pipeline (2025-01-XX)
  - Centralized filtering in utils.py
  - Filters in directory scanning, ZIP extraction, and video processing
  - Prevents broken thumbnails and wasted processing
