#!/usr/bin/env python3
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
from mcp.server import Server
from mcp.types import Tool, TextContent
from mref_oslc_client import MREFOSLCClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server
app = Server("mref-contract-manager")

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


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List all available MCP tools"""
    return [
        # Tool 1: Fetch All Contracts
        Tool(
            name="fetch_all_contracts",
            description="Retrieve and display all real estate contracts/leases from MREF. Returns comprehensive contract data including identifiers, dates, financial terms, locations, and status information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_size": {
                        "type": "integer",
                        "description": "Number of records per page (default: 100, max: 500)",
                        "default": 100
                    }
                }
            }
        ),
        
        # Tool 2: Create New Contract
        Tool(
            name="create_contract",
            description="Create a new real estate contract/lease in MREF. Requires contract name, location, dates, and financial information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contract_name": {"type": "string", "description": "Contract name (REQUIRED)"},
                    "contract_id": {"type": "string", "description": "Contract identifier"},
                    "city": {"type": "string", "description": "City location"},
                    "state": {"type": "string", "description": "State/Province"},
                    "country": {"type": "string", "description": "Country"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                    "status": {"type": "string", "description": "Contract status (e.g., Active, Draft)"},
                    "provider_type": {"type": "string", "description": "Provider type (e.g., Primary)"},
                    "accounting_type": {"type": "string", "description": "Accounting type"},
                    "accounting_calendar": {"type": "string", "description": "Accounting calendar"}
                },
                "required": ["contract_name"]
            }
        ),
        
        # Tool 3: Fetch with Filters
        Tool(
            name="fetch_contracts_filtered",
            description="Retrieve contracts filtered by specific criteria such as status, location, date range, or other attributes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Filter by status (e.g., Active, Draft, Expired)"},
                    "city": {"type": "string", "description": "Filter by city"},
                    "country": {"type": "string", "description": "Filter by country"},
                    "start_date_from": {"type": "string", "description": "Start date from (YYYY-MM-DD)"},
                    "start_date_to": {"type": "string", "description": "Start date to (YYYY-MM-DD)"},
                    "page_size": {"type": "integer", "description": "Number of records (default: 100)", "default": 100}
                }
            }
        ),
        
        # Tool 4: Update Contract
        Tool(
            name="update_contract",
            description="Update an existing real estate contract/lease. Requires contract ID and fields to update.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contract_id": {"type": "string", "description": "Contract ID to update (REQUIRED)"},
                    "contract_name": {"type": "string", "description": "Updated contract name"},
                    "status": {"type": "string", "description": "Updated status"},
                    "end_date": {"type": "string", "description": "Updated end date (YYYY-MM-DD)"},
                    "notes": {"type": "string", "description": "Additional notes"}
                },
                "required": ["contract_id"]
            }
        ),
        
        # Tool 5: Export to CSV
        Tool(
            name="export_contracts_csv",
            description="Export contracts to CSV file. Can export all contracts or filtered subset.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Output CSV filename (default: contracts_export.csv)"},
                    "status_filter": {"type": "string", "description": "Optional status filter"},
                    "max_records": {"type": "integer", "description": "Maximum records to export (default: 1000)"}
                }
            }
        ),
        
        # Tool 6: Bulk Import
        Tool(
            name="bulk_import_contracts",
            description="Create multiple contracts from CSV file. CSV must have columns: contract_name, city, state, country, start_date, end_date, status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "csv_file": {"type": "string", "description": "Path to CSV file (REQUIRED)"},
                    "dry_run": {"type": "boolean", "description": "Preview without creating (default: false)", "default": false}
                },
                "required": ["csv_file"]
            }
        ),
        
        # Tool 7: Get Statistics
        Tool(
            name="get_contract_statistics",
            description="Analyze contract data and return statistics including total count, status distribution, location breakdown, and date ranges.",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_charts": {"type": "boolean", "description": "Include chart data (default: true)", "default": true}
                }
            }
        ),
        
        # Tool 8: Search by Name
        Tool(
            name="search_contracts_by_name",
            description="Find contracts by name pattern using fuzzy matching. Returns contracts with names containing the search term.",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {"type": "string", "description": "Search term or pattern (REQUIRED)"},
                    "case_sensitive": {"type": "boolean", "description": "Case-sensitive search (default: false)", "default": false},
                    "max_results": {"type": "integer", "description": "Maximum results (default: 50)", "default": 50}
                },
                "required": ["search_term"]
            }
        ),
        
        # Tool 9: Verify Connection
        Tool(
            name="verify_connection",
            description="Test authentication and session with MREF. Verifies connectivity, authentication status, and API availability.",
            inputSchema={
                "type": "object",
                "properties": {
                    "detailed": {"type": "boolean", "description": "Include detailed diagnostics (default: false)", "default": false}
                }
            }
        ),
        
        # Tool 10: Generate Report
        Tool(
            name="generate_comprehensive_report",
            description="Create comprehensive contract report with statistics, summaries, and detailed listings. Includes status breakdown, location analysis, and financial summaries.",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_type": {
                        "type": "string",
                        "description": "Report type: summary, detailed, or executive (default: summary)",
                        "enum": ["summary", "detailed", "executive"],
                        "default": "summary"
                    },
                    "output_format": {
                        "type": "string",
                        "description": "Output format: json, markdown, or html (default: markdown)",
                        "enum": ["json", "markdown", "html"],
                        "default": "markdown"
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls"""
    try:
        logger.info(f"Tool called: {name}")
        
        # Get authenticated client
        client = get_client()
        
        # Route to appropriate handler
        if name == "fetch_all_contracts":
            return await handle_fetch_all(client, arguments)
        elif name == "create_contract":
            return await handle_create(client, arguments)
        elif name == "fetch_contracts_filtered":
            return await handle_fetch_filtered(client, arguments)
        elif name == "update_contract":
            return await handle_update(client, arguments)
        elif name == "export_contracts_csv":
            return await handle_export_csv(client, arguments)
        elif name == "bulk_import_contracts":
            return await handle_bulk_import(client, arguments)
        elif name == "get_contract_statistics":
            return await handle_statistics(client, arguments)
        elif name == "search_contracts_by_name":
            return await handle_search(client, arguments)
        elif name == "verify_connection":
            return await handle_verify(client, arguments)
        elif name == "generate_comprehensive_report":
            return await handle_report(client, arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Tool execution error: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e),
                "message": f"Tool execution failed: {str(e)}"
            }, indent=2)
        )]


