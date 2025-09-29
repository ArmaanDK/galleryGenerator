# Contributing to Art Gallery Generator

Thank you for your interest in contributing! This guide will help you get started with the project, even if you're new to Python.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Code Style](#code-style)
- [Making Changes](#making-changes)
- [Testing Your Changes](#testing-your-changes)
- [Submitting Changes](#submitting-changes)
- [Common Tasks](#common-tasks)

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Git (for version control)
- A text editor or IDE (VS Code, PyCharm, etc.)
- Basic understanding of command line/terminal

### First Time Setup

1. **Fork the repository** on GitHub (click the "Fork" button)

2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/YOUR-USERNAME/art-gallery-generator.git
   cd art-gallery-generator
   ```

3. **Set up the upstream remote** (to sync with the main project):
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/art-gallery-generator.git
   ```

4. **Create a virtual environment**:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate it
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Test that everything works**:
   ```bash
   python3 gallery_generator.py --help
   ```

## Development Setup

### Recommended IDE Setup

**VS Code Extensions:**
- Python (Microsoft)
- Pylance
- Python Docstring Generator
- GitLens

**PyCharm:**
- Built-in Python support works great out of the box

### Testing Your Setup

Create a simple test directory structure:

```bash
mkdir -p test_art/TestArtist/"2024-01-01 Test Post"
cd test_art/TestArtist/"2024-01-01 Test Post"
# Add some test images here
cd ../../..
```

Run the generator:
```bash
python3 gallery_generator.py test_art --verbose
```

## Project Structure

Understanding where different features live:

```
art-gallery-generator/
├── gallery_generator.py          # Main entry point - CLI argument handling
├── src/gallery/
│   ├── config.py                 # Configuration constants
│   ├── utils.py                  # Helper functions (file parsing, etc.)
│   ├── video.py                  # Video thumbnail generation
│   ├── media.py                  # Standard media file handling
│   ├── enhanced_media.py         # ZIP extraction & filtering
│   ├── generator.py              # Core gallery generation logic
│   ├── enhanced_generator.py     # Enhanced features (ZIP + downloads)
│   ├── downloader.py             # Content downloading from URLs
│   ├── template_loader.py        # HTML template management
│   ├── templates/
│   │   ├── default_template.py   # Default HTML template
│   │   └── gallery_template.html # User-customizable template
│   └── static/
│       ├── default_styles.py     # Default CSS
│       ├── default_gallery.py    # Default JavaScript
│       ├── styles.css            # User-customizable CSS
│       └── gallery.js            # User-customizable JS
```

### Where to Make Changes

| What you want to change | File to edit |
|------------------------|--------------|
| Add new file format support | `config.py` (add to format lists) |
| Change thumbnail generation | `video.py` (VideoProcessor class) |
| Modify ZIP extraction logic | `enhanced_media.py` (EnhancedMediaProcessor) |
| Add new download sources | `downloader.py` (ContentDownloader) |
| Change gallery appearance | `templates/gallery_template.html` or `static/styles.css` |
| Add new CLI options | `gallery_generator.py` (argument parser) |
| Modify gallery behavior | `enhanced_generator.py` (EnhancedArtGalleryGenerator) |

## Code Style

### Python Style Guidelines

We follow **PEP 8** (Python's style guide) with these specifics:

```python
# Good: Clear variable names
def process_media_files(post_dir: Path) -> List[Dict[str, Any]]:
    """Process all media files in a directory."""
    media_files = []
    for file_path in post_dir.iterdir():
        if file_path.is_file():
            media_files.append(process_file(file_path))
    return media_files

# Bad: Unclear names, no types
def proc(d):
    m = []
    for f in d.iterdir():
        if f.is_file():
            m.append(proc_f(f))
    return m
```

### Key Style Points

1. **Use type hints** for function parameters and returns
2. **Write docstrings** for classes and functions
3. **Keep functions focused** - one function, one purpose
4. **Use meaningful variable names** - `media_files` not `mf`
5. **Add comments** for complex logic
6. **Keep lines under 100 characters** when possible

### Documentation Style

```python
def download_file(self, url: str, destination: Path) -> bool:
    """
    Download a file from URL to destination.
    
    Args:
        url: URL to download from
        destination: Directory to save file
        
    Returns:
        True if successful, False otherwise
        
    Example:
        >>> downloader.download_file("https://example.com/file.zip", Path("./downloads"))
        True
    """
    # Implementation here
```

## Making Changes

### Development Workflow

1. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** in small, logical commits:
   ```bash
   git add path/to/changed/file.py
   git commit -m "Add support for .procreate files"
   ```

3. **Keep your branch updated** with the main project:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

4. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Guidelines

Write clear commit messages:

**Good:**
```
Add support for Procreate files in ZIP extraction

- Added .procreate to EXTRACTABLE_ARTWORK_FORMATS
- Updated documentation to mention Procreate support
- Added test case for .procreate file extraction
```

**Bad:**
```
fixed stuff
```

### Branch Naming

Use descriptive branch names:
- `feature/add-procreate-support`
- `fix/appledouble-filtering`
- `docs/improve-readme`
- `refactor/simplify-media-processor`

## Testing Your Changes

### Manual Testing

Always test your changes before submitting:

1. **Create test data** that exercises your feature:
   ```bash
   # Example: Testing new file format support
   mkdir -p test_art/Artist/"2024-01-01 Test"
   # Add files with new format to test directory
   ```

2. **Run the generator** with verbose output:
   ```bash
   python3 gallery_generator.py test_art --verbose
   ```

3. **Check the output** in a browser:
   ```bash
   open gallery/index.html
   ```

4. **Test edge cases**:
   - Empty directories
   - Large files
   - Special characters in filenames
   - Missing optional features (no ffmpeg, no internet, etc.)

### Testing Checklist

Before submitting, verify:
- [ ] Code runs without errors
- [ ] Verbose mode shows appropriate messages
- [ ] Gallery displays correctly in browser
- [ ] New features work as expected
- [ ] Existing features still work (no regressions)
- [ ] Works with and without optional dependencies
- [ ] Documentation updated (if adding features)

## Submitting Changes

### Pull Request Process

1. **Push your branch** to your fork (if not already done)

2. **Create a Pull Request** on GitHub:
   - Go to the original repository
   - Click "New Pull Request"
   - Click "compare across forks"
   - Select your fork and branch
   - Write a clear description

3. **Pull Request Template**:
   ```markdown
   ## Description
   Brief description of what this PR does
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Refactoring
   
   ## Changes Made
   - Detailed list of changes
   - Include any breaking changes
   
   ## Testing Done
   - Describe how you tested
   - Include screenshots if relevant
   
   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Documentation updated
   - [ ] Tested manually
   - [ ] No breaking changes (or noted in description)
   ```

4. **Respond to feedback**:
   - Address reviewer comments
   - Make requested changes
   - Push updates to your branch (they'll appear in the PR automatically)

## Common Tasks

### Adding Support for a New File Format

1. **Update `config.py`**:
   ```python
   # Add to appropriate format set
   EXTRACTABLE_ARTWORK_FORMATS = {
       '.psd', '.clip', '.ai',
       '.procreate',  # <- Your new format
       # ... rest
   }
   ```

2. **Test extraction**:
   ```bash
   # Create test ZIP with new format
   # Run generator and verify file is extracted
   ```

3. **Update documentation**:
   - Add to README.md under "Supported File Types"
   - Add to CHANGELOG.md

### Adding a New Download Source

1. **Edit `downloader.py`**:
   ```python
   def parse_dropbox_url(self, url: str) -> Optional[str]:
       """Convert Dropbox share URL to direct download URL."""
       # Add parsing logic
       pass
   
   def download_file(self, url: str, destination: Path) -> bool:
       # Add Dropbox handling
       if 'dropbox.com' in url:
           parsed_url = self.parse_dropbox_url(url)
           # ... handle download
   ```

2. **Test with real URLs**

3. **Update skip patterns** if needed:
   ```python
   skip_patterns = [
       'patreon.com/c/',
       # Don't add Dropbox here - we want to download from it!
   ]
   ```

### Modifying the Gallery Appearance

1. **For CSS changes**, edit `src/gallery/static/styles.css`:
   ```css
   /* Custom styles */
   .post-card {
       border-radius: 8px;  /* Change from default */
   }
   ```

2. **For HTML structure**, edit `src/gallery/templates/gallery_template.html`

3. **For JavaScript behavior**, edit `src/gallery/static/gallery.js`

4. **Test in multiple browsers** (Chrome, Firefox, Safari)

### Adding a CLI Option

1. **Edit `gallery_generator.py`**:
   ```python
   parser.add_argument('--your-option',
                      action='store_true',
                      help='Description of your option')
   ```

2. **Pass to generator**:
   ```python
   generator = EnhancedArtGalleryGenerator(
       art_dir,
       args.output,
       verbose=args.verbose,
       your_option=args.your_option  # <- Add here
   )
   ```

3. **Implement in generator** (`enhanced_generator.py`)

4. **Update help text** and README

## Getting Help

### Resources for New Python Developers

- **Python Documentation**: https://docs.python.org/3/
- **PEP 8 Style Guide**: https://pep8.org/
- **Real Python Tutorials**: https://realpython.com/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html

### Project-Specific Help

- **Open an issue** with the "question" label
- **Look at closed PRs** to see how similar changes were made
- **Read existing code** - the project is well-documented

### Common Python Pitfalls for New Developers

1. **Indentation matters** - Python uses indentation for code blocks:
   ```python
   # Correct
   if condition:
       do_something()
       do_another_thing()
   
   # Wrong - IndentationError
   if condition:
   do_something()
   ```

2. **Use Path objects** for file paths (not strings):
   ```python
   # Good
   from pathlib import Path
   file_path = Path("directory") / "file.txt"
   
   # Not as good
   file_path = "directory/file.txt"  # Won't work on Windows
   ```

3. **List vs Generator** - understand when to use each:
   ```python
   # List - loads everything in memory
   files = list(directory.iterdir())
   
   # Generator - processes one at a time
   for file in directory.iterdir():
       process(file)
   ```

## Code Review Expectations

When your PR is reviewed, expect feedback on:
- Code clarity and readability
- Proper error handling
- Documentation completeness
- Test coverage
- Performance implications

**Remember**: Code review is about improving the code, not criticizing you!

## Questions?

If you're stuck or unsure:
1. Check if there's a similar implementation in the codebase
2. Look at closed issues and PRs
3. Open a new issue with the "question" label
4. Be specific about what you've tried

## Thank You!

Your contributions help make this project better for everyone. We appreciate your time and effort! 🎉