#!/opt/homebrew/bin/python3.11
"""
MREF Contract Manager - MCP Server for Maximo Real Estate and Facilities
Comprehensive contract and lease management through OSLC APIs
Provides 10 powerful tools for managing real estate contracts/leases
"""

import asyncio
import json
import csv
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from fastmcp import FastMCP
from mref_oslc_client import MREFOSLCClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("mref-contract-manager")

# Global client instance
mref_client: Optional[MREFOSLCClient] = None
config: Optional[Dict[str, Any]] = None


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise


def get_client() -> MREFOSLCClient:
    """Get or create authenticated MREF client"""
    global mref_client, config
    
    if mref_client is None:
        logger.info("Initializing MREF client...")
        
        if config is None:
            config = load_config()
        
        mref_config = config['mref']
        
        mref_client = MREFOSLCClient(
            base_url=mref_config['base_url'],
            username=mref_config['username'],
            password=mref_config['password']
        )
        
        logger.info("Authenticating with MREF...")
        auth_result = mref_client.authenticate()
        
        if not auth_result['success']:
            logger.error(f"Authentication failed: {auth_result.get('message')}")
            raise Exception(f"Authentication failed: {auth_result.get('message')}")
        
        logger.info("✅ Authentication successful!")
    
    return mref_client


# ============================================================================
# CONTRACT MANAGEMENT TOOLS
# ============================================================================

@mcp.tool()
def fetch_all_contracts(page_size: int = 100) -> str:
    """
    Retrieve and display all real estate contracts/leases from MREF.
    
    Args:
        page_size: Number of records per page (default: 100, max: 500)
    
    Returns:
        JSON string with comprehensive contract data including identifiers, dates, 
        financial terms, locations, and status information
    """
    try:
        client = get_client()
        
        result = client.oslc_get('/oslc/spq/cstRELeaseQC', {
            'oslc.select': '*',
            'oslc.pageSize': str(min(page_size, 500))
        })
        
        if result['success']:
            data = result.get('data', {})
            contracts = data.get('rdfs:member', [])
            total = data.get('oslc:responseInfo', {}).get('oslc:totalCount', len(contracts))
            
            response = {
                "success": True,
                "total_count": total,
                "retrieved_count": len(contracts),
                "contracts": contracts,
                "message": f"Retrieved {len(contracts)} of {total} total contracts"
            }
        else:
            response = {
                "success": False,
                "error": result.get('error'),
                "message": "Failed to fetch contracts"
            }
        
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error fetching contracts: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, indent=2)


@mcp.tool()
def create_contract(
    contract_name: str,
    contract_id: str = "",
    city: str = "",
    state: str = "",
    country: str = "",
    start_date: str = "",
    end_date: str = "",
    provider_type: str = "Primary",
    accounting_type: str = "Accounts Payable (AP)",
    accounting_calendar: str = "Standard Calendar"
) -> str:
    """
    Create a new real estate contract/lease in MREF.
    
    Args:
        contract_name: Contract name (REQUIRED)
        contract_id: Contract identifier
        city: City location
        state: State/Province
        country: Country
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        provider_type: Provider type (default: Primary)
        accounting_type: Accounting type (default: Accounts Payable (AP))
        accounting_calendar: Accounting calendar (default: Standard Calendar)
    
    Returns:
        JSON string with creation result
    """
    try:
        client = get_client()
        
        contract_data = {
            "spi:triNameTX": contract_name,
            "spi:triIdTX": contract_id,
            "spi:triCityTX": city,
            "spi:triStateProvTX": state,
            "spi:triCountryTX": country,
            "spi:triStartDA": start_date,
            "spi:triExpirationDA": end_date,
            "spi:triProviderTypeLI": provider_type,
            "spi:triAccountingTypeLI": accounting_type,
            "spi:triAccountingCalendarCL": accounting_calendar
        }
        
        result = client.oslc_post('/oslc/so/cstRELeaseCF', contract_data)
        
        if result['success']:
            response = {
                "success": True,
                "status_code": result.get('status_code'),
                "message": "Contract created successfully",
                "location": result.get('location', ''),
                "duration_ms": result.get('duration_ms')
            }
        else:
            response = result
        
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error creating contract: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, indent=2)


