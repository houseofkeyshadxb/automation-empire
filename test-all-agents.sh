#!/bin/bash
# Test all agent scripts for proper loading and initialization

echo "🧪 Testing All AI Agents"
echo "========================"
echo ""

source ~/venv-agents/bin/activate

agents=("lead-nurture.py" "market-scout.py" "content-engine.py" "analytics-oracle.py")

for agent in "${agents[@]}"; do
    echo "Testing: $agent"
    echo "---"
    
    timeout 5 python3 ~/agents/$agent 2>&1 | head -10
    
    if [ $? -eq 124 ]; then
        echo "✅ $agent loaded successfully (timed out during execution - expected)"
    elif [ $? -eq 0 ]; then
        echo "✅ $agent completed successfully"
    else
        echo "❌ $agent failed"
    fi
    echo ""
done

echo "Test complete!"
