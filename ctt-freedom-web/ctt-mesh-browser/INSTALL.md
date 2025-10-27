# CTT Mesh Browser Extension - Installation Guide

## Quick Start

### 1. Install Prerequisites

```bash
# Install CTT Mesh Network daemon (if not already installed)
sudo dnf install ctt-mesh-network-1.0-1.fc42.x86_64.rpm

# Start the daemon
ctt_mesh_daemon &

# Verify it's running
curl http://localhost:8765/status
```

### 2. Install Browser Extension

#### For Firefox

1. Open Firefox
2. Type `about:debugging` in the address bar
3. Click "This Firefox" in the left sidebar
4. Click "Load Temporary Add-on..."
5. Navigate to `/home/americosimoes/ctt-mesh-browser/`
6. Select `manifest.json`
7. Extension is now loaded!

**Note**: Temporary add-ons are removed when you close Firefox. To make it permanent, you need to sign it through Mozilla.

#### For Chrome/Chromium

1. Open Chrome/Chromium
2. Type `chrome://extensions/` in the address bar
3. Enable "Developer mode" (toggle in top right)
4. Click "Load unpacked"
5. Navigate to `/home/americosimoes/ctt-mesh-browser/`
6. Select the folder
7. Extension is now loaded!

### 3. Test the Extension

1. Click the CTT Mesh icon in your browser toolbar
2. Check that status shows "Online" (green dot)
3. Try navigating to a content hash (if you have one)

## Publishing Your First Content

```bash
# Create a simple HTML file
echo '<h1>Hello CTT Mesh!</h1>' > test.html

# Publish it
ctt_mesh_publish -f test.html

# Copy the returned hash
# Navigate to ctt://<hash> in your browser!
```

## Packaging for Distribution

### Firefox Add-on (.xpi)

```bash
cd /home/americosimoes/ctt-mesh-browser
zip -r ctt-mesh-browser.xpi *
```

Upload to https://addons.mozilla.org for signing.

### Chrome Extension (.crx)

1. Go to `chrome://extensions/`
2. Click "Pack extension"
3. Select the extension directory
4. Chrome will generate a `.crx` file

## Troubleshooting

**Extension not loading**
- Check manifest.json syntax
- Ensure all referenced files exist
- Check browser console for errors (F12)

**Daemon connection fails**
- Verify daemon is running: `ps aux | grep ctt_mesh_daemon`
- Check port 8765 is not blocked: `curl localhost:8765/status`
- Restart daemon if needed

**Icons not displaying**
- Icons should be in `icons/` directory
- Run the icon generation script if missing

## Uninstalling

### Firefox
`about:debugging` → Find extension → Click "Remove"

### Chrome
`chrome://extensions/` → Find extension → Click "Remove"

---

For more information, see README.md or visit:
https://github.com/SimoesCTT/Documentation
