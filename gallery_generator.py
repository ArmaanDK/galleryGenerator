#!/usr/bin/env python3
"""
Art Gallery Generator - Main Entry Point
Generates a static HTML gallery from organized art directories with optional ZIP extraction.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gallery.generator import ArtGalleryGenerator


def main():
    """Main entry point for the gallery generator."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate an art gallery from organized directories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic gallery generation (with ZIP extraction by default)
  python gallery_generator.py /path/to/art
  
  # With ZIP extraction (preserves .psd, .clip files)
  python gallery_generator.py /path/to/art --extract-zips
  
  # Standard mode without ZIP processing
  python gallery_generator.py /path/to/art --no-extract-zips
  
  # With custom output and verbose logging
  python gallery_generator.py /path/to/art -o my_gallery -v --extract-zips
        """
    )
    
    parser.add_argument('art_directory', 
                       help='Path to the directory containing artist folders')
    parser.add_argument('-o', '--output', 
                       default='gallery',
                       help='Output directory for the generated gallery (default: gallery)')
    parser.add_argument('-v', '--verbose', 
                       action='store_true',
                       help='Enable verbose output')
    
    # ZIP extraction options
    zip_group = parser.add_mutually_exclusive_group()
    zip_group.add_argument('--extract-zips', 
                          action='store_true',
                          default=True,
                          help='Extract ZIP files and preserve all content including .psd, .clip files (default)')
    zip_group.add_argument('--no-extract-zips', 
                          action='store_true',
                          help='Disable ZIP extraction (standard mode)')
    
    # Download option
    parser.add_argument('-d', '--download', 
                       action='store_true',
                       help='Attempt to download content from links in posts (requires enhanced generator with download support)')
    
    args = parser.parse_args()
    
    # Validate input directory
    art_dir = Path(args.art_directory)
    if not art_dir.exists():
        print(f"Error: Art directory '{art_dir}' does not exist")
        sys.exit(1)
    
    if not art_dir.is_dir():
        print(f"Error: '{art_dir}' is not a directory")
        sys.exit(1)
    
    # Determine extraction mode
    extract_zips = args.extract_zips and not args.no_extract_zips
    
    # Choose generator based on features requested
    if extract_zips or args.download:
        # Use enhanced generator
        try:
            from gallery.enhanced_generator import EnhancedArtGalleryGenerator
            
            if args.download:
                # Use enhanced generator with download support
                generator = EnhancedArtGalleryGenerator(
                    art_dir, 
                    args.output, 
                    verbose=args.verbose,
                    extract_zips=extract_zips,
                    download_content=True
                )
                if args.verbose:
                    print("🔧 Using enhanced generator with ZIP extraction and download support")
            else:
                generator = EnhancedArtGalleryGenerator(
                    art_dir, 
                    args.output, 
                    verbose=args.verbose,
                    extract_zips=extract_zips
                )
                if args.verbose:
                    print("🔧 Using enhanced generator with ZIP extraction")
        
        except ImportError:
            print("Warning: Enhanced generator not available, falling back to standard generator")
            if args.download:
                print("Warning: Download functionality requires enhanced generator")
            generator = ArtGalleryGenerator(art_dir, args.output, verbose=args.verbose)
    else:
        # Use standard generator
        generator = ArtGalleryGenerator(art_dir, args.output, verbose=args.verbose)
        if args.verbose:
            print("🔧 Using standard generator (no ZIP extraction)")
    
    try:
        generator.generate()
        print(f"\n✅ Gallery successfully generated!")
        print(f"📁 Output: {Path(args.output).absolute()}")
        print(f"🌐 Open: file://{(Path(args.output) / 'index.html').absolute()}")
        
        # Show extraction and download reports if using enhanced generator
        if hasattr(generator, 'get_extraction_report'):
            report = generator.get_extraction_report()
            
            # ZIP extraction results
            if report['extraction_enabled'] and report['statistics']['total_zips_processed'] > 0:
                print(f"\n📦 ZIP Extraction Results:")
                stats = report['statistics']
                print(f"   • {stats['total_zips_processed']} ZIP files processed")
                print(f"   • {stats['total_files_extracted']} files extracted")
                print(f"   • {stats['artwork_files_preserved']} artwork files preserved (.psd, .clip, etc.)")
                print(f"   • Files saved to 'extracted/' folders in each post directory")
            
            # Download results
            if report.get('download_enabled') and report['download_statistics']['files_downloaded'] > 0:
                print(f"\n📥 Download Results:")
                dl_stats = report['download_statistics']
                print(f"   • {dl_stats['posts_processed']} posts with downloads")
                print(f"   • {dl_stats['files_downloaded']} files downloaded")
                print(f"   • Files saved to 'downloads/' folders in each post directory")
                
            if args.verbose and report['statistics']['total_zips_processed'] > 0:
                print(f"\n📋 Supported artwork formats:")
                artwork_formats = ', '.join(report['supported_artwork_formats'][:8])
                print(f"   {artwork_formats}, and more...")
        
        # Note if download was requested but not available
        if args.download and not hasattr(generator, 'download_content'):
            print(f"\n💡 Download functionality was requested but is not available.")
            print(f"🔧 Please ensure the ContentDownloader module is properly installed.")
    
    except Exception as e:
        print(f"❌ Error generating gallery: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()