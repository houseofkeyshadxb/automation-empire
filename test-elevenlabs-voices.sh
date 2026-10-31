#!/bin/bash

API_KEY="76cfe054b773418cdfabffdb6e91a48b70984e637ffc4c1d036d499c3ef53000"
TEXT="Your wallet belongs to me now, darling. Every pound, every shilling, it's all mine. Don't resist... you know you want to give it to Mistress Keysha."

# Voice IDs and names
declare -A voices=(
    ["pFZP5JQG7iQjIQuC4Bku"]="Lily-Velvety-British"
    ["Xb7hH8MSUJpSbSDYk0k2"]="Alice-British"
    ["EXAVITQu4vr4xnSDxMaL"]="Sarah-Mature"
    ["cgSgspJ2msm6clMCkdW9"]="Jessica-Playful"
)

mkdir -p ~/elevenlabs-voice-samples

for voice_id in "${!voices[@]}"; do
    name="${voices[$voice_id]}"
    echo "Generating: $name..."

    curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/$voice_id" \
        -H "xi-api-key: $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"$TEXT\",
            \"model_id\": \"eleven_multilingual_v2\",
            \"voice_settings\": {
                \"stability\": 0.5,
                \"similarity_boost\": 0.75,
                \"style\": 0.5
            }
        }" \
        --output "~/elevenlabs-voice-samples/${name}.mp3"

    echo "✓ Saved: ${name}.mp3"
done

echo ""
echo "All samples saved to: ~/elevenlabs-voice-samples/"
echo "Copying to Windows Desktop..."
cp ~/elevenlabs-voice-samples/*.mp3 /mnt/c/Users/User/Desktop/
echo "✓ Done! Check your Desktop!"
