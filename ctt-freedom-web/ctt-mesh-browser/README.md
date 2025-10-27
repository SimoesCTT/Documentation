# CTT Mesh Browser Extension

Browser extension for accessing the CTT Mesh Network (`ctt://` protocol) - a fully decentralized, peer-to-peer content distribution system based on Convergent Time Theory.

## Features

🔬 **Access Decentralized Content** - Navigate to `ctt://` URLs using SHA-256 content hashes  
🌐 **No DNS Required** - Pure content-addressing, no centralized name servers  
⚡ **Temporal Resonance** - Connects to local mesh daemon using 587kHz/293.5kHz discovery  
🔒 **Cryptographic Verification** - All content verified by hash  
📦 **Local + Network** - Retrieves from local cache or network peers automatically  

## Installation

### Prerequisites

1. **Install CTT Mesh Network daemon:**
   ```bash
   sudo dnf install ctt-mesh-network-1.0-1.fc42.x86_64.rpm
   ```

2. **Start the daemon:**
   ```bash
   ctt_mesh_daemon &
   ```

3. **Verify it's running:**
   ```bash
   curl http://localhost:8765/status
   ```

### Install Extension

#### Firefox
1. Open `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on"
3. Select `manifest.json` from this directory

#### Chrome/Chromium
1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select this directory

## Usage

### Method 1: Extension Popup
1. Click the CTT Mesh icon in your toolbar
2. Enter a 64-character SHA-256 hash
3. Click "Navigate"

### Method 2: Direct URL
Enter in address bar:
```
ctt://a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890
```

### Method 3: Click Links
Any `ctt://` links on web pages will be automatically enhanced and clickable.

## Architecture

```
┌──────────────────────┐
│  Browser Extension   │
│  (ctt:// handler)    │
└──────────┬───────────┘
           │ HTTP API (localhost:8765)
           ↓
┌──────────────────────┐
│   CTT Mesh Daemon    │
│  (Local + P2P node)  │
└──────────┬───────────┘
           │ Temporal Resonance
           ↓
┌──────────────────────┐
│   Mesh Network       │
│   (587kHz/293.5kHz)  │
└──────────────────────┘
```

## Publishing Content

Share files on the network:

```bash
# Publish a file
ctt_mesh_publish -f index.html

# Publish a directory
ctt_mesh_publish -d /path/to/website/

# Returns content hash - share this!
# ctt://abc123...
```

## Development

### File Structure
```
ctt-mesh-browser/
├── manifest.json          # Extension metadata
├── background.js          # Service worker (protocol handling)
├── content.js            # Content script (link enhancement)
├── popup.html/js         # Extension popup UI
├── viewer.html/js        # Content viewer page
├── error.html            # Error page
├── welcome.html          # Welcome/help page
└── icons/                # Extension icons
```

### API Endpoints (Daemon)

The extension communicates with the local daemon via HTTP:

- `GET /status` - Daemon status and network info
- `GET /retrieve/:hash` - Retrieve content by hash
- `GET /publish` - Publish new content

## Security

- **Sandboxed Content**: Retrieved content is rendered in a sandboxed iframe
- **Hash Verification**: All content is verified against its hash
- **Local Daemon**: Only communicates with localhost:8765
- **No Remote Code**: Extension doesn't execute remote code

## Technical Details

- **Protocol**: `ctt://` (content-addressed)
- **Hash**: SHA-256 (64 hex characters)
- **Daemon Port**: `localhost:8765`
- **Discovery**: Temporal resonance frequencies (587kHz/293.5kHz)
- **Network**: Fully decentralized P2P mesh

## Troubleshooting

**Extension icon shows "Offline"**
- Ensure `ctt_mesh_daemon` is running
- Check daemon status: `curl http://localhost:8765/status`

**Content not loading**
- Verify hash format (64 hex characters)
- Check if content exists on network
- Wait for peer discovery (may take a few seconds)

**Links not clickable**
- Extension must be enabled
- Daemon must be running
- Refresh the page

## License

Proprietary - Free for personal use  
Part of the Convergent Time Theory Research Project

Copyright © 2025 A.N.F. Simões

## Links

- **Documentation**: https://github.com/SimoesCTT/Documentation
- **Project**: CTT Mesh Network
- **Theory**: Convergent Time Theory (α = 0.0302)

---

**No DNS. No Servers. No Control.**  
The decentralized internet is here.
