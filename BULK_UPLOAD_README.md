# Bulk Upload Leases to MREF - User Guide

## Overview
This guide explains how to bulk upload multiple leases to MREF using the OSLC API with CSV files.

## Files

### 1. CSV Template: `lease_bulk_upload_template.csv`
Contains the required fields for creating leases in MREF.

**CSV Columns:**
- `triIdTX` - Unique lease ID (required)
- `triNameTX` - Lease name/description (required)
- `triProviderTypeLI` - Provider type (default: "Primary")
- `triAccountingTypeLI` - Accounting type (default: "Accounts Payable (AP)")
- `triCityTX` - City location
- `triStateProvTX` - State/Province
- `triCountryTX` - Country
- `triStartDA` - Start date (YYYY-MM-DD format)
- `triExpirationDA` - Expiration date (YYYY-MM-DD format)
- `triContractStatusCL` - Contract status (default: "Active")
- `triAccountingCalendarCL` - Accounting calendar (default: "Standard Calendar")
- `triUserMessageFlagTX` - User message flag (optional, can be empty)

### 2. Bulk Upload Script: `bulk_upload_leases.py`
Python script that reads the CSV and creates leases via OSLC API.

## How to Use

### Step 1: Prepare Your CSV File

1. Open `lease_bulk_upload_template.csv` in Excel or any spreadsheet application
2. Edit the sample data or add new rows with your lease information
3. **Important:** Keep the header row unchanged
4. Ensure all required fields are filled:
   - `triIdTX` (must be unique)
   - `triNameTX`
   - `triStartDA` (format: YYYY-MM-DD)
   - `triExpirationDA` (format: YYYY-MM-DD)
5. Save the file

**Example CSV:**
```csv
triIdTX,triNameTX,triProviderTypeLI,triAccountingTypeLI,triCityTX,triStateProvTX,triCountryTX,triStartDA,triExpirationDA,triContractStatusCL,triAccountingCalendarCL,triUserMessageFlagTX
17032026,Real Estate Lease 17032026,Primary,Accounts Payable (AP),OAKBROOK TERRACE,Illinois,United States,2026-03-17,2031-03-16,Active,Standard Calendar,
17032027,Real Estate Lease 17032027,Primary,Accounts Payable (AP),Chicago,Illinois,United States,2026-04-01,2031-03-31,Active,Standard Calendar,
```

### Step 2: Run the Bulk Upload

**Basic Usage (uses default template file):**
```bash
cd Bob_MREF2_MCP
python3 bulk_upload_leases.py
```

**Custom CSV File:**
```bash
python3 bulk_upload_leases.py /path/to/your/custom_leases.csv
```

### Step 3: Review Results

The script will:
1. Authenticate with MREF using JSESSIONID
2. Process each lease in the CSV file
3. Display progress for each lease
4. Show a summary of successful and failed uploads
5. Save detailed results to a JSON file: `bulk_upload_results_YYYYMMDD_HHMMSS.json`

**Console Output Example:**
```
====================================================================================================
BULK UPLOAD LEASES - OSLC API
====================================================================================================
Timestamp: 2026-03-17 19:44:23
CSV File: lease_bulk_upload_template.csv

[Step 1] Loading OSLC configuration...
✅ Configuration loaded

[Step 2] Loading leases from CSV...
✅ Loaded 5 leases from lease_bulk_upload_template.csv

[Step 3] Initializing MREF OSLC Client...
✅ OSLC Client initialized

[Step 4] Authenticating with MREF...
✅ Authentication successful!

[Step 5] Uploading leases...
====================================================================================================

[1/5] Creating Lease: 17032026
   Name: Real Estate Lease 17032026
   Location: OAKBROOK TERRACE, Illinois
   ✅ SUCCESS - HTTP 201 (6795ms)

[2/5] Creating Lease: 17032027
   Name: Real Estate Lease 17032027
   Location: Chicago, Illinois
   ✅ SUCCESS - HTTP 201 (5234ms)

====================================================================================================
BULK UPLOAD SUMMARY
====================================================================================================
Total Leases: 5
✅ Successful: 5
❌ Failed: 0
Success Rate: 100.0%

✅ Successfully Created Leases:
   - 17032026: Real Estate Lease 17032026 (HTTP 201, 6795ms)
   - 17032027: Real Estate Lease 17032027 (HTTP 201, 5234ms)
   ...
====================================================================================================

📄 Results saved to: bulk_upload_results_20260317_194423.json
```

## Important Notes

### Authentication
- The script uses the credentials from `config.json`
- Authentication is done once at the start using `/p/websignon/signon`
- The JSESSIONID is automatically used for all subsequent lease creation requests

### Rate Limiting
- The script includes a 1-second delay between each lease creation
- This prevents overwhelming the MREF server
- You can modify the delay in the script if needed

### Field Validation
- **Read-only fields** are automatically excluded (e.g., `triStatusCL`, `triContractRentableNU`)
- **Required fields:** triIdTX, triNameTX, triStartDA, triExpirationDA
- **Date format:** Must be YYYY-MM-DD (e.g., 2026-03-17)
- **Unique IDs:** Each triIdTX must be unique across all leases

### Error Handling
- If a lease fails to create, the script continues with the next lease
- All errors are logged in the results JSON file
- Failed leases are listed in the summary with error details

## Troubleshooting

### Common Issues

**1. Authentication Failed**
- Check credentials in `config.json`
- Verify network connectivity to MREF server

**2. Lease Creation Failed - HTTP 400**
- Check for invalid field values
- Ensure dates are in YYYY-MM-DD format
- Verify triIdTX is unique
- Check that required fields are not empty

**3. CSV File Not Found**
- Verify the CSV file path
- Ensure you're running the script from the correct directory

**4. Duplicate Lease ID**
- Each triIdTX must be unique
- Check existing leases in MREF before uploading

## Results File

The JSON results file contains:
```json
{
  "success": [
    {
      "id": "17032026",
      "name": "Real Estate Lease 17032026",
      "status_code": 201,
      "duration_ms": 6795
    }
  ],
  "failed": [
    {
      "id": "17032099",
      "name": "Failed Lease",
      "status_code": 400,
      "error": "Error message here"
    }
  ],
  "total": 5
}
```

## Best Practices

1. **Test First:** Start with a small CSV file (2-3 leases) to test
2. **Backup:** Keep a backup of your CSV file
3. **Unique IDs:** Use a consistent ID naming scheme (e.g., sequential numbers)
4. **Validation:** Validate your CSV data before uploading
5. **Monitor:** Watch the console output during upload
6. **Review:** Check the results JSON file after completion

## Support

For issues or questions:
- Check the log file: `mref_oslc_client.log`
- Review the results JSON file for detailed error messages
- Verify your CSV format matches the template

## Example Workflow

```bash
# 1. Navigate to the directory
cd Bob_MREF2_MCP

# 2. Edit the CSV template with your lease data
# (Use Excel, LibreOffice, or any text editor)

# 3. Run the bulk upload
python3 bulk_upload_leases.py lease_bulk_upload_template.csv

# 4. Review the results
cat bulk_upload_results_*.json

# 5. Check the log for details
tail -f mref_oslc_client.log
```

---

**Created:** 2026-03-17  
**Version:** 1.0  
**Author:** Bob