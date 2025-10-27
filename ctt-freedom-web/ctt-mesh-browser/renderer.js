// Navigation history
let history = [];
let historyIndex = -1;
let currentHash = null;

// Elements
const addressInput = document.getElementById('addressInput');
const goBtn = document.getElementById('goBtn');
const backBtn = document.getElementById('backBtn');
const forwardBtn = document.getElementById('forwardBtn');
const refreshBtn = document.getElementById('refreshBtn');
const homeBtn = document.getElementById('homeBtn');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const infoBar = document.getElementById('infoBar');
const infoText = document.getElementById('infoText');

const homeScreen = document.getElementById('homeScreen');
const contentFrame = document.getElementById('contentFrame');
const loadingScreen = document.getElementById('loadingScreen');
const errorScreen = document.getElementById('errorScreen');
const contentIframe = document.getElementById('contentIframe');

// Check daemon status
async function updateStatus() {
    const result = await window.meshAPI.getStatus();
    
    if (result.success) {
        statusDot.className = 'status-dot online';
        statusText.textContent = 'Online';
        
        const data = result.data;
        document.getElementById('homeStatusText').textContent = 'Online ✓';
        document.getElementById('homeNodeCount').textContent = data.nodes || 1;
        document.getElementById('homeCacheSize').textContent = formatBytes(data.cache_size || 0);
    } else {
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'Offline';
        document.getElementById('homeStatusText').textContent = 'Offline ✗';
    }
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Navigate to content hash
async function navigate(hash) {
    if (!hash || hash.length !== 64) {
        showError('Invalid content hash. Must be 64 hexadecimal characters.');
        return;
    }
    
    showLoading();
    addressInput.value = hash;
    currentHash = hash;
    
    // Add to history
    if (historyIndex < history.length - 1) {
        history = history.slice(0, historyIndex + 1);
    }
    history.push(hash);
    historyIndex = history.length - 1;
    updateNavButtons();
    
    const result = await window.meshAPI.retrieveContent(hash);
    
    if (result.success && result.data.success) {
        const content = result.data.content;
        const source = result.data.source;
        
        // Update info bar
        infoText.textContent = `Retrieved from ${source.toUpperCase()} • ctt://${hash}`;
        
        // Display content
        contentIframe.srcdoc = content;
        showContent();
    } else {
        const error = result.data?.error || result.error || 'Content not found';
        showError(error);
    }
}

// Screen transitions
function showHome() {
    homeScreen.style.display = 'block';
    contentFrame.style.display = 'none';
    loadingScreen.style.display = 'none';
    errorScreen.style.display = 'none';
    addressInput.value = '';
    currentHash = null;
    infoText.textContent = 'CTT Mesh Network';
}

function showContent() {
    homeScreen.style.display = 'none';
    contentFrame.style.display = 'block';
    loadingScreen.style.display = 'none';
    errorScreen.style.display = 'none';
}

function showLoading() {
    homeScreen.style.display = 'none';
    contentFrame.style.display = 'none';
    loadingScreen.style.display = 'flex';
    errorScreen.style.display = 'none';
}

function showError(message) {
    homeScreen.style.display = 'none';
    contentFrame.style.display = 'none';
    loadingScreen.style.display = 'none';
    errorScreen.style.display = 'flex';
    document.getElementById('errorMessage').textContent = message;
}

function closeInfoBar() {
    infoBar.style.display = 'none';
}

function updateNavButtons() {
    backBtn.disabled = historyIndex <= 0;
    forwardBtn.disabled = historyIndex >= history.length - 1;
}

// Event listeners
goBtn.addEventListener('click', () => {
    const hash = addressInput.value.trim().replace(/^ctt:\/\//, '');
    navigate(hash);
});

addressInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const hash = addressInput.value.trim().replace(/^ctt:\/\//, '');
        navigate(hash);
    }
});

backBtn.addEventListener('click', () => {
    if (historyIndex > 0) {
        historyIndex--;
        navigate(history[historyIndex]);
    }
});

forwardBtn.addEventListener('click', () => {
    if (historyIndex < history.length - 1) {
        historyIndex++;
        navigate(history[historyIndex]);
    }
});

refreshBtn.addEventListener('click', () => {
    if (currentHash) {
        navigate(currentHash);
    }
});

homeBtn.addEventListener('click', () => {
    showHome();
});

// Initialize
updateStatus();
setInterval(updateStatus, 5000);
updateNavButtons();
