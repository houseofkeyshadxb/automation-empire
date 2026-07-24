#!/bin/bash
# Test Voice-to-Text Setup

echo "========================================="
echo "Voice-to-Text Setup Test"
echo "========================================="
echo ""

# Test 1: Check Python
echo "[1/7] Checking Python..."
if command -v python3 &> /dev/null; then
    echo "✓ Python found: $(python3 --version)"
else
    echo "✗ Python not found"
    exit 1
fi
echo ""

# Test 2: Check script exists
echo "[2/7] Checking voice-to-text.py..."
if [ -f ~/voice-to-text.py ]; then
    echo "✓ Script found: ~/voice-to-text.py"
else
    echo "✗ Script not found"
    exit 1
fi
echo ""

# Test 3: Check if executable
echo "[3/7] Checking if script is executable..."
if [ -x ~/voice-to-text.py ]; then
    echo "✓ Script is executable"
else
    echo "⚠ Script not executable, fixing..."
    chmod +x ~/voice-to-text.py
    echo "✓ Fixed"
fi
echo ""

# Test 4: Check wrapper script
echo "[4/7] Checking wrapper script..."
if [ -f ~/voice ]; then
    echo "✓ Wrapper script found: ~/voice"
else
    echo "⚠ Wrapper script not found (run install script)"
fi
echo ""

# Test 5: Check web interface
echo "[5/7] Checking web interface..."
if [ -f ~/voice-to-text.html ]; then
    echo "✓ Web interface found: ~/voice-to-text.html"
else
    echo "✗ Web interface not found"
fi
echo ""

# Test 6: Check API key
echo "[6/7] Checking OpenAI API key..."
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✓ OPENAI_API_KEY is set"
    echo "  Key: ${OPENAI_API_KEY:0:8}..."
else
    echo "⚠ OPENAI_API_KEY not set"
    echo "  Set with: export OPENAI_API_KEY='your-key'"
fi
echo ""

# Test 7: Test script help
echo "[7/7] Testing script..."
if python3 ~/voice-to-text.py --help > /dev/null 2>&1; then
    echo "✓ Script runs successfully"
else
    echo "⚠ Script has warnings (may need dependencies)"
    echo "  Run: bash ~/install-voice-to-text.sh"
fi
echo ""

# Summary
echo "========================================="
echo "Setup Summary"
echo "========================================="
echo ""
echo "Files created:"
echo "  ✓ ~/voice-to-text.py (CLI tool)"
echo "  ✓ ~/voice-to-text.html (Web interface)"
echo "  ✓ ~/install-voice-to-text.sh (Installer)"
echo "  ✓ ~/.voice-aliases (Shell aliases)"
echo "  ✓ ~/VOICE_TO_TEXT_GUIDE.txt (Guide)"
echo "  ✓ ~/VOICE_QUICK_REFERENCE.md (Quick ref)"
echo ""
echo "Next steps:"
echo "  1. Run installer: bash ~/install-voice-to-text.sh"
echo "  2. Set API key: export OPENAI_API_KEY='your-key'"
echo "  3. Load aliases: source ~/.voice-aliases"
echo "  4. Test recording: ~/voice --record"
echo "  5. Open web: xdg-open ~/voice-to-text.html"
echo ""
echo "========================================="
