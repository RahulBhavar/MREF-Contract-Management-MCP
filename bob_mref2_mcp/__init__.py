"""
Bob_MREF2_MCP - MCP Server for Maximo Real Estate and Facilities Integration

This package provides a comprehensive Model Context Protocol (MCP) server
for integrating IBM Bob with Maximo Real Estate and Facilities (TRIRIGA).

Main Components:
- mref_comprehensive_mcp_server: Main MCP server with 10 comprehensive tools
- mref_oslc_client: OSLC API client for TRIRIGA
- fetch_all_contracts_now: Standalone script for fetching contracts

Usage:
    # As MCP Server
    python -m bob_mref2_mcp.mref_comprehensive_mcp_server
    
    # As CLI tool
    mref-fetch-contracts 100
"""

__version__ = "2.0.0"
__author__ = "IBM"
__license__ = "Apache-2.0"

from .mref_oslc_client import MREFOSLCClient

__all__ = ["MREFOSLCClient", "__version__"]

# Made with Bob
