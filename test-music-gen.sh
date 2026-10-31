#!/bin/bash
# Test Lyrics + Music Generator

echo "🎵 Testing Lyrics + Music Generator..."
echo ""
echo "Sending request to N8N workflow..."
echo ""

curl -X POST http://localhost:5678/webhook/generate-music \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "building an empire from nothing",
    "genre": "motivational hip-hop",
    "mood": "powerful",
    "language": "English"
  }' | jq '.'

echo ""
echo "✅ Request sent!"
echo ""
echo "Check output in: ~/music-generated/"
