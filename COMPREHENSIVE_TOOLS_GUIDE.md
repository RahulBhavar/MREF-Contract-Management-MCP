# Bob_MREF2_MCP - Comprehensive Tools Guide

## Overview

Bob_MREF2_MCP provides 10 comprehensive tools for managing real estate contracts/leases in Maximo Real Estate and Facilities (TRIRIGA). This guide details each tool's functionality, parameters, and usage examples.

---

## 🔧 Tool 1: Fetch All Contracts

**Tool Name:** `fetch_all_contracts`

**Description:** Retrieve and display all real estate contracts/leases from MREF. Returns comprehensive contract data including identifiers, dates, financial terms, locations, and status information.

**Parameters:**
- `page_size` (optional): Number of records per page (default: 100, max: 500)

**Usage Example:**
```
Use the fetch_all_contracts tool to retrieve all contracts with page size 200
```

**Response Structure:**
```json
{
  "success": true,
  "total_count": 310,
  "retrieved_count": 200,
  "contracts": [...],
  "message": "Retrieved 200 of 310 total contracts"
}
```

---

## 🆕 Tool 2: Create New Contract

**Tool Name:** `create_contract`

**Description:** Create a new real estate contract/lease in MREF. Requires contract name, location, dates, and financial information.

**Parameters:**
- `contract_name` (required): Contract name
- `contract_id` (optional): Contract identifier
- `city` (optional): City location
- `state` (optional): State/Province
- `country` (optional): Country
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)
- `status` (optional): Contract status (e.g., Active, Draft)
- `provider_type` (optional): Provider type (e.g., Primary)
- `accounting_type` (optional): Accounting type
- `accounting_calendar` (optional): Accounting calendar

**Usage Example:**
```
Create a new contract with name "Office Lease 2026", city "Chicago", state "Illinois", country "United States", start date "2026-01-01", end date "2031-12-31", status "Active"
```

**Response Structure:**
```json
{
  "success": true,
  "contract_id": "...",
  "message": "Contract created successfully"
}
```

---

## 🔍 Tool 3: Fetch with Filters

**Tool Name:** `fetch_contracts_filtered`

**Description:** Retrieve contracts filtered by specific criteria such as status, location, date range, or other attributes.

**Parameters:**
- `status` (optional): Filter by status (e.g., Active, Draft, Expired)
- `city` (optional): Filter by city
- `country` (optional): Filter by country
- `start_date_from` (optional): Start date from (YYYY-MM-DD)
- `start_date_to` (optional): Start date to (YYYY-MM-DD)
- `page_size` (optional): Number of records (default: 100)

**Usage Example:**
```
Fetch contracts filtered by status "Active" and country "United States"
```

**Response Structure:**
```json
{
  "success": true,
  "filters_applied": {
    "status": "Active",
    "country": "United States"
  },
  "count": 45,
  "contracts": [...]
}
```

---

## ✏️ Tool 4: Update Contract

**Tool Name:** `update_contract`

**Description:** Update an existing real estate contract/lease. Requires contract ID and fields to update.

**Parameters:**
- `contract_id` (required): Contract ID to update
- `contract_name` (optional): Updated contract name
- `status` (optional): Updated status
- `end_date` (optional): Updated end date (YYYY-MM-DD)
- `notes` (optional): Additional notes

**Usage Example:**
```
Update contract with ID "GPNA-US-RE-OP-001" to set status "Expired" and end date "2026-12-31"
```

**Note:** Update functionality requires fetching the contract first, then posting updates. Current implementation provides guidance for this workflow.

---

## 📊 Tool 5: Export to CSV

**Tool Name:** `export_contracts_csv`

**Description:** Export contracts to CSV file. Can export all contracts or filtered subset.

**Parameters:**
- `filename` (optional): Output CSV filename (default: contracts_export_YYYYMMDD_HHMMSS.csv)
- `status_filter` (optional): Optional status filter
- `max_records` (optional): Maximum records to export (default: 1000)

**Usage Example:**
```
Export all active contracts to CSV file named "active_contracts.csv" with status filter "Active"
```

**Response Structure:**
```json
{
  "success": true,
  "filename": "active_contracts.csv",
  "records_exported": 150,
  "message": "Exported 150 contracts to active_contracts.csv"
}
```

---

## 📥 Tool 6: Bulk Import

**Tool Name:** `bulk_import_contracts`

**Description:** Create multiple contracts from CSV file. CSV must have columns: contract_name, city, state, country, start_date, end_date, status.

**Parameters:**
- `csv_file` (required): Path to CSV file
- `dry_run` (optional): Preview without creating (default: false)

**CSV Format:**
```csv
contract_name,city,state,country,start_date,end_date,status
"Office Lease A","New York","New York","United States","2026-01-01","2031-12-31","Active"
"Warehouse Lease B","Los Angeles","California","United States","2026-03-01","2029-02-28","Active"
```

**Usage Example:**
```
Bulk import contracts from CSV file "new_contracts.csv" with dry run true
```

**Response Structure:**
```json
{
  "success": true,
  "created_count": 25,
  "error_count": 2,
  "created": ["Office Lease A", "Warehouse Lease B", ...],
  "errors": [...]
}
```

---

## 📈 Tool 7: Get Statistics

**Tool Name:** `get_contract_statistics`

**Description:** Analyze contract data and return statistics including total count, status distribution, location breakdown, and date ranges.

**Parameters:**
- `include_charts` (optional): Include chart data (default: true)

**Usage Example:**
```
Get contract statistics with charts included
```

