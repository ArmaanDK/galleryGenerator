"""
Default JavaScript for the Art Gallery Generator
"""

DEFAULT_JAVASCRIPT = '''
// Theme management and state variables
let currentZoom = 1;
let fitWindowMode = true;
let isDragging = false;
let dragStartX = 0, dragStartY = 0;
let imageOffsetX = 0, imageOffsetY = 0;
let currentPosts = posts;
let currentPostIndex = -1;
let currentMediaIndex = 0;
let activeMediaFilter = 'all';
let isFullscreen = false;

function initializeTheme() {
    const savedTheme = localStorage.getItem('gallery-theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
    applyTheme(theme);
    
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('gallery-theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');
    
    if (theme === 'dark') {
        themeIcon.textContent = '☀️';
        themeText.textContent = 'Light';
    } else {
        themeIcon.textContent = '🌙';
        themeText.textContent = 'Dark';
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    localStorage.setItem('gallery-theme', newTheme);
}

function toggleFullscreen() {
    const modal = document.getElementById('modal');
    const modalContent = document.querySelector('.modal-content');
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    const leftHoverZone = document.querySelector('.media-hover-zone.left');
    
    isFullscreen = !isFullscreen;
    
    if (isFullscreen) {
        modal.classList.add('fullscreen-mode');
        modalContent.classList.add('fullscreen-content');
        if (fullscreenBtn) {
            fullscreenBtn.innerHTML = '⤓';
            fullscreenBtn.title = 'Exit fullscreen';
        }
        
        // Add exit button to left hover zone but keep the arrow functional
        if (leftHoverZone && !leftHoverZone.querySelector('.fullscreen-exit-btn')) {
            const exitBtn = document.createElement('button');
            exitBtn.className = 'fullscreen-exit-btn';
            exitBtn.innerHTML = '⤓ Exit';
            exitBtn.title = 'Exit fullscreen';
            exitBtn.onclick = function(e) {
                e.stopPropagation();
                toggleFullscreen();
            };
            leftHoverZone.insertBefore(exitBtn, leftHoverZone.firstChild);
        }
    } else {
        modal.classList.remove('fullscreen-mode');
        modalContent.classList.remove('fullscreen-content');
        if (fullscreenBtn) {
            fullscreenBtn.innerHTML = '⤢';
            fullscreenBtn.title = 'Enter fullscreen';
        }
        
        // Remove exit button from left hover zone
        const exitBtn = document.querySelector('.fullscreen-exit-btn');
        if (exitBtn) {
            exitBtn.remove();
        }
    }
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric', month: 'long', day: 'numeric'
    });
}

function createPostCard(post, index) {
    let thumbnailHtml;
    if (post.thumbnail) {
        thumbnailHtml = `<img src="${post.thumbnail}" alt="${post.title}" class="post-thumbnail" loading="lazy">`;
    } else {
        thumbnailHtml = `<div class="video-placeholder"><div class="video-icon">🎬</div><div>Video Post</div></div>`;
    }
    
    return `
        <div class="post-card" onclick="openModal(${index})">
            ${thumbnailHtml}
            <div class="post-info">
                <div class="post-artist">${post.artist}</div>
                <div class="post-title">${post.title}</div>
                <div class="post-date">${formatDate(post.date)}</div>
                <div class="post-text">${post.text.replace(/\\\\n/g, ' ')}</div>
                <div class="media-count">${post.media.length} item${post.media.length > 1 ? 's' : ''}</div>
            </div>
        </div>
    `;
}

function renderGallery() {
    const gallery = document.getElementById('gallery');
    gallery.innerHTML = currentPosts.map((post, index) => createPostCard(post, index)).join('');
}

function populateArtistFilter() {
    const artists = [...new Set(posts.map(post => post.artist))].sort();
    const select = document.getElementById('artistFilter');
    artists.forEach(artist => {
        const option = document.createElement('option');
        option.value = artist;
        option.textContent = artist;
        select.appendChild(option);
    });
}

function getPostMediaTypes(post) {
    const hasImages = post.media.some(m => m.type === 'image');
    const hasGifs = post.media.some(m => m.type === 'gif');
    const hasVideos = post.media.some(m => m.type === 'video');
    return { hasImages, hasGifs, hasVideos, typeCount: [hasImages, hasGifs, hasVideos].filter(Boolean).length };
}

function initializeMediaButtons() {
    const buttons = document.querySelectorAll('.media-filter-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            buttons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            activeMediaFilter = this.getAttribute('data-media');
            filterPosts();
        });
    });
}

function filterPosts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const selectedArtist = document.getElementById('artistFilter').value;
    const sortType = document.getElementById('sortFilter').value;
    
    let filtered = posts.filter(post => {
        const matchesSearch = !searchTerm || 
            post.title.toLowerCase().includes(searchTerm) ||
            post.text.toLowerCase().includes(searchTerm) ||
            post.artist.toLowerCase().includes(searchTerm);
        
        const matchesArtist = !selectedArtist || post.artist === selectedArtist;
        
        let matchesMedia = true;
        if (activeMediaFilter !== 'all') {
            const mediaTypes = getPostMediaTypes(post);
            switch(activeMediaFilter) {
                case 'images': matchesMedia = mediaTypes.hasImages; break;
                case 'gifs': matchesMedia = mediaTypes.hasGifs; break;
                case 'videos': matchesMedia = mediaTypes.hasVideos; break;
                case 'mixed': matchesMedia = mediaTypes.typeCount > 1; break;
            }
        }
        
        return matchesSearch && matchesArtist && matchesMedia;
    });
    
    // Sort posts
    const sorted = [...filtered];
    switch(sortType) {
        case 'date-asc': currentPosts = sorted.sort((a, b) => new Date(a.date) - new Date(b.date)); break;
        case 'date-desc': currentPosts = sorted.sort((a, b) => new Date(b.date) - new Date(a.date)); break;
        case 'artist-asc': currentPosts = sorted.sort((a, b) => a.artist.localeCompare(b.artist)); break;
        case 'artist-desc': currentPosts = sorted.sort((a, b) => b.artist.localeCompare(a.artist)); break;
        case 'title-asc': currentPosts = sorted.sort((a, b) => a.title.localeCompare(b.title)); break;
        case 'title-desc': currentPosts = sorted.sort((a, b) => b.title.localeCompare(a.title)); break;
        default: currentPosts = sorted.sort((a, b) => new Date(b.date) - new Date(a.date));
    }
    
    renderGallery();
}

function openModal(postIndex) {
    const post = currentPosts[postIndex];
    document.getElementById('modalTitle').innerHTML = `
        ${post.artist} - ${post.title}
        <button class="fullscreen-btn" id="fullscreenBtn" onclick="toggleFullscreen()" title="Enter fullscreen">⤢</button>
    `;
    document.getElementById('modalText').innerHTML = post.text.replace(/\\\\n/g, '<br>');
    
    // Reset fullscreen state when opening modal
    isFullscreen = false;
    document.getElementById('modal').classList.remove('fullscreen-mode');
    document.querySelector('.modal-content').classList.remove('fullscreen-content');
    
    const mediaNav = document.getElementById('mediaNavigation');
    mediaNav.innerHTML = post.media.map((media, index) => {
        if (media.type === 'image' || media.type === 'gif') {
            return `<img src="${media.path}" class="media-thumb ${index === 0 ? 'active' : ''}" onclick="showMedia(${postIndex}, ${index})">`;
        } else {
            if (media.thumbnail) {
                return `<img src="${media.thumbnail}" class="media-thumb ${index === 0 ? 'active' : ''}" onclick="showMedia(${postIndex}, ${index})">`;
            } else {
                return `<div class="media-thumb video ${index === 0 ? 'active' : ''}" onclick="showMedia(${postIndex}, ${index})">🎬</div>`;
            }
        }
    }).join('');
    
    showMedia(postIndex, 0);
    document.getElementById('modal').style.display = 'block';
}

function showMedia(postIndex, mediaIndex) {
    const post = currentPosts[postIndex];
    const media = post.media[mediaIndex];
    const viewer = document.getElementById('mediaViewer');
    
    currentPostIndex = postIndex;
    currentMediaIndex = mediaIndex;
    
    // Reset zoom state
    currentZoom = 1;
    fitWindowMode = true;
    imageOffsetX = 0;
    imageOffsetY = 0;
    
    // Update navigation
    document.querySelectorAll('.media-thumb').forEach((thumb, index) => {
        thumb.classList.toggle('active', index === mediaIndex);
    });
    
    viewer.classList.toggle('single-media', post.media.length <= 1);
    
    // Remove existing media
    const existingMedia = viewer.querySelector('.media-item');
    if (existingMedia) existingMedia.remove();
    
    // Add new media
    if (media.type === 'image' || media.type === 'gif') {
        const mediaHtml = `<img src="${media.path}" class="media-item image fit-window" alt="${media.filename}">`;
        viewer.querySelector('.media-hover-zone.right').insertAdjacentHTML('beforebegin', mediaHtml);
        
        const img = viewer.querySelector('.media-item');
        setupImageInteractions(img);
        document.getElementById('zoomControls').style.display = 'flex';
        updateZoomControls();
    } else {
        const mediaHtml = `<video src="${media.path}" class="media-item video fit-window" controls></video>`;
        viewer.querySelector('.media-hover-zone.right').insertAdjacentHTML('beforebegin', mediaHtml);
        document.getElementById('zoomControls').style.display = 'none';
    }
}

function setupImageInteractions(img) {
    img.addEventListener('click', (e) => {
        if (isDragging || currentZoom > 1) return;
        const rect = e.target.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const clickedZone = x / rect.width;
        if (clickedZone > 0.25 && clickedZone < 0.75) toggleZoom();
    });
    
    img.addEventListener('mousedown', (e) => {
        if (currentZoom <= 1) return;
        isDragging = true;
        dragStartX = e.clientX - imageOffsetX;
        dragStartY = e.clientY - imageOffsetY;
        e.target.classList.add('dragging');
        e.preventDefault();
    });
    
    img.addEventListener('mousemove', (e) => {
        if (!isDragging || currentZoom <= 1) return;
        imageOffsetX = e.clientX - dragStartX;
        imageOffsetY = e.clientY - dragStartY;
        updateImageTransform();
        e.preventDefault();
    });
    
    img.addEventListener('mouseup', (e) => {
        if (isDragging) {
            isDragging = false;
            e.target.classList.remove('dragging');
        }
    });
    
    img.addEventListener('dragstart', (e) => e.preventDefault());
}

function updateImageTransform() {
    const img = document.querySelector('.media-item');
    if (!img || img.tagName !== 'IMG') return;
    
    if (fitWindowMode) {
        img.style.transform = '';
    } else {
        img.style.transform = `translate(${imageOffsetX}px, ${imageOffsetY}px) scale(${currentZoom})`;
    }
}

function toggleZoom() {
    if (currentZoom === 1) {
        zoomImage(1);
    } else {
        resetZoom();
    }
}

function zoomImage(delta) {
    const img = document.querySelector('.media-item');
    if (!img || img.tagName !== 'IMG') return;
    
    currentZoom = Math.max(0.5, Math.min(5, currentZoom + delta));
    fitWindowMode = false;
    
    if (currentZoom <= 1) {
        imageOffsetX = 0;
        imageOffsetY = 0;
    }
    
    img.classList.remove('fit-window');
    img.classList.toggle('zoomed', currentZoom > 1);
    updateImageTransform();
    updateZoomControls();
}

function resetZoom() {
    const img = document.querySelector('.media-item');
    if (!img || img.tagName !== 'IMG') return;
    
    currentZoom = 1;
    fitWindowMode = false;
    imageOffsetX = 0;
    imageOffsetY = 0;
    
    img.classList.remove('fit-window', 'zoomed');
    updateImageTransform();
    updateZoomControls();
}

function toggleFitWindow() {
    const img = document.querySelector('.media-item');
    if (!img || img.tagName !== 'IMG') return;
    
    fitWindowMode = !fitWindowMode;
    
    if (fitWindowMode) {
        currentZoom = 1;
        imageOffsetX = 0;
        imageOffsetY = 0;
        img.classList.add('fit-window');
        img.classList.remove('zoomed');
    } else {
        img.classList.remove('fit-window');
        img.classList.toggle('zoomed', currentZoom > 1);
    }
    
    updateImageTransform();
    updateZoomControls();
}

function updateZoomControls() {
    const fitBtn = document.getElementById('fitBtn');
    const zoomOutBtn = document.getElementById('zoomOutBtn');
    const zoomInBtn = document.getElementById('zoomInBtn');
    const resetBtn = document.getElementById('resetBtn');
    
    fitBtn.style.background = fitWindowMode ? 'rgba(255, 107, 53, 0.9)' : 'rgba(0, 0, 0, 0.7)';
    zoomOutBtn.disabled = currentZoom <= 0.5;
    zoomInBtn.disabled = currentZoom >= 5;
    resetBtn.disabled = currentZoom === 1 && !fitWindowMode;
}

function navigateMedia(direction) {
    if (currentPostIndex === -1) return;
    
    const post = currentPosts[currentPostIndex];
    const totalMedia = post.media.length;
    
    if (totalMedia <= 1) return;
    
    let newIndex = currentMediaIndex + direction;
    
    if (newIndex < 0) {
        newIndex = totalMedia - 1;
    } else if (newIndex >= totalMedia) {
        newIndex = 0;
    }
    
    showMedia(currentPostIndex, newIndex);
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    currentPostIndex = -1;
    currentMediaIndex = 0;
    
    // Reset fullscreen state
    isFullscreen = false;
    document.getElementById('modal').classList.remove('fullscreen-mode');
    document.querySelector('.modal-content').classList.remove('fullscreen-content');
}

// Event listeners
document.getElementById('searchInput').addEventListener('input', filterPosts);
document.getElementById('artistFilter').addEventListener('change', filterPosts);
document.getElementById('sortFilter').addEventListener('change', filterPosts);

document.querySelector('.close').addEventListener('click', closeModal);

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) closeModal();
});

// Keyboard navigation
document.addEventListener('keydown', function(event) {
    const modal = document.getElementById('modal');
    if (modal.style.display !== 'block') return;
    
    switch(event.key) {
        case 'ArrowLeft':
            event.preventDefault();
            navigateMedia(-1);
            break;
        case 'ArrowRight':
            event.preventDefault();
            navigateMedia(1);
            break;
        case 'Escape':
            event.preventDefault();
            closeModal();
            break;
        case '+':
        case '=':
            event.preventDefault();
            zoomImage(0.5);
            break;
        case '-':
            event.preventDefault();
            zoomImage(-0.5);
            break;
        case '0':
            event.preventDefault();
            resetZoom();
            break;
        case 'f':
        case 'F':
            if (!event.target.matches('input')) {
                event.preventDefault();
                toggleFitWindow();
            }
            break;
        case 'F11':
            event.preventDefault();
            toggleFullscreen();
            break;
    }
});

// Initialize
initializeTheme();
populateArtistFilter();
initializeMediaButtons();
renderGallery();
'''