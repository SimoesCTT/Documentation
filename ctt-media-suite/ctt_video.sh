#!/bin/bash
# CTT Video Codec - Complete pipeline
# Extract, compress, and reconstruct video using resonance encoding

set -e

show_usage() {
    echo "CTT Video Codec v1.0 - Complete Pipeline"
    echo ""
    echo "Usage:"
    echo "  $0 compress <input.mp4> <output.cttv>"
    echo "  $0 decompress <input.cttv> <output.mp4>"
    echo ""
    echo "Examples:"
    echo "  $0 compress myvideo.mp4 myvideo.cttv"
    echo "  $0 decompress myvideo.cttv reconstructed.mp4"
    exit 1
}

if [ $# -lt 3 ]; then
    show_usage
fi

COMMAND=$1
INPUT=$2
OUTPUT=$3

if [ "$COMMAND" == "compress" ]; then
    echo "=== CTT Video Codec: Compression Pipeline ==="
    echo "Input:  $INPUT"
    echo "Output: $OUTPUT"
    echo ""
    
    # Create temp directory
    TEMP_DIR=$(mktemp -d)
    FRAMES_DIR="$TEMP_DIR/frames"
    mkdir -p "$FRAMES_DIR"
    
    echo "[1/4] Extracting video metadata..."
    WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$INPUT")
    HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$INPUT")
    FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$INPUT" | bc -l | xargs printf "%.0f")
    DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT" | cut -d. -f1)
    NUM_FRAMES=$((FPS * DURATION))
    
    echo "  Resolution: ${WIDTH}x${HEIGHT}"
    echo "  FPS: $FPS"
    echo "  Duration: ${DURATION}s"
    echo "  Frames: $NUM_FRAMES"
    echo ""
    
    echo "[2/4] Extracting frames to RGB..."
    ffmpeg -i "$INPUT" -f rawvideo -pix_fmt rgb24 "$FRAMES_DIR/frame_%04d.rgb" -loglevel quiet
    echo "  ✓ Extracted $NUM_FRAMES frames"
    echo ""
    
    echo "[3/4] Compressing with CTT resonance encoding..."
    ./ctt_video_compress -c "$FRAMES_DIR" "$OUTPUT" $WIDTH $HEIGHT $FPS $NUM_FRAMES
    echo ""
    
    echo "[4/4] Cleaning up..."
    rm -rf "$TEMP_DIR"
    echo "  ✓ Done"
    echo ""
    
    # Show comparison
    ORIG_SIZE=$(stat -f%z "$INPUT" 2>/dev/null || stat -c%s "$INPUT")
    COMP_SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT")
    RATIO=$(echo "scale=2; (1 - $COMP_SIZE / $ORIG_SIZE) * 100" | bc)
    
    echo "=== FINAL RESULTS ==="
    echo "Original (MP4):     $ORIG_SIZE bytes ($(echo "scale=2; $ORIG_SIZE/1024/1024" | bc) MB)"
    echo "Compressed (CTTV):  $COMP_SIZE bytes ($(echo "scale=2; $COMP_SIZE/1024/1024" | bc) MB)"
    echo "Compression ratio:  ${RATIO}%"
    echo ""
    
elif [ "$COMMAND" == "decompress" ]; then
    echo "=== CTT Video Codec: Decompression Pipeline ==="
    echo "Input:  $INPUT"
    echo "Output: $OUTPUT"
    echo ""
    
    # Create temp directory
    TEMP_DIR=$(mktemp -d)
    FRAMES_DIR="$TEMP_DIR/frames"
    mkdir -p "$FRAMES_DIR"
    
    echo "[1/3] Decompressing CTT video..."
    ./ctt_video_compress -d "$INPUT" "$FRAMES_DIR"
    echo ""
    
    # Get metadata from first frame
    FIRST_FRAME="$FRAMES_DIR/frame_0000.rgb"
    FRAME_SIZE=$(stat -f%z "$FIRST_FRAME" 2>/dev/null || stat -c%s "$FIRST_FRAME")
    
    # Calculate dimensions (assuming RGB24)
    # Common resolutions - try to detect
    if [ $FRAME_SIZE -eq $((1920*1080*3)) ]; then
        WIDTH=1920
        HEIGHT=1080
    elif [ $FRAME_SIZE -eq $((1280*720*3)) ]; then
        WIDTH=1280
        HEIGHT=720
    elif [ $FRAME_SIZE -eq $((3840*2160*3)) ]; then
        WIDTH=3840
        HEIGHT=2160
    else
        echo "ERROR: Cannot detect resolution from frame size: $FRAME_SIZE"
        exit 1
    fi
    
    echo "[2/3] Reconstructing video..."
    echo "  Resolution: ${WIDTH}x${HEIGHT}"
    ffmpeg -f rawvideo -pix_fmt rgb24 -s ${WIDTH}x${HEIGHT} -i "$FRAMES_DIR/frame_%04d.rgb" \
           -c:v libx264 -preset medium -crf 18 "$OUTPUT" -loglevel quiet
    echo "  ✓ Video reconstructed"
    echo ""
    
    echo "[3/3] Cleaning up..."
    rm -rf "$TEMP_DIR"
    echo "  ✓ Done"
    echo ""
    
    echo "=== OUTPUT ==="
    echo "Reconstructed video: $OUTPUT"
    echo ""
    
else
    echo "ERROR: Unknown command: $COMMAND"
    show_usage
fi
