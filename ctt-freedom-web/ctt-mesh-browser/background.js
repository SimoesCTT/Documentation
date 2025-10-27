/**
 * CTT Mesh Browser Extension - Background Service Worker
 * Handles ctt:// protocol requests and communicates with local mesh daemon
 */

const CTT_DAEMON_HOST = 'http://localhost:8765';
const CTT_PROTOCOL = 'ctt://';

// Extension state
let meshStatus = {
  connected: false,
  nodeCount: 0,
  cacheSize: 0,
  lastCheck: null
};

// Installation handler
chrome.runtime.onInstalled.addListener(async (details) => {
  if (details.reason === 'install') {
    console.log('CTT Mesh Browser installed');
    await checkDaemonStatus();
    
    // Open welcome page
    chrome.tabs.create({
      url: chrome.runtime.getURL('welcome.html')
    });
  }
});

// Check mesh daemon status
async function checkDaemonStatus() {
  try {
    const response = await fetch(`${CTT_DAEMON_HOST}/status`);
    if (response.ok) {
      const data = await response.json();
      meshStatus = {
        connected: true,
        nodeCount: data.nodes || 0,
        cacheSize: data.cache_size || 0,
        lastCheck: Date.now()
      };
      chrome.action.setIcon({ path: 'icons/icon-active.png' });
      return true;
    }
  } catch (error) {
    console.error('Daemon not accessible:', error);
  }
  
  meshStatus.connected = false;
  chrome.action.setIcon({ path: 'icons/icon-inactive.png' });
  return false;
}

// Retrieve content from mesh network
async function retrieveFromMesh(contentHash) {
  try {
    const response = await fetch(`${CTT_DAEMON_HOST}/retrieve/${contentHash}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return {
      success: true,
      content: data.content,
      mimeType: data.mime_type || 'text/html',
      source: data.source || 'unknown', // 'cache' or 'peer'
      hash: contentHash
    };
  } catch (error) {
    console.error('Failed to retrieve from mesh:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Parse CTT URL
function parseCttUrl(url) {
  if (!url.startsWith(CTT_PROTOCOL)) {
    return null;
  }
  
  const hash = url.substring(CTT_PROTOCOL.length).replace(/^\/+/, '');
  
  // Validate hash format (SHA-256 hex = 64 chars)
  if (!/^[a-f0-9]{64}$/i.test(hash)) {
    return { valid: false, error: 'Invalid content hash format' };
  }
  
  return { valid: true, hash: hash.toLowerCase() };
}

// Handle navigation to ctt:// URLs
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  if (details.frameId !== 0) return; // Only handle main frame
  
  const url = details.url;
  if (!url.startsWith(CTT_PROTOCOL)) return;
  
  console.log('Intercepting CTT URL:', url);
  
  const parsed = parseCttUrl(url);
  if (!parsed.valid) {
    chrome.tabs.update(details.tabId, {
      url: chrome.runtime.getURL(`error.html?message=${encodeURIComponent(parsed.error)}`)
    });
    return;
  }
  
  // Check daemon status
  const daemonOnline = await checkDaemonStatus();
  if (!daemonOnline) {
    chrome.tabs.update(details.tabId, {
      url: chrome.runtime.getURL('error.html?message=Mesh%20daemon%20not%20running')
    });
    return;
  }
  
  // Retrieve content from mesh
  const result = await retrieveFromMesh(parsed.hash);
  
  if (result.success) {
    // Store content in session for viewer page
    await chrome.storage.session.set({
      [`content_${parsed.hash}`]: {
        content: result.content,
        mimeType: result.mimeType,
        source: result.source,
        timestamp: Date.now()
      }
    });
    
    // Navigate to viewer page
    chrome.tabs.update(details.tabId, {
      url: chrome.runtime.getURL(`viewer.html?hash=${parsed.hash}`)
    });
  } else {
    chrome.tabs.update(details.tabId, {
      url: chrome.runtime.getURL(`error.html?message=${encodeURIComponent(result.error)}`)
    });
  }
});

// Message handler for popup and content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  (async () => {
    switch (message.type) {
      case 'GET_STATUS':
        await checkDaemonStatus();
        sendResponse(meshStatus);
        break;
        
      case 'RETRIEVE_CONTENT':
        const result = await retrieveFromMesh(message.hash);
        sendResponse(result);
        break;
        
      case 'PARSE_URL':
        const parsed = parseCttUrl(message.url);
        sendResponse(parsed);
        break;
        
      case 'GET_CONTENT':
        const data = await chrome.storage.session.get(`content_${message.hash}`);
        sendResponse(data[`content_${message.hash}`] || null);
        break;
        
      default:
        sendResponse({ error: 'Unknown message type' });
    }
  })();
  
  return true; // Keep channel open for async response
});

// Periodic daemon status check
setInterval(checkDaemonStatus, 30000); // Every 30 seconds

// Initial status check
checkDaemonStatus();

console.log('CTT Mesh Browser extension loaded');
