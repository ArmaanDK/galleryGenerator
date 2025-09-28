"""
Template loading and rendering for the Art Gallery Generator
"""

import json
from pathlib import Path
from typing import List, Dict, Any


class TemplateLoader:
    """Handles loading and rendering of HTML templates."""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent / "templates"
        self.static_dir = Path(__file__).parent / "static"
    
    def load_css(self) -> str:
        """Load CSS styles."""
        css_file = self.static_dir / "styles.css"
        if css_file.exists():
            return css_file.read_text(encoding='utf-8')
        return self._get_default_css()
    
    def load_js(self) -> str:
        """Load JavaScript code."""
        js_file = self.static_dir / "gallery.js"
        if js_file.exists():
            return js_file.read_text(encoding='utf-8')
        return self._get_default_js()
    
    def load_template(self) -> str:
        """Load HTML template."""
        template_file = self.template_dir / "gallery_template.html"
        if template_file.exists():
            return template_file.read_text(encoding='utf-8')
        return self._get_default_template()
    
    def render_gallery(self, posts: List[Dict[str, Any]], gallery_title: str) -> str:
        """
        Render the complete gallery HTML.
        
        Args:
            posts: List of post data
            gallery_title: Title for the gallery
            
        Returns:
            Complete HTML string
        """
        template = self.load_template()
        
        # Safely encode posts data for JavaScript
        posts_json = json.dumps(posts, ensure_ascii=True, separators=(',', ':'))
        
        # Replace template variables
        html = template.replace('{{ gallery_title }}', gallery_title)
        html = html.replace('{{ posts_json }}', posts_json)
        html = html.replace('{{ css_content }}', self.load_css())
        html = html.replace('{{ js_content }}', self.load_js())
        
        return html
    
    def _get_default_template(self) -> str:
        """Get default HTML template if file doesn't exist."""
        from .templates.default_template import DEFAULT_HTML_TEMPLATE
        return DEFAULT_HTML_TEMPLATE

    def _get_default_css(self) -> str:
        """Get default CSS if file doesn't exist."""
        from .static.default_styles import DEFAULT_CSS
        return DEFAULT_CSS

    def _get_default_js(self) -> str:
        """Get default JavaScript if file doesn't exist."""
        from .static.default_gallery import DEFAULT_JAVASCRIPT
        return DEFAULT_JAVASCRIPT