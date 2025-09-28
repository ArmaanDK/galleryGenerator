"""
Default CSS styles for the Art Gallery Generator
"""

DEFAULT_CSS = '''
:root {
    --bg-primary: #f5f5f5;
    --bg-secondary: #ffffff;
    --text-primary: #333333;
    --text-secondary: #666666;
    --accent-color: #ff6b35;
    --border-color: #dddddd;
    --shadow-light: rgba(0, 0, 0, 0.1);
    --shadow-medium: rgba(0, 0, 0, 0.15);
    --modal-overlay: rgba(0, 0, 0, 0.9);
}

[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d2d2d;
    --text-primary: #e0e0e0;
    --text-secondary: #b0b0b0;
    --accent-color: #ff6b35;
    --border-color: #404040;
    --shadow-light: rgba(0, 0, 0, 0.3);
    --shadow-medium: rgba(0, 0, 0, 0.4);
    --modal-overlay: rgba(0, 0, 0, 0.95);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.header {
    background: var(--bg-secondary);
    padding: 1rem 2rem;
    box-shadow: 0 2px 10px var(--shadow-light);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header h1 {
    color: var(--accent-color);
    font-size: 2rem;
    display: inline-block;
    margin-right: 2rem;
}

.header-controls {
    display: inline-flex;
    align-items: center;
    gap: 1rem;
}

.theme-toggle {
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: 20px;
    padding: 0.4rem 0.8rem;
    color: var(--text-primary);
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.theme-toggle:hover {
    border-color: var(--accent-color);
    color: var(--accent-color);
}

.filters {
    margin: 1rem 0;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.filter-input, .filter-select {
    padding: 0.5rem;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    font-size: 1rem;
    background: var(--bg-secondary);
    color: var(--text-primary);
    transition: all 0.3s ease;
}

.filter-input:focus, .filter-select:focus {
    outline: none;
    border-color: var(--accent-color);
}

.filter-input { min-width: 200px; }
.filter-select { min-width: 120px; }

.media-filters {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    align-items: center;
}

.media-filters-label {
    font-weight: 500;
    color: var(--text-primary);
    margin-right: 0.5rem;
}

.media-filter-btn {
    padding: 0.4rem 0.8rem;
    border: 2px solid var(--border-color);
    border-radius: 20px;
    background: var(--bg-secondary);
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    user-select: none;
}

.media-filter-btn:hover {
    border-color: var(--accent-color);
    color: var(--accent-color);
}

.media-filter-btn.active {
    background: var(--accent-color);
    border-color: var(--accent-color);
    color: white;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 2rem;
}

.post-card {
    background: var(--bg-secondary);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px var(--shadow-light);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}

.post-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px var(--shadow-medium);
}

.post-thumbnail {
    width: 100%;
    height: 250px;
    object-fit: cover;
}

.video-placeholder {
    width: 100%;
    height: 250px;
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--border-color) 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
}

.video-icon { font-size: 3rem; margin-bottom: 0.5rem; }

.post-info { padding: 1rem; }

.post-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
}

.post-artist {
    color: var(--accent-color);
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.post-date {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.post-text {
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.5;
    max-height: 60px;
    overflow: hidden;
}

.media-count {
    background: var(--accent-color);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.8rem;
    display: inline-block;
    margin-top: 0.5rem;
}

/* Modal styles */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0; top: 0;
    width: 100%; height: 100%;
    background-color: var(--modal-overlay);
}

.modal-content {
    position: relative;
    margin: 2% auto;
    width: 90%;
    max-width: 1000px;
    background: var(--bg-secondary);
    border-radius: 12px;
    overflow: hidden;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    padding: 1rem 2rem;
    background: var(--accent-color);
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.close { font-size: 2rem; cursor: pointer; color: white; }
.modal-body { padding: 2rem; }

.media-viewer {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
    position: relative;
}

.media-item {
    max-width: 100%;
    border-radius: 8px;
    transition: transform 0.3s ease;
    user-select: none;
}

.media-item.image { cursor: zoom-in; }
.media-item.video { cursor: default; }
.media-item.zoomed { cursor: grab; }
.media-item.zoomed.dragging { cursor: grabbing; transition: none; }
.media-item.fit-window { max-height: calc(90vh - 250px); object-fit: contain; }

.zoom-controls {
    position: absolute;
    top: 10px; right: 10px;
    display: flex;
    gap: 0.5rem;
    z-index: 15;
}

.zoom-btn {
    background: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    width: 35px; height: 35px;
    border-radius: 50%;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.zoom-btn:hover { background: rgba(255, 107, 53, 0.9); }
.zoom-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.media-hover-zone {
    position: absolute;
    top: 25%; bottom: 25%;
    width: 25%;
    z-index: 5;
    display: flex;
    align-items: center;
    cursor: pointer;
}

.media-hover-zone.left { left: 0; justify-content: flex-start; padding-left: 20px; }
.media-hover-zone.right { right: 0; justify-content: flex-end; padding-right: 20px; }

.media-nav-arrow {
    background: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    width: 50px; height: 50px;
    border-radius: 50%;
    font-size: 20px;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.2s ease;
}

.media-hover-zone:hover .media-nav-arrow { opacity: 0.4; }
.media-hover-zone .media-nav-arrow:hover { opacity: 1 !important; }
.media-viewer.single-media .media-hover-zone { display: none; }

.media-navigation {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    overflow-x: auto;
}

.media-thumb {
    width: 80px; height: 80px;
    object-fit: cover;
    cursor: pointer;
    border-radius: 4px;
    border: 3px solid transparent;
    transition: border-color 0.3s;
}

.media-thumb.active { border-color: var(--accent-color); }
.media-thumb.video {
    background: var(--border-color);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Fullscreen button styles */
.fullscreen-btn {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    border-radius: 4px;
    padding: 0.3rem 0.6rem;
    font-size: 1rem;
    cursor: pointer;
    margin-left: 1rem;
    transition: all 0.3s ease;
    float: right;
}

.fullscreen-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
}

/* Fullscreen modal styles */
.modal.fullscreen-mode {
    background-color: rgba(0, 0, 0, 0.98);
}

.modal-content.fullscreen-content {
    margin: 0;
    width: 100vw;
    height: 100vh;
    max-width: none;
    max-height: none;
    border-radius: 0;
    display: flex;
    flex-direction: column;
}

.fullscreen-content .modal-header {
    display: none;
}

.fullscreen-content .modal-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 0;
    overflow: hidden;
}

.fullscreen-content .media-viewer {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-bottom: 0;
}

.fullscreen-content .media-item {
    max-width: 100vw;
    max-height: 100vh;
    object-fit: contain;
}

.fullscreen-content .media-navigation {
    display: none;
}

.fullscreen-content #modalText {
    display: none;
}

/* Fullscreen left hover zone styling */
.fullscreen-content .media-hover-zone.left {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: space-between;
    padding: 20px;
    top: 0;
    bottom: 0;
    height: 100%;
    gap: 10px;
}

.fullscreen-content .media-hover-zone.left .fullscreen-exit-btn {
    background: rgba(0, 0, 0, 0.8);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    opacity: 1;
    align-self: flex-start;
}

.fullscreen-content .media-hover-zone.left .fullscreen-exit-btn:hover {
    background: rgba(255, 107, 53, 0.9);
    border-color: rgba(255, 255, 255, 0.5);
}

.fullscreen-content .media-hover-zone.left .media-nav-arrow {
    background: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    font-size: 20px;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.2s ease;
    align-self: flex-start;
    margin-top: auto;
    margin-bottom: auto;
}

.fullscreen-content .media-hover-zone.left:hover .media-nav-arrow {
    opacity: 0.4;
}

.fullscreen-content .media-hover-zone.left .media-nav-arrow:hover {
    opacity: 1 !important;
}

/* Special handling for fullscreen single media */
.fullscreen-content .media-viewer.single-media .media-hover-zone.left {
    display: flex;
    pointer-events: none;
}

.fullscreen-content .media-viewer.single-media .media-hover-zone.left .fullscreen-exit-btn {
    pointer-events: auto;
}

.fullscreen-content .media-viewer.single-media .media-hover-zone.left .media-nav-arrow {
    display: none;
}

.fullscreen-content .media-viewer.single-media .media-hover-zone.right {
    display: none;
}

@media (max-width: 768px) {
    .container { padding: 1rem; }
    .gallery { grid-template-columns: 1fr; gap: 1rem; }
    .filters { flex-direction: column; }
}
'''