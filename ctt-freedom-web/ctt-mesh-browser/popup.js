/**
 * CTT Mesh Browser - Popup Logic
 */

document.addEventListener('DOMContentLoaded', async () => {
  const statusDot = document.getElementById('statusDot');
  const statusText = document.getElementById('statusText');
  const nodeCount = document.getElementById('nodeCount');
  const cacheSize = document.getElementById('cacheSize');
  const hashInput = document.getElementById('hashInput');
  const navigateBtn = document.getElementById('navigateBtn');
  const errorMsg = document.getElementById('errorMsg');
  
  // Get mesh status
  async function updateStatus() {
    try {
      const response = await chrome.runtime.sendMessage({ type: 'GET_STATUS' });
      
      if (response.connected) {
        statusDot.className = 'status-dot online';
        statusText.textContent = 'Online';
        nodeCount.textContent = response.nodeCount;
        cacheSize.textContent = formatBytes(response.cacheSize);
        navigateBtn.disabled = false;
      } else {
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'Offline';
        nodeCount.textContent = '-';
        cacheSize.textContent = '-';
        navigateBtn.disabled = true;
        showError('Mesh daemon not running. Start ctt_mesh_daemon first.');
      }
    } catch (error) {
      console.error('Failed to get status:', error);
      statusDot.className = 'status-dot offline';
      statusText.textContent = 'Error';
      navigateBtn.disabled = true;
    }
  }
  
  // Format bytes to human-readable
  function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }
  
  // Show error message
  function showError(message) {
    errorMsg.textContent = message;
    errorMsg.style.display = 'block';
    setTimeout(() => {
      errorMsg.style.display = 'none';
    }, 5000);
  }
  
  // Navigate to hash
  navigateBtn.addEventListener('click', async () => {
    const hash = hashInput.value.trim().toLowerCase();
    
    // Validate hash format
    if (!/^[a-f0-9]{64}$/.test(hash)) {
      showError('Invalid hash format. Must be 64 hex characters.');
      return;
    }
    
    // Open new tab with ctt:// URL
    try {
      await chrome.tabs.create({
        url: `ctt://${hash}`
      });
      window.close();
    } catch (error) {
      showError('Failed to navigate: ' + error.message);
    }
  });
  
  // Allow Enter key to navigate
  hashInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !navigateBtn.disabled) {
      navigateBtn.click();
    }
  });
  
  // Initial status update
  updateStatus();
  
  // Refresh status every 5 seconds
  setInterval(updateStatus, 5000);
});
