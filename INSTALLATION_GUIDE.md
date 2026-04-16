# MREF Contract Manager - Installation & Distribution Guide

## 📦 Package Distribution Options

This guide covers multiple ways to distribute and install the MREF Contract Manager MCP server for use by others.

## ⚠️ Important: Python Version Requirement

**This MCP server requires Python 3.10 or higher** due to the FastMCP framework dependency.

### Check Your Python Version
```bash
python3 --version
```

### Install Python 3.10+ (if needed)

**macOS (Homebrew):**
```bash
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11
```

---

## Option 1: Install from Source (Local Development)

### For Users on the Same Machine

```bash
# Navigate to the package directory
cd /path/to/mref-contract-mcp

# Verify Python version (must be 3.10+)
python3 --version

# Install dependencies using Python 3.11
/opt/homebrew/bin/python3.11 -m pip install -r requirements.txt
```

### For Users on Different Machines

1. **Copy the entire directory** to the target machine
2. **Verify Python 3.10+** is installed
3. Run the installation command:
```bash
cd mref-contract-mcp
# Use Python 3.11 or higher
/opt/homebrew/bin/python3.11 -m pip install -r requirements.txt
```

---

## Option 2: Create a Distributable Package

### Build Distribution Files

```bash
# Install build tools
pip install build twine

# Navigate to package directory
cd Bob_MREF2_MCP

# Build the package
python -m build

# This creates:
# - dist/bob_mref2_mcp-2.0.0.tar.gz (source distribution)
# - dist/bob_mref2_mcp-2.0.0-py3-none-any.whl (wheel distribution)
```

### Share the Package

**Option A: Share the .whl file**
```bash
# Send the .whl file to users
# Users install with:
pip install bob_mref2_mcp-2.0.0-py3-none-any.whl
```

**Option B: Share the .tar.gz file**
```bash
# Send the .tar.gz file to users
# Users install with:
pip install bob_mref2_mcp-2.0.0.tar.gz
```

---

## Option 3: Publish to PyPI (Public)

