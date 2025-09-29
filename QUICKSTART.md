# Quick Start Guide for Contributors

New to Python or the project? Start here!

## ⚡ 5-Minute Setup

### 1. Install Python
```bash
# Check if Python is installed
python3 --version

# Should show: Python 3.7 or higher
# If not installed, download from: https://www.python.org/downloads/
```

### 2. Get the Code
```bash
# Fork the project on GitHub, then:
git clone https://github.com/YOUR-USERNAME/art-gallery-generator.git
cd art-gallery-generator
```

### 3. Create Test Data
```bash
# Create a simple test structure
mkdir -p test_art/TestArtist/"2024-01-01 My First Post"

# Add a test image (copy any .jpg or .png file)
cp /path/to/any/image.jpg test_art/TestArtist/"2024-01-01 My First Post"/
```

### 4. Run It!
```bash
python3 gallery_generator.py test_art --verbose
```

### 5. View Result
```bash
# Open in browser
open gallery/index.html  # macOS
xdg-open gallery/index.html  # Linux
start gallery/index.html  # Windows
```

**🎉 If you see a gallery with your test image, you're ready to contribute!**

---

## 🎯 Your First Contribution

### Easy First Issues

Look for issues labeled `good first issue` on GitHub. Here are some examples:

#### 1. Add a New File Format
**Time**: ~15 minutes  
**Skills**: None required!

```python
# Edit: src/gallery/config.py
# Add one line:

EXTRACTABLE_ARTWORK_FORMATS = {
    '.psd', '.clip', '.ai',
    '.procreate',  # <- Add this line!
    # ... rest
}
```

Then test it!

#### 2. Improve Error Messages
**Time**: ~20 minutes  
**Skills**: Basic reading

Find a confusing error message and make it clearer:

```python
# Before
print("Error processing file")

# After  
print(f"❌ Error processing {file.name}: File may be corrupted or in unsupported format")
```

#### 3. Add Emoji to Output
**Time**: ~10 minutes  
**Skills**: Copy & paste 😄

Make the verbose output more fun:

```python
# Find prints in any file and add emoji
print("✨ Starting ZIP extraction...")
print("📦 Found 5 files to extract")
print("🎉 Gallery generated successfully!")
```

---

## 🧪 Testing Your Changes

### Basic Test
```bash
# Always test with verbose to see what's happening
python3 gallery_generator.py test_art --verbose
```

### Test Different Modes
```bash
# Test ZIP extraction
python3 gallery_generator.py test_art --extract-zips --verbose

# Test without ZIP extraction
python3 gallery_generator.py test_art --no-extract-zips --verbose

# Test with downloads (need a links-*.txt file with URLs)
python3 gallery_generator.py test_art --download --verbose
```

### Check the Output
1. **Terminal**: Look for errors or warnings
2. **Browser**: Open gallery/index.html and check it works
3. **Files**: Look in gallery/ folder to see what was generated

---

## 📖 Understanding the Code

### Where Things Live

```
gallery_generator.py          ← Start here! Main entry point
│
src/gallery/
├── config.py                 ← Add file formats here
├── utils.py                  ← Helper functions
├── enhanced_media.py         ← ZIP extraction logic
├── enhanced_generator.py     ← Main gallery generator
└── downloader.py             ← Download logic
```

### Reading the Code

**Start with what you want to change:**

| I want to... | Look in... |
|-------------|-----------|
| Add a file format | `config.py` |
| Change error messages | Any file with `print(` |
| Modify ZIP extraction | `enhanced_media.py` |
| Change gallery look | `templates/` or `static/` |
| Add a CLI option | `gallery_generator.py` |

### Code Reading Tips

1. **Follow the imports**: See what the file uses
2. **Read the docstrings**: The `"""text"""` under functions
3. **Look at the types**: `def func(name: str) -> bool:` means takes string, returns boolean
4. **Search for examples**: Find similar code already in the project

---

## 🚀 Making Your First Change

### Step-by-Step

1. **Create a branch**:
   ```bash
   git checkout -b my-first-change
   ```

2. **Make ONE small change**:
   - Add a file format
   - Fix a typo
   - Improve an error message

3. **Test it**:
   ```bash
   python3 gallery_generator.py test_art --verbose
   ```

4. **Commit it**:
   ```bash
   git add .
   git commit -m "Add .procreate file format support"
   ```

5. **Push it**:
   ```bash
   git push origin my-first-change
   ```

6. **Create Pull Request** on GitHub

---

## 🆘 Getting Help

### "It's not working!"

**Step 1**: Check for error messages
```bash
# Run with verbose
python3 gallery_generator.py test_art --verbose
```

**Step 2**: Common issues

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Make sure you're in the right directory |
| `FileNotFoundError` | Check your test_art directory exists |
| `No module named 'gallery'` | Run from project root, not from src/ |
| `SyntaxError` | Check your Python version is 3.7+ |

**Step 3**: Ask for help
- Open an issue on GitHub
- Include the error message
- Show what you tried

### "I don't understand the code!"

**That's normal!** Here's what to do:

1. **Focus on one small part** - Don't try to understand everything
2. **Look for patterns** - Similar code is often nearby
3. **Add print statements** - See what values variables have
4. **Ask questions** - Open an issue with "question" label

### Python Basics You Need

You really only need to know:
- **Variables**: `name = "value"`
- **Functions**: `def do_something():`
- **If statements**: `if condition:`
- **For loops**: `for item in list:`
- **Import**: `from module import function`

That's it! You can learn as you go.

---

## 🎓 Learning Resources

### If You're New to Python
- [Python.org Tutorial](https://docs.python.org/3/tutorial/) - Official tutorial
- [Real Python](https://realpython.com/) - Practical tutorials
- [Python for Beginners](https://www.pythonforbeginners.com/) - Beginner friendly

### If You're New to Git
- [GitHub Guides](https://guides.github.com/) - Official guides
- [Git Handbook](https://guides.github.com/introduction/git-handbook/) - Quick reference
- [Oh Shit, Git!](https://ohshitgit.com/) - Fixing mistakes

### Project-Specific
- [CONTRIBUTING.md](CONTRIBUTING.md) - Detailed contribution guide
- [DEVELOPMENT.md](DEVELOPMENT.md) - Technical architecture
- [README.md](README.md) - User documentation

---

## ✅ Before You Submit

Quick checklist:

- [ ] Code runs without errors
- [ ] Tested with `--verbose` flag
- [ ] Gallery displays correctly in browser
- [ ] One logical change (not mixing multiple features)
- [ ] Commit message describes what changed
- [ ] No personal/test files committed

---

## 🎉 You're Ready!

Remember:
- **Start small** - One line changes are great!
- **Ask questions** - No question is too basic
- **Have fun** - You're learning and helping!
- **Be patient** - Everyone was a beginner once

**Need help? Open an issue with the "question" label!**

Happy contributing! 🚀