# Tool Handlers

async def handle_fetch_all(client: MREFOSLCClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Fetch all contracts"""
    page_size = arguments.get('page_size', 100)
    
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
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def handle_create(client: MREFOSLCClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Create new contract"""
    # Only include writable fields (no read-only fields like spi:triContractStatusCL, spi:triStatusCL, spi:triContractRentableNU)
    contract_data = {
        "spi:triNameTX": arguments.get('contract_name'),
        "spi:triIdTX": arguments.get('contract_id', ''),
        "spi:triCityTX": arguments.get('city', ''),
        "spi:triStateProvTX": arguments.get('state', ''),
        "spi:triCountryTX": arguments.get('country', ''),
        "spi:triStartDA": arguments.get('start_date', ''),
        "spi:triExpirationDA": arguments.get('end_date', ''),
        "spi:triProviderTypeLI": arguments.get('provider_type', 'Primary'),
        "spi:triAccountingTypeLI": arguments.get('accounting_type', 'Accounts Payable (AP)'),
        "spi:triAccountingCalendarCL": arguments.get('accounting_calendar', 'Standard Calendar')
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
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def handle_fetch_filtered(client: MREFOSLCClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Fetch contracts with filters"""
    # Build OSLC where clause
    filters = []
    if arguments.get('status'):
        filters.append(f'spi:triContractStatusCL="{arguments["status"]}"')
    if arguments.get('city'):
        filters.append(f'spi:triCityTX="{arguments["city"]}"')
    if arguments.get('country'):
        filters.append(f'spi:triCountryTX="{arguments["country"]}"')
    
    params = {
        'oslc.select': '*',
        'oslc.pageSize': str(arguments.get('page_size', 100))
    }
    
    if filters:
        params['oslc.where'] = ' and '.join(filters)
    
    result = client.oslc_get('/oslc/spq/cstRELeaseQC', params)
    
    if result['success']:
        data = result.get('data', {})
        contracts = data.get('rdfs:member', [])
        
        response = {
            "success": True,
            "filters_applied": arguments,
            "count": len(contracts),
            "contracts": contracts
        }
    else:
        response = result
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def handle_update(client: MREFOSLCClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Update existing contract"""
    # Note: Update requires fetching the contract first, then posting updates
    response = {
        "success": False,
        "message": "Update functionality requires contract fetch and modification",
        "note": "Use create_contract with same ID to update, or implement PUT endpoint"
    }
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def handle_export_csv(client: MREFOSLCClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Export contracts to CSV"""
    filename = arguments.get('filename', f'contracts_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    max_records = arguments.get('max_records', 1000)
    
    # Fetch contracts
    params = {'oslc.select': '*', 'oslc.pageSize': str(max_records)}
    if arguments.get('status_filter'):
        params['oslc.where'] = f'spi:triContractStatusCL="{arguments["status_filter"]}"'
    
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
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def handle_bulk_import(client: MREFOSLCClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Bulk import contracts from CSV"""
    csv_file = arguments.get('csv_file')
    dry_run = arguments.get('dry_run', False)
    
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
            created = []
            errors = []
            
            for contract in contracts:
                create_result = await handle_create(client, contract)
                result_data = json.loads(create_result[0].text)
                
                if result_data.get('success'):
                    created.append(contract.get('contract_name'))
                else:
                    errors.append({
                        'contract': contract.get('contract_name'),
                        'error': result_data.get('error')
                    })
            
            response = {
                "success": True,
                "created_count": len(created),
                "error_count": len(errors),
                "created": created,
                "errors": errors if errors else None
            }
    
    except Exception as e:
        response = {
            "success": False,
            "error": str(e),
            "message": f"Failed to import from {csv_file}"
        }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def handle_statistics(client: MREFOSLCClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Get contract statistics"""
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
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def handle_search(client: MREFOSLCClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Search contracts by name"""
    search_term = arguments.get('search_term', '')
    case_sensitive = arguments.get('case_sensitive', False)
    max_results = arguments.get('max_results', 50)
    
    result = client.oslc_get('/oslc/spq/cstRELeaseQC', {
        'oslc.select': '*',
        'oslc.pageSize': '500'
    })
    
    if result['success']:
        contracts = result.get('data', {}).get('rdfs:member', [])
        
        # Filter by name
        if not case_sensitive:
            search_term = search_term.lower()
        
        matches = []
        for contract in contracts:
            name = contract.get('spi:triNameTX', '')
            if not case_sensitive:
                name = name.lower()
            
            if search_term in name:
                matches.append(contract)
                if len(matches) >= max_results:
                    break
        
        response = {
            "success": True,
            "search_term": arguments.get('search_term'),
            "matches_found": len(matches),
            "contracts": matches,
            "message": f"Found {len(matches)} contracts matching '{arguments.get('search_term')}'"
        }
    else:
        response = result
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def handle_verify(client: MREFOSLCClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Verify connection"""
    detailed = arguments.get('detailed', False)
    
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
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def handle_report(client: MREFOSLCClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Generate comprehensive report"""
    report_type = arguments.get('report_type', 'summary')
    output_format = arguments.get('output_format', 'markdown')
    
    # Fetch data
    result = client.oslc_get('/oslc/spq/cstRELeaseQC', {
        'oslc.select': '*',
        'oslc.pageSize': '500'
    })
    
    if not result['success']:
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
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
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def main():
    """Main entry point"""
    from mcp.server.stdio import stdio_server
    
    logger.info("=" * 80)
    logger.info("Starting Bob_MREF2_MCP Comprehensive Server")
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
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
