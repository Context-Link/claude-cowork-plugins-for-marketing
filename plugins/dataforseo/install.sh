#!/bin/bash
# DataForSEO Skill Installer for Claude Code

set -e

echo "Installing DataForSEO Skill for Claude Code..."

# Determine script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create skills directories if they don't exist
mkdir -p ~/.agents/skills
mkdir -p ~/.claude/skills

# Copy skill files
echo "Copying skill files..."
cp -r "$SCRIPT_DIR/dataforseo" ~/.agents/skills/

# Create symlink
echo "Creating symlink..."
ln -sf ../../.agents/skills/dataforseo ~/.claude/skills/dataforseo

# Verify installation
if [ -d ~/.agents/skills/dataforseo ] && [ -L ~/.claude/skills/dataforseo ]; then
    echo ""
    echo "✓ Installation successful!"
    echo ""
    echo "Next steps:"
    echo "1. Restart Claude Code"
    echo "2. Set up your DataForSEO API credentials (see README.md)"
    echo ""
    echo "Get your API credentials at: https://app.dataforseo.com/"
else
    echo "✗ Installation failed. Please check permissions and try again."
    exit 1
fi
