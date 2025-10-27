# Icons Needed

Create PNG icons with the following sizes:
- icon16.png (16x16)
- icon32.png (32x32)
- icon48.png (48x48)
- icon128.png (128x128)
- icon-active.png (48x48) - for when daemon is online
- icon-inactive.png (48x48) - for when daemon is offline

## Design Suggestion

- Color scheme: #00ff88 (green) on dark background
- Symbol: Lightning bolt (⚡) or mesh network nodes
- Style: Modern, tech-focused, glowing effect

## Quick Generation with ImageMagick

```bash
# Install ImageMagick if needed
sudo dnf install ImageMagick

# Generate simple placeholder icons
cd icons/

# Active icon (green)
convert -size 128x128 xc:none -fill "#00ff88" -draw "circle 64,64 64,20" icon128.png
convert icon128.png -resize 48x48 icon48.png
convert icon128.png -resize 32x32 icon32.png
convert icon128.png -resize 16x16 icon16.png
cp icon48.png icon-active.png

# Inactive icon (red)
convert -size 48x48 xc:none -fill "#ff4444" -draw "circle 24,24 24,8" icon-inactive.png
```

Alternatively, use a graphic design tool like GIMP, Inkscape, or online tools.
