# Bob_MREF2_MCP - Comprehensive MCP Server for Maximo Real Estate and Facilities

## 🎯 Overview

Bob_MREF2_MCP is a comprehensive Model Context Protocol (MCP) server that enables IBM Bob to interact with Maximo Real Estate and Facilities (TRIRIGA) for managing real estate contracts and leases. This tool provides 10 powerful capabilities for contract management, data analysis, and reporting.

## ✨ Features

### 10 Comprehensive Tools

1. **📋 Fetch All Contracts** - Retrieve and display all real estate contracts
2. **🆕 Create New Contract** - Create new contracts with full details
3. **🔍 Fetch with Filters** - Get contracts by status, location, or date range
4. **✏️ Update Contract** - Modify existing contract records
5. **📊 Export to CSV** - Export contracts to CSV files
6. **📥 Bulk Import** - Create multiple contracts from CSV
7. **📈 Get Statistics** - Analyze contract data with breakdowns
8. **🔎 Search by Name** - Find contracts using name patterns
9. **✅ Verify Connection** - Test authentication and API access
10. **📋 Generate Report** - Create comprehensive contract reports

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- IBM Bob with MCP support
- Access to Maximo Real Estate and Facilities (TRIRIGA)

### Installation

1. **Install Dependencies**
```bash
cd Bob_MREF2_MCP
pip install -r requirements.txt
```

2. **Configure Connection**

The [`config.json`](config.json) file is already configured with:
```json
{
  "mref": {
    "base_url": "https://semas.facilities.semas.apps.srvengmas.cp.fyre.ibm.com",
    "username": "rbhavar",
    "password": "passwordpassword"
  }
}
```

3. **Verify MCP Registration**

The server is registered in Bob's MCP settings at:
`/Users/rahulbhavar/.bob/settings/mcp_settings.json`

```json
{
  "mcpServers": {
    "bob-mref2-mcp": {
      "command": "python3",
      "args": [
        "/Users/rahulbhavar/Documents/BOB/Bob_MREF2_MCP/mref_comprehensive_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/rahulbhavar/Documents/BOB/Bob_MREF2_MCP"
      },
      "disabled": false
    }
  }
}
```

4. **Restart Bob** to load the MCP server

## 📖 Usage Examples

### Example 1: Get All Contracts
```
Use the fetch_all_contracts tool to retrieve all contracts
```

### Example 2: Create a New Contract
```
Create a new contract with name "Office Lease 2026", city "Chicago", 
state "Illinois", country "United States", start date "2026-01-01", 
end date "2031-12-31", status "Active"
```

### Example 3: Filter Active Contracts
```
Fetch contracts filtered by status "Active" and country "United States"
```

### Example 4: Export to CSV
```
Export all active contracts to CSV file named "active_contracts.csv"
```

### Example 5: Get Statistics
```
Get contract statistics to analyze the data
```

### Example 6: Search Contracts
```
Search contracts by name with search term "Office"
```

### Example 7: Verify Connection
```
Verify connection to test authentication and API access
```

### Example 8: Generate Report
```
Generate comprehensive report with report type "detailed" and output format "markdown"
```

## 📚 Documentation

- **[COMPREHENSIVE_TOOLS_GUIDE.md](COMPREHENSIVE_TOOLS_GUIDE.md)** - Detailed guide for all 10 tools
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details

## 🏗️ Architecture

### Components

1. **[`mref_comprehensive_mcp_server.py`](mref_comprehensive_mcp_server.py)** - Main MCP server with 10 tools
2. **[`mref_oslc_client.py`](mref_oslc_client.py)** - Core OSLC API client
3. **[`config.json`](config.json)** - Configuration file

### Key Technologies

- **MCP (Model Context Protocol)** - Framework for extending Bob's capabilities
- **OSLC (Open Services for Lifecycle Collaboration)** - REST API standard
- **TRIRIGA** - IBM's real estate and facilities management platform
- **Python 3** - Implementation language

## 🔐 Authentication

The server uses POST authentication to TRIRIGA:

**Endpoint:** `/p/websignon/signon`

**Method:** POST

**Payload:**
```json
{
  "userName": "rbhavar",
  "password": "passwordpassword"
}
```

**Session Management:**
- JSESSIONID cookie maintained across requests
- Automatic re-authentication on session expiry
- Persistent session for all tool operations

## 🌐 API Endpoints

### Query Endpoint (GET)
```
GET /oslc/spq/cstRELeaseQC?oslc.select=*&oslc.pageSize=100
```

### Service Object Endpoint (POST)
```
POST /oslc/so/cstRELeaseCF
Content-Type: application/json
```

### Critical Headers
```
X-Requested-With: XMLHttpRequest
Content-Type: application/json
Accept: application/json
```

## 📊 Data Model

### Contract/Lease Fields

- `dcterms:identifier` - Unique identifier
- `spi:triNameTX` - Contract name
- `spi:triIdTX` - Contract ID
- `spi:triCityTX` - City
- `spi:triStateProvTX` - State/Province
- `spi:triCountryTX` - Country
- `spi:triStartDA` - Start date
- `spi:triExpirationDA` - End date
- `spi:triContractStatusCL` - Status (Active, Draft, Expired)
- `spi:triProviderTypeLI` - Provider type
- `spi:triAccountingTypeLI` - Accounting type
- `spi:triAccountingCalendarCL` - Accounting calendar

## 🔧 Troubleshooting

### Connection Issues

1. **Verify credentials** in [`config.json`](config.json)
2. **Check base URL** - Must NOT include `/app/tririga`
3. **Test connection** using `verify_connection` tool
4. **Check logs** in terminal where Bob is running

### Authentication Failures

- Ensure username and password are correct
- Verify network connectivity to TRIRIGA server
- Check if account is active and has proper permissions

### No Data Returned

- Use `fetch_all_contracts` to verify data exists
- Check filter criteria are not too restrictive
- Verify OSLC endpoints are accessible

### Tool Not Available in Bob

1. Restart Bob to reload MCP servers
2. Check MCP settings file is correct
3. Verify Python dependencies are installed
4. Check server logs for errors

## 📝 Development

### Project Structure
```
Bob_MREF2_MCP/
├── mref_comprehensive_mcp_server.py  # Main MCP server (10 tools)
├── mref_oslc_client.py               # OSLC API client
├── config.json                       # Configuration
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── COMPREHENSIVE_TOOLS_GUIDE.md      # Detailed tools guide
├── QUICK_START.md                    # Quick start guide
└── IMPLEMENTATION_SUMMARY.md         # Technical details
```

### Testing

Test the server directly:
```bash
cd Bob_MREF2_MCP
python3 mref_comprehensive_mcp_server.py
```

### Logging

Logs are written to console with format:
```
2026-03-17 17:15:00 - bob-mref2-comprehensive - INFO - Tool called: fetch_all_contracts
```

## 🤝 Contributing

This is an internal IBM tool. For issues or enhancements, contact the development team.

## 📄 License

Internal IBM use only.

## 🔗 Related Projects

- **Bob2_MREF** - Previous MREF integration
- **Bob2_maximo** - Maximo MCP integration
- **MREF_MCP2** - Alternative MREF connector

## 📞 Support

For support or questions:
- Check the [COMPREHENSIVE_TOOLS_GUIDE.md](COMPREHENSIVE_TOOLS_GUIDE.md)
- Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- Contact the development team

---

**Version:** 2.0 - Comprehensive Edition  
**Last Updated:** 2026-03-17  
**Status:** ✅ Production Ready