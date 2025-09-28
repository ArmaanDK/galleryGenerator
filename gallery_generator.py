#!/usr/bin/env python3
"""
Art Gallery Generator - Main Entry Point
Generates a static HTML gallery from organized art directories.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gallery.generator import ArtGalleryGenerator

def main():
    """Main entry point for the gallery generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate an art gallery from organized directories')
    parser.add_argument('art_directory', 
                       help='Path to the directory containing artist folders')
    parser.add_argument('-o', '--output', 
                       default='gallery',
                       help='Output directory for the generated gallery (default: gallery)')
    parser.add_argument('-v', '--verbose', 
                       action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Validate input directory
    art_dir = Path(args.art_directory)
    if not art_dir.exists():
        print(f"Error: Art directory '{art_dir}' does not exist")
        sys.exit(1)
    
    if not art_dir.is_dir():
        print(f"Error: '{art_dir}' is not a directory")
        sys.exit(1)
    
    # Create generator and run
    generator = ArtGalleryGenerator(art_dir, args.output, verbose=args.verbose)
    
    try:
        generator.generate()
        print(f"\n✅ Gallery successfully generated!")
        print(f"📁 Output: {Path(args.output).absolute()}")
        print(f"🌐 Open: file://{(Path(args.output) / 'index.html').absolute()}")
    except Exception as e:
        print(f"❌ Error generating gallery: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()