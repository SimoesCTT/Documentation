#!/bin/bash
# CTT Audio Codec - Complete pipeline
# Convert, compress, and reconstruct audio using resonance encoding

set -e

show_usage() {
    echo "CTT Audio Codec v1.0 - Complete Pipeline"
    echo ""
    echo "Usage:"
    echo "  $0 compress <input> <output.ctta>"
    echo "  $0 decompress <input.ctta> <output>"
    echo ""
    echo "Examples:"
    echo "  $0 compress song.mp3 song.ctta"
    echo "  $0 compress audio.wav audio.ctta"
    echo "  $0 decompress song.ctta reconstructed.wav"
    echo ""
    echo "Supported formats: MP3, WAV, FLAC, OGG, M4A, AAC"
    exit 1
}

if [ $# -lt 3 ]; then
    show_usage
fi

COMMAND=$1
INPUT=$2
OUTPUT=$3

if [ "$COMMAND" == "compress" ]; then
    echo "=== CTT Audio Codec: Compression Pipeline ==="
    echo "Input:  $INPUT"
    echo "Output: $OUTPUT"
    echo ""
    
    # Create temp directory
    TEMP_DIR=$(mktemp -d)
    RAW_FILE="$TEMP_DIR/audio.raw"
    
    echo "[1/3] Converting to raw PCM..."
    # Get audio metadata
    SAMPLE_RATE=$(ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of csv=p=0 "$INPUT")
    CHANNELS=$(ffprobe -v error -select_streams a:0 -show_entries stream=channels -of csv=p=0 "$INPUT")
    DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT" | cut -d. -f1)
    
    echo "  Sample rate: ${SAMPLE_RATE} Hz"
    echo "  Channels: ${CHANNELS}"
    echo "  Duration: ${DURATION}s"
    
    # Convert to raw PCM (16-bit signed little-endian)
    ffmpeg -i "$INPUT" -f s16le -acodec pcm_s16le "$RAW_FILE" -loglevel quiet
    echo "  ✓ Converted to PCM"
    echo ""
    
    echo "[2/3] Compressing with CTT resonance encoding..."
    ./ctt_audio_compress -c "$RAW_FILE" "$OUTPUT" $SAMPLE_RATE $CHANNELS 16
    echo ""
    
    echo "[3/3] Cleaning up..."
    rm -rf "$TEMP_DIR"
    echo "  ✓ Done"
    echo ""
    
    # Show comparison with FLAC
    ORIG_SIZE=$(stat -f%z "$INPUT" 2>/dev/null || stat -c%s "$INPUT")
    CTT_SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT")
    
    # Generate FLAC for comparison
    FLAC_FILE="$TEMP_DIR/compare.flac"
    mkdir -p "$TEMP_DIR"
    ffmpeg -i "$INPUT" "$FLAC_FILE" -loglevel quiet 2>/dev/null || true
    if [ -f "$FLAC_FILE" ]; then
        FLAC_SIZE=$(stat -f%z "$FLAC_FILE" 2>/dev/null || stat -c%s "$FLAC_FILE")
        FLAC_RATIO=$(echo "scale=2; (1 - $FLAC_SIZE / $ORIG_SIZE) * 100" | bc)
        CTT_VS_FLAC=$(echo "scale=2; (1 - $CTT_SIZE / $FLAC_SIZE) * 100" | bc)
        rm -rf "$TEMP_DIR"
        
        echo "=== COMPARISON ==="
        echo "Original:       $ORIG_SIZE bytes ($(echo "scale=2; $ORIG_SIZE/1024/1024" | bc) MB)"
        echo "FLAC:           $FLAC_SIZE bytes (${FLAC_RATIO}% compression)"
        echo "CTT Audio:      $CTT_SIZE bytes"
        echo "CTT vs FLAC:    ${CTT_VS_FLAC}% better"
    else
        CTT_RATIO=$(echo "scale=2; (1 - $CTT_SIZE / $ORIG_SIZE) * 100" | bc)
        echo "=== RESULTS ==="
        echo "Original:       $ORIG_SIZE bytes ($(echo "scale=2; $ORIG_SIZE/1024/1024" | bc) MB)"
        echo "CTT Audio:      $CTT_SIZE bytes"
        echo "Compression:    ${CTT_RATIO}%"
    fi
    echo ""
    
elif [ "$COMMAND" == "decompress" ]; then
    echo "=== CTT Audio Codec: Decompression Pipeline ==="
    echo "Input:  $INPUT"
    echo "Output: $OUTPUT"
    echo ""
    
    # Create temp directory
    TEMP_DIR=$(mktemp -d)
    RAW_FILE="$TEMP_DIR/audio.raw"
    
    echo "[1/3] Decompressing CTT audio..."
    ./ctt_audio_compress -d "$INPUT" "$RAW_FILE"
    
    # Extract metadata from header (would need to parse, for now use defaults)
    SAMPLE_RATE=44100
    CHANNELS=2
    
    echo ""
    echo "[2/3] Converting to output format..."
    # Detect output format from extension
    EXT="${OUTPUT##*.}"
    case "$EXT" in
        wav)
            ffmpeg -f s16le -ar $SAMPLE_RATE -ac $CHANNELS -i "$RAW_FILE" "$OUTPUT" -loglevel quiet
            ;;
        mp3)
            ffmpeg -f s16le -ar $SAMPLE_RATE -ac $CHANNELS -i "$RAW_FILE" -codec:a libmp3lame -qscale:a 2 "$OUTPUT" -loglevel quiet
            ;;
        flac)
            ffmpeg -f s16le -ar $SAMPLE_RATE -ac $CHANNELS -i "$RAW_FILE" "$OUTPUT" -loglevel quiet
            ;;
        *)
            ffmpeg -f s16le -ar $SAMPLE_RATE -ac $CHANNELS -i "$RAW_FILE" "$OUTPUT" -loglevel quiet
            ;;
    esac
    echo "  ✓ Converted to $EXT format"
    echo ""
    
    echo "[3/3] Cleaning up..."
    rm -rf "$TEMP_DIR"
    echo "  ✓ Done"
    echo ""
    
    echo "=== OUTPUT ==="
    echo "Reconstructed audio: $OUTPUT"
    echo ""
    
else
    echo "ERROR: Unknown command: $COMMAND"
    show_usage
fi
