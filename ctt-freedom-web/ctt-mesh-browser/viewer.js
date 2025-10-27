/**
 * CTT Mesh Browser - Content Viewer
 */

document.addEventListener('DOMContentLoaded', async () => {
  const params = new URLSearchParams(window.location.search);
  const hash = params.get('hash');
  
  const hashDisplay = document.getElementById('hashDisplay');
  const sourceDisplay = document.getElementById('sourceDisplay');
  const loadingIndicator = document.getElementById('loadingIndicator');
  const contentFrame = document.getElementById('content-frame');
  
  if (!hash) {
    loadingIndicator.innerHTML = '<span style="color: #ff4444;">Error: No content hash provided</span>';
    return;
  }
  
  // Display hash
  hashDisplay.textContent = `ctt://${hash}`;
  hashDisplay.title = `ctt://${hash}`;
  
  try {
    // Retrieve content from session storage
    const response = await chrome.runtime.sendMessage({
      type: 'GET_CONTENT',
      hash: hash
    });
    
    if (!response) {
      throw new Error('Content not found in session');
    }
    
    const { content, mimeType, source } = response;
    
    // Update source display
    sourceDisplay.textContent = source === 'cache' ? '📦 Local Cache' : '🌐 Network Peer';
    sourceDisplay.style.background = source === 'cache' ? 
      'rgba(0, 255, 136, 0.2)' : 
      'rgba(0, 136, 255, 0.2)';
    sourceDisplay.style.borderColor = source === 'cache' ? '#00ff88' : '#0088ff';
    sourceDisplay.style.color = source === 'cache' ? '#00ff88' : '#0088ff';
    
    // Render content based on MIME type
    if (mimeType.startsWith('text/html')) {
      // Render HTML in iframe
      const blob = new Blob([content], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      contentFrame.src = url;
    } else if (mimeType.startsWith('text/')) {
      // Render plain text
      const html = `
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body {
              font-family: monospace;
              padding: 20px;
              background: #1a1a1a;
              color: #e0e0e0;
              white-space: pre-wrap;
              word-wrap: break-word;
            }
          </style>
        </head>
        <body>${escapeHtml(content)}</body>
        </html>
      `;
      const blob = new Blob([html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      contentFrame.src = url;
    } else if (mimeType.startsWith('image/')) {
      // Render image
      const html = `
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body {
              margin: 0;
              display: flex;
              align-items: center;
              justify-content: center;
              min-height: 100vh;
              background: #1a1a1a;
            }
            img {
              max-width: 100%;
              max-height: 100vh;
              object-fit: contain;
            }
          </style>
        </head>
        <body>
          <img src="data:${mimeType};base64,${btoa(content)}" />
        </body>
        </html>
      `;
      const blob = new Blob([html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      contentFrame.src = url;
    } else {
      // Unsupported type - offer download
      const html = `
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body {
              font-family: 'Segoe UI', sans-serif;
              padding: 40px;
              background: #1a1a1a;
              color: #e0e0e0;
              text-align: center;
            }
            h1 {
              color: #00ff88;
            }
            .download-btn {
              display: inline-block;
              margin-top: 20px;
              padding: 12px 24px;
              background: #00ff88;
              color: #000;
              text-decoration: none;
              border-radius: 4px;
              font-weight: bold;
            }
            .download-btn:hover {
              background: #00dd77;
            }
          </style>
        </head>
        <body>
          <h1>Content Retrieved</h1>
          <p>MIME Type: ${mimeType}</p>
          <p>This content type cannot be displayed in the browser.</p>
          <a href="#" class="download-btn" onclick="downloadContent(); return false;">Download Content</a>
          <script>
            function downloadContent() {
              const content = ${JSON.stringify(content)};
              const blob = new Blob([content], { type: '${mimeType}' });
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = 'content_${hash.substring(0, 8)}';
              a.click();
            }
          </script>
        </body>
        </html>
      `;
      const blob = new Blob([html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      contentFrame.src = url;
    }
    
    // Show content, hide loading
    loadingIndicator.style.display = 'none';
    contentFrame.style.display = 'block';
    
  } catch (error) {
    console.error('Failed to load content:', error);
    loadingIndicator.innerHTML = `<span style="color: #ff4444;">Error: ${escapeHtml(error.message)}</span>`;
  }
});

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