### Prerequisites
- PyPI account (https://pypi.org/account/register/)
- API token from PyPI

### Publishing Steps

```bash
# 1. Build the package
python -m build

# 2. Upload to PyPI
python -m twine upload dist/*

# Enter your PyPI credentials when prompted
```

### Users Install From PyPI
```bash
pip install bob-mref2-mcp
```

---

## Option 4: Publish to Private PyPI Server

### For Internal IBM Use

```bash
# Upload to internal PyPI server
twine upload --repository-url https://your-internal-pypi.ibm.com dist/*

# Users install from internal server
pip install bob-mref2-mcp --index-url https://your-internal-pypi.ibm.com
```

---

## Option 5: GitHub/GitLab Repository

### Setup Repository

```bash
# Initialize git repository
cd Bob_MREF2_MCP
git init
git add .
git commit -m "Initial commit: Bob_MREF2_MCP v2.0.0"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/ibm/bob-mref2-mcp.git
git push -u origin main
```

### Users Install From Git

```bash
# Install directly from GitHub
pip install git+https://github.com/ibm/bob-mref2-mcp.git

# Or install specific version/branch
pip install git+https://github.com/ibm/bob-mref2-mcp.git@v2.0.0
```

---

## Option 6: Docker Container

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy package files
COPY . /app/

# Install package
RUN pip install --no-cache-dir .

# Expose MCP server
CMD ["python", "-m", "bob_mref2_mcp.mref_comprehensive_mcp_server"]
```

### Build and Share

```bash
# Build Docker image
docker build -t bob-mref2-mcp:2.0.0 .

# Save image to file
docker save bob-mref2-mcp:2.0.0 -o bob-mref2-mcp-2.0.0.tar

# Share the .tar file
# Users load with:
docker load -i bob-mref2-mcp-2.0.0.tar
docker run -it bob-mref2-mcp:2.0.0
```

---

## Post-Installation Configuration

### 1. Configure Connection

After installation, users need to configure their MREF connection:

```bash
# Create config directory
mkdir -p ~/.bob-mref2-mcp

# Copy and edit config file
cp /path/to/bob_mref2_mcp/config.json ~/.bob-mref2-mcp/config.json

# Edit with their credentials
nano ~/.bob-mref2-mcp/config.json
```

### 2. Register with Bob

Users need to add the MCP server to Bob's settings:

**File:** `~/.bob/settings/mcp_settings.json`

```json
{
  "mcpServers": {
    "bob-mref2-mcp": {
      "command": "python3",
      "args": ["-m", "bob_mref2_mcp.mref_comprehensive_mcp_server"],
      "env": {
        "PYTHONPATH": "/path/to/site-packages"
      },
      "disabled": false
    }
  }
}
```

### 3. Verify Installation

```bash
# Test the installation
python -c "import bob_mref2_mcp; print(bob_mref2_mcp.__version__)"

# Run test suite
python -m pytest tests/

# Fetch contracts
mref-fetch-contracts 10
```

---

## Usage After Installation

### As MCP Server
```bash
# Start the MCP server
python -m bob_mref2_mcp.mref_comprehensive_mcp_server
```

### As CLI Tool
```bash
# Fetch contracts
mref-fetch-contracts 100

# Or use Python directly
python -m bob_mref2_mcp.fetch_all_contracts_now 100
```

### As Python Library
```python
from bob_mref2_mcp import MREFOSLCClient

# Create client
client = MREFOSLCClient(
    base_url="https://your-mref-server.com",
    username="your-username",
    password="your-password"
)

# Authenticate
client.authenticate()

# Fetch contracts
result = client.oslc_get('/oslc/spq/cstRELeaseQC', {
    'oslc.select': '*',
    'oslc.pageSize': '100'
})
```

---

## Recommended Distribution Method

### For Internal IBM Use:

**Best Option:** GitHub/GitLab + Internal PyPI

1. **Host on Internal Git Repository**
   - Version control
   - Easy updates
   - Collaboration

2. **Publish to Internal PyPI**
   - Easy installation with `pip`
   - Dependency management
   - Version control

3. **Provide Documentation**
   - README.md
   - COMPREHENSIVE_TOOLS_GUIDE.md
   - This INSTALLATION_GUIDE.md

### Installation Command for Users:
```bash
# One-line installation
pip install bob-mref2-mcp --index-url https://internal-pypi.ibm.com

# Configure
mkdir -p ~/.bob-mref2-mcp
cp config.json.example ~/.bob-mref2-mcp/config.json
nano ~/.bob-mref2-mcp/config.json

# Test
mref-fetch-contracts 10
```

---

## Package Structure

```
Bob_MREF2_MCP/
├── bob_mref2_mcp/              # Main package
│   ├── __init__.py
│   ├── mref_comprehensive_mcp_server.py
│   ├── mref_oslc_client.py
│   ├── fetch_all_contracts_now.py
│   └── config.json
├── setup.py                    # Package configuration
├── MANIFEST.in                 # Include/exclude files
├── LICENSE                     # Apache 2.0 License
├── README.md                   # Main documentation
├── COMPREHENSIVE_TOOLS_GUIDE.md
├── INSTALLATION_GUIDE.md       # This file
├── requirements.txt            # Dependencies
└── dist/                       # Built distributions (after build)
    ├── bob_mref2_mcp-2.0.0.tar.gz
    └── bob_mref2_mcp-2.0.0-py3-none-any.whl
```

---

## Troubleshooting

### Import Errors
```bash
# Ensure package is installed
pip list | grep bob-mref2-mcp

# Reinstall if needed
pip uninstall bob-mref2-mcp
pip install bob-mref2-mcp
```

### Configuration Issues
```bash
# Check config file location
python -c "import bob_mref2_mcp; print(bob_mref2_mcp.__file__)"

# Verify config.json exists
ls -la ~/.bob-mref2-mcp/config.json
```

### MCP Server Not Found
```bash
# Check Bob's MCP settings
cat ~/.bob/settings/mcp_settings.json

# Verify Python path
which python3
python3 -m bob_mref2_mcp.mref_comprehensive_mcp_server
```

---

## Version Management

### Updating the Package

```bash
# Update version in setup.py
# Update version in bob_mref2_mcp/__init__.py

# Rebuild
python -m build

# Republish
python -m twine upload dist/*
```

### Users Update

```bash
# Update to latest version
pip install --upgrade bob-mref2-mcp

# Or install specific version
pip install bob-mref2-mcp==2.0.0
```

---

## Support

For issues or questions:
- Check documentation in README.md
- Review COMPREHENSIVE_TOOLS_GUIDE.md
- Contact: rbhavar@ibm.com

---

**Version:** 2.0.0  
**Last Updated:** 2026-03-17