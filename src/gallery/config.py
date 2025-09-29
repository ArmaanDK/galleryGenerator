"""
Configuration settings for the Art Gallery Generator
"""

# Supported file formats
SUPPORTED_IMAGE_FORMATS = {'.jpeg', '.jpg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
SUPPORTED_VIDEO_FORMATS = {'.mp4', '.webm', '.mov', '.avi', '.mkv', '.flv'}

# ZIP extraction settings
EXTRACT_ZIPS_BY_DEFAULT = True
PRESERVE_ORIGINAL_ZIPS = True  # Keep original ZIP files after extraction

# Comprehensive list of extractable file types
EXTRACTABLE_ARTWORK_FORMATS = {
    # Adobe Creative Suite
    '.psd',     # Photoshop
    '.ai',      # Illustrator
    '.indd',    # InDesign
    '.aep',     # After Effects
    '.prproj',  # Premiere Pro
    
    # Clip Studio Paint
    '.clip',    # Clip Studio Paint
    '.lip',     # Clip Studio Paint (older)
    
    # Other Digital Art Software
    '.xcf',     # GIMP
    '.kra',     # Krita
    '.ora',     # OpenRaster
    '.sai',     # Paint Tool SAI
    '.sai2',    # Paint Tool SAI 2
    '.mdp',     # FireAlpaca/MediBang
    
    # Design Software
    '.sketch',      # Sketch
    '.fig',         # Figma (exported)
    '.afdesign',    # Affinity Designer
    '.afphoto',     # Affinity Photo
    '.afpub',       # Affinity Publisher
    
    # 3D Software
    '.blend',   # Blender
    '.c4d',     # Cinema 4D
    '.max',     # 3ds Max
    '.ma',      # Maya ASCII
    '.mb',      # Maya Binary
    '.fbx',     # FBX
    '.obj',     # Wavefront OBJ
    '.dae',     # Collada
    
    # Vector Graphics
    '.svg',     # Scalable Vector Graphics
    '.eps',     # Encapsulated PostScript
    '.pdf',     # Portable Document Format
    
    # CAD Formats
    '.dwg',     # AutoCAD
    '.dxf',     # Drawing Exchange Format
}

EXTRACTABLE_DOCUMENT_FORMATS = {
    '.txt', '.md', '.rtf', '.doc', '.docx', '.odt',
    '.pdf', '.html', '.xml', '.json', '.csv'
}

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

# ZIP extraction behavior
EXTRACTION_SETTINGS = {
    'extract_zips': EXTRACT_ZIPS_BY_DEFAULT,
    'preserve_originals': PRESERVE_ORIGINAL_ZIPS,
    'flatten_structure': True,  # Move files from subdirs to root of extracted/
    'skip_system_files': True,  # Skip __MACOSX, .DS_Store, etc.
    'max_file_size_mb': 100,    # Skip files larger than this (per file)
    'max_total_size_mb': 500,   # Skip ZIP if total extracted size exceeds this
}