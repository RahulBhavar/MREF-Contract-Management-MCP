# Bob_MREF2_MCP Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Verify Installation

The MCP server is already installed and configured! Check that all files are in place:

```bash
cd /Users/rahulbhavar/Documents/BOB/Bob_MREF2_MCP
ls -la
```

You should see:
- `mref_oslc_client.py` - API client
- `mref_oslc_mcp_server.py` - MCP server
- `config.json` - Configuration
- `requirements.txt` - Dependencies
- `README.md` - Full documentation

### Step 2: Test the Connection

Run the API client directly to test your TRIRIGA connection:

```bash
cd /Users/rahulbhavar/Documents/BOB/Bob_MREF2_MCP
python3 mref_oslc_client.py
```

Expected output:
```
Authentication: Authentication successful
================================================================================
Testing OSLC GET Request
================================================================================
GET Result: Successfully retrieved X records
Records retrieved: X
================================================================================
Testing OSLC POST Request
================================================================================
POST Result: Resource created successfully
```

### Step 3: Use Through Bob

The MCP server is now available in Bob! You can use it by asking Bob to:

#### Query Data (GET)
```
"Get all real estate leases from MREF"
"Show me active contracts in TRIRIGA"
"List all buildings in the MREF system"
```

#### Create Resources (POST)
```
"Create a new lease in MREF with the following details: [details]"
"Add a new contract to TRIRIGA for [property name]"
```

## 📋 Common Use Cases

### 1. Query All Leases

Ask Bob:
```
"Use mref_oslc_get to query all leases with endpoint /oslc/spq/cstRELeaseQC and params oslc.select=*"
```

### 2. Query Active Contracts

Ask Bob:
```
"Get active contracts from MREF using endpoint /oslc/spq/cstREContractQC with filter triStatusLI='Active'"
```

### 3. Create a New Lease

Ask Bob:
```
"Create a new lease in MREF using endpoint /oslc/so/cstRELeaseCF with data:
- Name: Office Lease 2026
- City: Chicago
- State: Illinois
- Country: United States
- Start Date: 2026-01-01
- End Date: 2031-12-31
- Status: Active"
```

## 🔧 Configuration

Your configuration is stored in `config.json`:

```json
{
  "mref": {
    "base_url": "https://semas.facilities.semas.apps.srvengmas.cp.fyre.ibm.com/app/tririga",
    "username": "rbhavar",
    "password": "passwordpassword"
  }
}
```

To change credentials, edit this file and restart Bob.

## 📊 Available Endpoints

### Query Endpoints (GET)
- `/oslc/spq/cstRELeaseQC` - Real estate leases
- `/oslc/spq/cstREContractQC` - Real estate contracts
- `/oslc/spq/triBuildingQC` - Buildings
- `/oslc/spq/triLocationQC` - Locations

### Service Object Endpoints (POST)
- `/oslc/so/cstRELeaseCF` - Create/update leases
- `/oslc/so/cstREContractCF` - Create/update contracts
- `/oslc/so/triBuildingCF` - Create/update buildings
- `/oslc/so/triLocationCF` - Create/update locations

## 🎯 OSLC Query Parameters

Use these parameters with GET requests:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `oslc.select` | Fields to return | `*` or `triNameTX,triIdTX` |
| `oslc.where` | Filter criteria | `triStatusLI="Active"` |
| `oslc.pageSize` | Results per page | `50` |
| `oslc.orderBy` | Sort order | `+triNameTX` |

## 🔍 Troubleshooting

### Problem: Authentication fails
**Solution**: Check credentials in `config.json`

### Problem: Cannot find module 'mcp'
**Solution**: 
```bash
python3 -m pip install --user modelcontextprotocol
```

### Problem: Connection timeout
**Solution**: Verify TRIRIGA instance is accessible and URL is correct

## 📝 Example Conversations with Bob

### Example 1: Query Leases
**You**: "Get all leases from MREF"

**Bob**: Uses `mref_oslc_get` tool with:
- endpoint: `/oslc/spq/cstRELeaseQC`
- params: `{"oslc.select": "*"}`

**Result**: List of all leases with full details

### Example 2: Create Lease
**You**: "Create a new 5-year lease in MREF for Chicago office starting January 2026"

**Bob**: Uses `mref_oslc_post` tool with:
- endpoint: `/oslc/so/cstRELeaseCF`
- data: Complete lease details

**Result**: New lease created in TRIRIGA

## 🎓 Next Steps

1. **Explore the API**: Try different OSLC endpoints
2. **Read Full Documentation**: See `README.md` for complete details
3. **Check Logs**: Review `mref_oslc_client.log` for detailed operation logs
4. **Customize**: Modify `config.json` for your specific needs

## 💡 Tips

- **Session Persistence**: The authenticated session is maintained across requests
- **Error Messages**: Check logs for detailed error information
- **Performance**: Use `oslc.select` to limit fields and improve response time
- **Filtering**: Use `oslc.where` to query specific records

## 📞 Need Help?

1. Check `mref_oslc_client.log` for detailed logs
2. Review `README.md` for comprehensive documentation
3. Test connection with `python3 mref_oslc_client.py`

---

**Happy querying! 🎉**

Made with Bob 🤖