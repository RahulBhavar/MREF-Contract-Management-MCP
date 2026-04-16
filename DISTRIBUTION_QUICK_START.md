# Bob_MREF2_MCP - Distribution Quick Start

## 🚀 Quick Distribution Guide

This is a simplified guide for quickly distributing the Bob_MREF2_MCP package to others.

---

## Method 1: Share the Wheel File (Easiest) ⭐

### Step 1: Build the Package
```bash
cd Bob_MREF2_MCP
./build_package.sh
```

Or manually:
```bash
pip install build
python -m build
```

### Step 2: Share the File
The build creates: `dist/bob_mref2_mcp-2.0.0-py3-none-any.whl`

**Share this .whl file** via:
- Email
- Shared drive
- Internal file server
- Slack/Teams

### Step 3: Users Install
```bash
pip install bob_mref2_mcp-2.0.0-py3-none-any.whl
```

**That's it!** ✅

---

## Method 2: Share the Entire Directory

### Step 1: Zip the Directory
```bash
cd /Users/rahulbhavar/Documents/BOB
tar -czf Bob_MREF2_MCP.tar.gz Bob_MREF2_MCP/
```

### Step 2: Share the Archive
Share `Bob_MREF2_MCP.tar.gz` with users

### Step 3: Users Install
```bash
# Extract
tar -xzf Bob_MREF2_MCP.tar.gz
cd Bob_MREF2_MCP

# Install
pip install .
```

---

## Method 3: Git Repository (Best for Teams)

### Step 1: Create Repository
```bash
cd Bob_MREF2_MCP
git init
git add .
git commit -m "Initial commit: Bob_MREF2_MCP v2.0.0"
```

### Step 2: Push to Git Server
```bash
# Add remote (use your internal Git server)
git remote add origin https://github.ibm.com/your-org/bob-mref2-mcp.git
git push -u origin main
```

### Step 3: Users Install
```bash
pip install git+https://github.ibm.com/your-org/bob-mref2-mcp.git
```

---

## Post-Installation Setup for Users

### 1. Configure Credentials

Users need to create their config file:

```bash
# Create config directory
mkdir -p ~/.bob-mref2-mcp

# Create config file
cat > ~/.bob-mref2-mcp/config.json << 'EOF'
{
  "mref": {
    "base_url": "https://semas.facilities.semas.apps.srvengmas.cp.fyre.ibm.com",
    "username": "THEIR_USERNAME",
    "password": "THEIR_PASSWORD"
  }
}
EOF

# Edit with their credentials
nano ~/.bob-mref2-mcp/config.json
```

### 2. Register with Bob

Add to `~/.bob/settings/mcp_settings.json`:

```json
{
  "mcpServers": {
    "bob-mref2-mcp": {
      "command": "python3",
      "args": ["-m", "bob_mref2_mcp.mref_comprehensive_mcp_server"],
      "disabled": false
    }
  }
}
```

### 3. Test Installation

```bash
# Test import
python -c "import bob_mref2_mcp; print(bob_mref2_mcp.__version__)"

# Fetch contracts
mref-fetch-contracts 10

# Start MCP server
python -m bob_mref2_mcp.mref_comprehensive_mcp_server
```

---

## Quick Commands Reference

### Build Package
```bash
cd Bob_MREF2_MCP
python -m build
```

### Install Locally
```bash
pip install .
```

### Install from Wheel
```bash
pip install dist/bob_mref2_mcp-2.0.0-py3-none-any.whl
```

### Install from Git
```bash
pip install git+https://github.ibm.com/your-org/bob-mref2-mcp.git
```

### Uninstall
```bash
pip uninstall bob-mref2-mcp
```

### Update
```bash
pip install --upgrade bob-mref2-mcp
```

---

## Package Contents

After installation, users get:

### Command-Line Tools
- `bob-mref2-mcp` - Start MCP server
- `mref-fetch-contracts` - Fetch contracts CLI

### Python Library
```python
from bob_mref2_mcp import MREFOSLCClient

client = MREFOSLCClient(
    base_url="https://your-server.com",
    username="user",
    password="pass"
)
```

### MCP Server
- 10 comprehensive tools for contract management
- Automatic authentication
- Session management

---

## Troubleshooting

### "Module not found"
```bash
pip install bob-mref2-mcp
```

### "Command not found: mref-fetch-contracts"
```bash
# Ensure pip bin directory is in PATH
export PATH="$PATH:$(python -m site --user-base)/bin"
```

### "Config file not found"
```bash
# Create config
mkdir -p ~/.bob-mref2-mcp
cp config.json ~/.bob-mref2-mcp/
```

---

## Distribution Checklist

- [ ] Build package: `python -m build`
- [ ] Test installation: `pip install dist/*.whl`
- [ ] Test import: `python -c "import bob_mref2_mcp"`
- [ ] Test CLI: `mref-fetch-contracts 10`
- [ ] Share wheel file or push to Git
- [ ] Provide config.json template
- [ ] Share documentation (README.md, INSTALLATION_GUIDE.md)

---

## Support

For issues:
1. Check [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
2. Review [README.md](README.md)
3. Contact: rbhavar@ibm.com

---

**Version:** 2.0.0  
**Last Updated:** 2026-03-17