/**
 * CTT Mesh Browser - Content Script
 * Detects and enhances ctt:// links on web pages
 */

(function() {
  'use strict';
  
  // Add visual indicators to ctt:// links
  function enhanceCttLinks() {
    const links = document.querySelectorAll('a[href^="ctt://"]');
    
    links.forEach(link => {
      if (link.classList.contains('ctt-enhanced')) return;
      
      link.classList.add('ctt-enhanced');
      link.style.borderBottom = '2px solid #00ff88';
      link.style.paddingLeft = '20px';
      link.style.backgroundImage = 'url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSI4IiBjeT0iOCIgcj0iNiIgZmlsbD0iIzAwZmY4OCIvPjwvc3ZnPg==)';
      link.style.backgroundRepeat = 'no-repeat';
      link.style.backgroundPosition = 'left center';
      link.title = `CTT Mesh: ${link.href}`;
    });
  }
  
  // Run on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceCttLinks);
  } else {
    enhanceCttLinks();
  }
  
  // Watch for dynamically added links
  const observer = new MutationObserver(enhanceCttLinks);
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
})();