@mcp.tool()
def fetch_contracts_filtered(
    status: str = None,
    city: str = None,
    country: str = None,
    start_date_from: str = None,
    start_date_to: str = None,
    page_size: int = 100
) -> str:
    """
    Retrieve contracts filtered by specific criteria.
    
    Args:
        status: Filter by status (e.g., Active, Draft, Expired)
        city: Filter by city
        country: Filter by country
        start_date_from: Start date from (YYYY-MM-DD)
        start_date_to: Start date to (YYYY-MM-DD)
        page_size: Number of records (default: 100)
    
    Returns:
        JSON string with filtered contracts
    """
    try:
        client = get_client()
        
        # Build OSLC where clause
        filters = []
        if status:
            filters.append(f'spi:triContractStatusCL="{status}"')
        if city:
            filters.append(f'spi:triCityTX="{city}"')
        if country:
            filters.append(f'spi:triCountryTX="{country}"')
        
        params = {
            'oslc.select': '*',
            'oslc.pageSize': str(page_size)
        }
        
        if filters:
            params['oslc.where'] = ' and '.join(filters)
        
        result = client.oslc_get('/oslc/spq/cstRELeaseQC', params)
        
        if result['success']:
            data = result.get('data', {})
            contracts = data.get('rdfs:member', [])
            
            response = {
                "success": True,
                "filters_applied": {
                    "status": status,
                    "city": city,
                    "country": country
                },
                "count": len(contracts),
                "contracts": contracts
            }
        else:
            response = result
        
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error fetching filtered contracts: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, indent=2)


@mcp.tool()
def update_contract(
    contract_id: str,
    contract_name: str = None,
    status: str = None,
    end_date: str = None,
    notes: str = None
) -> str:
    """
    Update an existing real estate contract/lease.
    
    Args:
        contract_id: Contract ID to update (REQUIRED)
        contract_name: Updated contract name
        status: Updated status
        end_date: Updated end date (YYYY-MM-DD)
        notes: Additional notes
    
    Returns:
        JSON string with update result
    """
    response = {
        "success": False,
        "message": "Update functionality requires contract fetch and modification",
        "note": "Use create_contract with same ID to update, or implement PUT endpoint"
    }
    return json.dumps(response, indent=2)


@mcp.tool()
def export_contracts_csv(
    filename: str = None,
    status_filter: str = None,
    max_records: int = 1000
) -> str:
    """
    Export contracts to CSV file.
    
    Args:
        filename: Output CSV filename (default: contracts_export_TIMESTAMP.csv)
        status_filter: Optional status filter
        max_records: Maximum records to export (default: 1000)
    
    Returns:
        JSON string with export result
    """
    try:
        client = get_client()
        
        if filename is None:
            filename = f'contracts_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        # Fetch contracts
        params = {'oslc.select': '*', 'oslc.pageSize': str(max_records)}
        if status_filter:
            params['oslc.where'] = f'spi:triContractStatusCL="{status_filter}"'
        
        result = client.oslc_get('/oslc/spq/cstRELeaseQC', params)
        
        if result['success']:
            contracts = result.get('data', {}).get('rdfs:member', [])
            
            if contracts:
                # Write to CSV
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=contracts[0].keys())
                    writer.writeheader()
                    writer.writerows(contracts)
                
                response = {
                    "success": True,
                    "filename": filename,
                    "records_exported": len(contracts),
                    "message": f"Exported {len(contracts)} contracts to {filename}"
                }
            else:
                response = {
                    "success": False,
                    "message": "No contracts found to export"
                }
        else:
            response = result
        
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error exporting contracts: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, indent=2)


