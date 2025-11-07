#!/bin/bash
# Sync all deep dive companies to Notion
# Usage: ./scripts/sync_all_to_notion.sh

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYNC_SCRIPT="$SCRIPT_DIR/quick_sync_to_notion.py"

echo "======================================"
echo "  Syncing All Companies to Notion"
echo "======================================"
echo ""

# Check if NOTION_API_KEY is set
if [ -z "$NOTION_API_KEY" ]; then
    echo "⚠️  NOTION_API_KEY not set in environment"
    echo ""
    echo "Checking for config/.env file..."
    ENV_FILE="$SCRIPT_DIR/../config/.env"
    if [ -f "$ENV_FILE" ]; then
        echo "✅ Found config/.env, the script will use it"
    else
        echo ""
        echo "❌ No API key found. Please either:"
        echo "   1. Create config/.env with NOTION_API_KEY=your_key"
        echo "   2. Export NOTION_API_KEY in your shell:"
        echo "      export NOTION_API_KEY='secret_your_key_here'"
        echo ""
        exit 1
    fi
fi

echo ""

# Companies to sync
companies=("livekit.io" "100ms.live" "daily.co")

# Sync each company
for company in "${companies[@]}"; do
    echo ""
    echo "--------------------------------------"
    echo "  Syncing: $company"
    echo "--------------------------------------"
    python "$SYNC_SCRIPT" "$company"

    # Check exit status
    if [ $? -eq 0 ]; then
        echo "✅ Successfully synced $company"
    else
        echo "❌ Failed to sync $company"
        exit 1
    fi

    echo ""
done

echo ""
echo "======================================"
echo "  ✅ All Companies Synced!"
echo "======================================"
echo ""
echo "🔗 View in Notion:"
echo "   https://notion.so/2861bdff7e998000a14edb0bf56a75bf"
echo ""
