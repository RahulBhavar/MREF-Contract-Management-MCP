#!/bin/bash
# Build and test the Bob_MREF2_MCP package

set -e  # Exit on error

echo "=========================================="
echo "  Bob_MREF2_MCP Package Builder"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Clean previous builds
echo -e "\n${BLUE}Step 1: Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.egg-info bob_mref2_mcp.egg-info
echo -e "${GREEN}✓ Cleaned${NC}"

# Step 2: Install build tools
echo -e "\n${BLUE}Step 2: Installing build tools...${NC}"
pip install --upgrade build twine
echo -e "${GREEN}✓ Build tools installed${NC}"

# Step 3: Build the package
echo -e "\n${BLUE}Step 3: Building package...${NC}"
python -m build
echo -e "${GREEN}✓ Package built${NC}"

# Step 4: List built files
echo -e "\n${BLUE}Step 4: Built files:${NC}"
ls -lh dist/
echo ""

# Step 5: Check package
echo -e "\n${BLUE}Step 5: Checking package...${NC}"
python -m twine check dist/*
echo -e "${GREEN}✓ Package check passed${NC}"

# Step 6: Test installation (optional)
echo -e "\n${BLUE}Step 6: Test installation (optional)${NC}"
read -p "Do you want to test install the package? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Installing package in test mode..."
    pip install --force-reinstall dist/*.whl
    echo -e "${GREEN}✓ Package installed${NC}"
    
    # Test import
    echo "Testing import..."
    python -c "import bob_mref2_mcp; print(f'Version: {bob_mref2_mcp.__version__}')"
    echo -e "${GREEN}✓ Import successful${NC}"
fi

# Step 7: Summary
echo -e "\n=========================================="
echo -e "${GREEN}  Build Complete!${NC}"
echo "=========================================="
echo ""
echo "Distribution files created in dist/:"
echo "  - bob_mref2_mcp-2.0.0.tar.gz (source)"
echo "  - bob_mref2_mcp-2.0.0-py3-none-any.whl (wheel)"
echo ""
echo "Next steps:"
echo "  1. Share the .whl file with users"
echo "  2. Or upload to PyPI: python -m twine upload dist/*"
echo "  3. Or push to Git: git add . && git commit && git push"
echo ""
echo "Users can install with:"
echo "  pip install dist/bob_mref2_mcp-2.0.0-py3-none-any.whl"
echo ""

# Made with Bob