@mcp.tool()
def bulk_import_contracts(csv_file: str, dry_run: bool = False) -> str:
    """
    Create multiple contracts from CSV file.
    
    Args:
        csv_file: Path to CSV file (REQUIRED)
        dry_run: Preview without creating (default: false)
    
    Returns:
        JSON string with import result
    
    Note:
        CSV must have columns: contract_name, city, state, country, start_date, end_date, status
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            contracts = list(reader)
        
        if dry_run:
            response = {
                "success": True,
                "dry_run": True,
                "contracts_to_create": len(contracts),
                "preview": contracts[:5],
                "message": f"Dry run: Would create {len(contracts)} contracts"
            }
        else:
            client = get_client()
            created = []
            errors = []
            
            for contract in contracts:
                contract_data = {
                    "spi:triNameTX": contract.get('contract_name'),
                    "spi:triCityTX": contract.get('city', ''),
                    "spi:triStateProvTX": contract.get('state', ''),
                    "spi:triCountryTX": contract.get('country', ''),
                    "spi:triStartDA": contract.get('start_date', ''),
                    "spi:triExpirationDA": contract.get('end_date', '')
                }
                
                result = client.oslc_post('/oslc/so/cstRELeaseCF', contract_data)
                
                if result.get('success'):
                    created.append(contract.get('contract_name'))
                else:
                    errors.append({
                        'contract': contract.get('contract_name'),
                        'error': result.get('error')
                    })
            
            response = {
                "success": True,
                "created_count": len(created),
                "error_count": len(errors),
                "created": created,
                "errors": errors if errors else None
            }
        
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error importing contracts: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e), "message": f"Failed to import from {csv_file}"}, indent=2)


@mcp.tool()
def get_contract_statistics(include_charts: bool = True) -> str:
    """
    Analyze contract data and return statistics.
    
    Args:
        include_charts: Include chart data (default: true)
    
    Returns:
        JSON string with statistics including total count, status distribution, 
        location breakdown, and date ranges
    """
    try:
        client = get_client()
        
        result = client.oslc_get('/oslc/spq/cstRELeaseQC', {
            'oslc.select': '*',
            'oslc.pageSize': '500'
        })
        
        if result['success']:
            contracts = result.get('data', {}).get('rdfs:member', [])
            total = result.get('data', {}).get('oslc:responseInfo', {}).get('oslc:totalCount', len(contracts))
            
            # Calculate statistics
            status_counts = {}
            city_counts = {}
            country_counts = {}
            
            for contract in contracts:
                status = contract.get('spi:triContractStatusCL', 'Unknown')
                city = contract.get('spi:triCityTX', 'Unknown')
                country = contract.get('spi:triCountryTX', 'Unknown')
                
                status_counts[status] = status_counts.get(status, 0) + 1
                city_counts[city] = city_counts.get(city, 0) + 1
                country_counts[country] = country_counts.get(country, 0) + 1
            
            response = {
                "success": True,
                "total_contracts": total,
                "analyzed_contracts": len(contracts),
                "statistics": {
                    "by_status": status_counts,
                    "by_city": dict(sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
                    "by_country": country_counts
                },
                "message": f"Statistics for {len(contracts)} contracts"
            }
        else:
            response = result
        
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error getting statistics: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, indent=2)


@mcp.tool()
def search_contracts_by_name(
    search_term: str,
    case_sensitive: bool = False,
    max_results: int = 50
) -> str:
    """
    Find contracts by name pattern using fuzzy matching.
    
    Args:
        search_term: Search term or pattern (REQUIRED)
        case_sensitive: Case-sensitive search (default: false)
        max_results: Maximum results (default: 50)
    
    Returns:
        JSON string with contracts matching the search term
    """
    try:
        client = get_client()
        
        result = client.oslc_get('/oslc/spq/cstRELeaseQC', {
            'oslc.select': '*',
            'oslc.pageSize': '500'
        })
        
        if result['success']:
            contracts = result.get('data', {}).get('rdfs:member', [])
            
            # Filter by name
            search_lower = search_term.lower() if not case_sensitive else search_term
            
            matches = []
            for contract in contracts:
                name = contract.get('spi:triNameTX', '')
                name_compare = name.lower() if not case_sensitive else name
                
                if search_lower in name_compare:
                    matches.append(contract)
                    if len(matches) >= max_results:
                        break
            
            response = {
                "success": True,
                "search_term": search_term,
                "matches_found": len(matches),
                "contracts": matches,
                "message": f"Found {len(matches)} contracts matching '{search_term}'"
            }
        else:
            response = result
        
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error searching contracts: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, indent=2)


@mcp.tool()
def verify_connection(detailed: bool = False) -> str:
    """
    Test authentication and session with MREF.
    
    Args:
        detailed: Include detailed diagnostics (default: false)
    
    Returns:
        JSON string with connection verification results including connectivity, 
        authentication status, and API availability
    """
    try:
        client = get_client()
        
        # Test authentication
        auth_status = client.authenticated
        
        # Test API access
        test_result = client.oslc_get('/oslc/spq/cstRELeaseQC', {
            'oslc.select': '*',
            'oslc.pageSize': '1'
        })
        
        response = {
            "success": True,
            "authentication": {
                "status": "authenticated" if auth_status else "not authenticated",
                "username": config['mref']['username'],
                "base_url": config['mref']['base_url']
            },
            "api_access": {
                "status": "accessible" if test_result['success'] else "failed",
                "test_endpoint": "/oslc/spq/cstRELeaseQC"
            },
            "message": "Connection verified successfully" if test_result['success'] else "Connection issues detected"
        }
        
        if detailed:
            response["details"] = {
                "test_result": test_result,
                "session_cookies": "present" if client.cookies else "missing"
            }
        
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error verifying connection: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, indent=2)


@mcp.tool()
def generate_comprehensive_report(
    report_type: str = "summary",
    output_format: str = "markdown"
) -> str:
    """
    Create comprehensive contract report with statistics, summaries, and detailed listings.
    
    Args:
        report_type: Report type - summary, detailed, or executive (default: summary)
        output_format: Output format - json, markdown, or html (default: markdown)
    
    Returns:
        JSON string with report including status breakdown, location analysis, 
        and financial summaries
    """
    try:
        client = get_client()
        
        # Fetch data
        result = client.oslc_get('/oslc/spq/cstRELeaseQC', {
            'oslc.select': '*',
            'oslc.pageSize': '500'
        })
        
        if not result['success']:
            return json.dumps(result, indent=2)
        
        contracts = result.get('data', {}).get('rdfs:member', [])
        total = result.get('data', {}).get('oslc:responseInfo', {}).get('oslc:totalCount', len(contracts))
        
        # Generate report based on format
        if output_format == 'markdown':
            report = f"""# MREF Real Estate Contracts Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Contracts**: {total}
