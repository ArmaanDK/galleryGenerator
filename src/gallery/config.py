"""
Configuration settings for the Art Gallery Generator
"""

# Supported file formats
SUPPORTED_IMAGE_FORMATS = {'.jpeg', '.jpg', '.png', '.gif', '.webp'}
SUPPORTED_VIDEO_FORMATS = {'.mp4', '.webm', '.mov', '.avi'}

# Video thumbnail settings
THUMBNAIL_SIZE = "320:240"
THUMBNAIL_TIMESTAMP_PERCENT = 0.1  # 10% into the video
MIN_THUMBNAIL_TIMESTAMP = 1.0  # At least 1 second
MAX_THUMBNAIL_TIMESTAMP = 5.0  # But not more than 5 seconds

# Gallery settings
GALLERY_TITLE = "🎨 Art Gallery"
DEFAULT_OUTPUT_DIR = "gallery"

# Template paths (relative to this file)
TEMPLATE_DIR = "templates"
STATIC_DIR = "static"