**Response Structure:**
```json
{
  "success": true,
  "total_contracts": 310,
  "analyzed_contracts": 310,
  "statistics": {
    "by_status": {
      "Active": 150,
      "Draft": 50,
      "Expired": 110
    },
    "by_city": {
      "New York": 45,
      "Chicago": 38,
      "Los Angeles": 32,
      ...
    },
    "by_country": {
      "United States": 280,
      "Canada": 20,
      "Mexico": 10
    }
  },
  "message": "Statistics for 310 contracts"
}
```

---

## 🔎 Tool 8: Search by Name

**Tool Name:** `search_contracts_by_name`

**Description:** Find contracts by name pattern using fuzzy matching. Returns contracts with names containing the search term.

**Parameters:**
- `search_term` (required): Search term or pattern
- `case_sensitive` (optional): Case-sensitive search (default: false)
- `max_results` (optional): Maximum results (default: 50)

**Usage Example:**
```
Search contracts by name with search term "Office" case sensitive false and max results 20
```

**Response Structure:**
```json
{
  "success": true,
  "search_term": "Office",
  "matches_found": 15,
  "contracts": [...],
  "message": "Found 15 contracts matching 'Office'"
}
```

---

## ✅ Tool 9: Verify Connection

**Tool Name:** `verify_connection`

**Description:** Test authentication and session with MREF. Verifies connectivity, authentication status, and API availability.

**Parameters:**
- `detailed` (optional): Include detailed diagnostics (default: false)

**Usage Example:**
```
Verify connection with detailed diagnostics
```

**Response Structure:**
```json
{
  "success": true,
  "authentication": {
    "status": "authenticated",
    "username": "rbhavar",
    "base_url": "https://semas.facilities.semas.apps.srvengmas.cp.fyre.ibm.com"
  },
  "api_access": {
    "status": "accessible",
    "test_endpoint": "/oslc/spq/cstRELeaseQC"
  },
  "message": "Connection verified successfully"
}
```

---

## 📋 Tool 10: Generate Report

**Tool Name:** `generate_comprehensive_report`

**Description:** Create comprehensive contract report with statistics, summaries, and detailed listings. Includes status breakdown, location analysis, and financial summaries.

**Parameters:**
- `report_type` (optional): Report type: summary, detailed, or executive (default: summary)
- `output_format` (optional): Output format: json, markdown, or html (default: markdown)

**Usage Example:**
```
Generate comprehensive report with report type "detailed" and output format "markdown"
```

**Response Structure (Markdown):**
```markdown
# MREF Real Estate Contracts Report
Generated: 2026-03-17 17:15:00

## Summary
- **Total Contracts**: 310
- **Analyzed**: 310

## Status Distribution
- Active: 150
- Draft: 50
- Expired: 110

## Contract Listings
### 1. Office Lease Downtown
- **ID**: GPNA-US-RE-OP-001
- **City**: New York
- **Status**: Active
...
```

---

## 🚀 Quick Start Examples

### Example 1: Get Overview of All Contracts
```
Use fetch_all_contracts to get the first 100 contracts
```

### Example 2: Find Active Contracts in Chicago
```
Use fetch_contracts_filtered with status "Active" and city "Chicago"
```

### Example 3: Create a New Lease
```
Use create_contract with name "New Office Lease 2026", city "Boston", state "Massachusetts", country "United States", start date "2026-04-01", end date "2031-03-31", status "Draft"
```

### Example 4: Export All Contracts
```
Use export_contracts_csv with filename "all_contracts_backup.csv" and max records 500
```

### Example 5: Get Contract Analytics
```
Use get_contract_statistics to analyze all contract data
```

### Example 6: Search for Specific Contracts
```
Use search_contracts_by_name with search term "Warehouse" to find all warehouse leases
```

### Example 7: Verify System Connection
```
Use verify_connection to test authentication and API access
```

### Example 8: Generate Executive Report
```
Use generate_comprehensive_report with report type "executive" and output format "markdown"
```

---

## 🔐 Authentication

All tools automatically handle authentication using credentials from [`config.json`](config.json):
- Base URL: `https://semas.facilities.semas.apps.srvengmas.cp.fyre.ibm.com`
- Username: `rbhavar`
- Password: `passwordpassword`

Session cookies are maintained across all tool calls for efficient API access.

---

## 📝 Notes

1. **Contract vs Lease**: In TRIRIGA/MREF, "Real Estate Contracts" and "Leases" are often used interchangeably. These tools work with the `cstRELeaseCF` business object.

2. **OSLC Endpoints**: 
   - Query: `/oslc/spq/cstRELeaseQC` (GET)
   - Service Object: `/oslc/so/cstRELeaseCF` (POST)

3. **Pagination**: Large datasets are paginated. Use `page_size` parameter to control batch size.

4. **Error Handling**: All tools return structured JSON responses with `success` boolean and descriptive error messages.

5. **Session Management**: Authentication is performed once and session is maintained for all subsequent operations.

---

## 🆘 Troubleshooting

### Connection Issues
```
Use verify_connection with detailed true to diagnose connection problems
```

### Authentication Failures
- Check credentials in [`config.json`](config.json)
- Verify base URL is correct (no `/app/tririga` suffix)
- Ensure `X-Requested-With: XMLHttpRequest` header is present

### No Data Returned
- Verify filters are not too restrictive
- Check if contracts exist in the system
- Use `fetch_all_contracts` first to confirm data availability

---

## 📚 Additional Resources

- [README.md](README.md) - Project overview
- [QUICK_START.md](QUICK_START.md) - Quick start guide
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical implementation details
- [mref_oslc_client.py](mref_oslc_client.py) - Core API client
- [mref_comprehensive_mcp_server.py](mref_comprehensive_mcp_server.py) - MCP server implementation

---

**Last Updated:** 2026-03-17  
**Version:** 2.0 - Comprehensive Edition