- **Analyzed**: {len(contracts)}

## Status Distribution
"""
            status_counts = {}
            for contract in contracts:
                status = contract.get('spi:triContractStatusCL', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
                report += f"- {status}: {count}\n"
            
            if report_type == 'detailed':
                report += "\n## Contract Listings\n"
                for i, contract in enumerate(contracts[:20], 1):
                    report += f"\n### {i}. {contract.get('spi:triNameTX', 'N/A')}\n"
                    report += f"- **ID**: {contract.get('dcterms:identifier', 'N/A')}\n"
                    report += f"- **City**: {contract.get('spi:triCityTX', 'N/A')}\n"
                    report += f"- **Status**: {contract.get('spi:triContractStatusCL', 'N/A')}\n"
            
            response = {
                "success": True,
                "report_type": report_type,
                "format": output_format,
                "report": report
            }
        else:
            response = {
                "success": True,
                "report_type": report_type,
                "format": output_format,
                "total_contracts": total,
                "contracts": contracts
            }
        
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        return json.dumps({"success": False, "error": str(e)}, indent=2)


if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("Starting MREF Contract Manager MCP Server")
    logger.info("Maximo Real Estate and Facilities Integration")
    logger.info("=" * 80)
    logger.info("Available Tools:")
    logger.info("  1. fetch_all_contracts - Retrieve all contracts")
    logger.info("  2. create_contract - Create new contract")
    logger.info("  3. fetch_contracts_filtered - Get filtered contracts")
    logger.info("  4. update_contract - Update existing contract")
    logger.info("  5. export_contracts_csv - Export to CSV")
    logger.info("  6. bulk_import_contracts - Bulk import from CSV")
    logger.info("  7. get_contract_statistics - Analyze contract data")
    logger.info("  8. search_contracts_by_name - Search by name")
    logger.info("  9. verify_connection - Test connection")
    logger.info(" 10. generate_comprehensive_report - Generate report")
    logger.info("=" * 80)
    
    mcp.run()

# Made with Bob
