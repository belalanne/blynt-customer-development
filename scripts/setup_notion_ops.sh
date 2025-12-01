#!/bin/bash
# Setup script for token-optimized Notion operations
set -e

echo "=========================================="
echo "  Notion Contact Ops - Setup"
echo "=========================================="
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found"
    echo "   Creating .venv..."
    python3 -m venv .venv
    echo "✅ Created .venv"
fi

# Activate venv and install dependencies
echo "📦 Installing notion-client..."
.venv/bin/pip install -q notion-client==2.2.1

echo "✅ Dependencies installed"
echo ""

# Check for NOTION_API_KEY
if [ ! -f "config/.env" ]; then
    echo "⚠️  config/.env not found"
    echo "   Please create it and add: NOTION_API_KEY=secret_your_key"
elif ! grep -q "NOTION_API_KEY" config/.env; then
    echo "⚠️  NOTION_API_KEY not found in config/.env"
    echo "   Please add: NOTION_API_KEY=secret_your_key"
else
    echo "✅ NOTION_API_KEY found in config/.env"
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Share Notion databases with your integration:"
echo "   • Open People database → ... → Add connections"
echo "   • Open Companies database → ... → Add connections"
echo ""
echo "2. Test the script:"
echo "   .venv/bin/python3 scripts/notion_contact_ops.py check-duplicate \\"
echo "     --linkedin \"https://www.linkedin.com/in/example/\""
echo ""
echo "3. Use /add-contact command (now optimized!)"
echo ""
