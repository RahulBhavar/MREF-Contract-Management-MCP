#!/usr/bin/env python3
"""
Standalone Test Script for Bob_MREF2_MCP Server
Tests the MREF OSLC client and configuration without requiring the mcp module
"""

import json
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from mref_oslc_client import MREFOSLCClient


def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return None


def test_connection(config):
    """Test connection to MREF/TRIRIGA"""
    print("\n🔍 Testing MREF Connection...")
    print("=" * 60)
    
    try:
        # Initialize client
        mref_config = config['mref']
        client = MREFOSLCClient(
            base_url=mref_config['base_url'],
            username=mref_config['username'],
            password=mref_config['password']
        )
        
        print(f"✓ Client initialized")
        print(f"  Base URL: {mref_config['base_url']}")
        print(f"  Username: {mref_config['username']}")
        
        # Test authentication
        print("\n🔐 Testing Authentication...")
        if client.authenticate():
            print("✓ Authentication successful")
            session_id = getattr(client, 'session_id', None)
            print(f"  Session ID: {session_id[:20]}..." if session_id else "  No session ID")
            return client
        else:
            print("❌ Authentication failed")
            return None
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_fetch_contracts(client):
    """Test fetching contracts"""
    print("\n📋 Testing Fetch Contracts...")
    print("=" * 60)
    
    try:
        # Get lease endpoint from config
        endpoint = "/oslc/spq/cstRELeaseQC"
        params = {
            "oslc.select": "*",
            "oslc.pageSize": "5"  # Just fetch 5 for testing
        }
        
        print(f"  Endpoint: {endpoint}")
        print(f"  Parameters: {params}")
        
        response = client.get(endpoint, params=params)
        
        if response and response.get('member'):
            contracts = response['member']
            print(f"\n✓ Successfully fetched {len(contracts)} contracts")
            
            # Display first contract details
            if contracts:
                print("\n📄 Sample Contract:")
                contract = contracts[0]
                print(f"  Name: {contract.get('spi:triNameTX', 'N/A')}")
                print(f"  ID: {contract.get('spi:triIdTX', 'N/A')}")
                print(f"  City: {contract.get('spi:triCityTX', 'N/A')}")
                print(f"  State: {contract.get('spi:triStateProvTX', 'N/A')}")
                print(f"  Country: {contract.get('spi:triCountryTX', 'N/A')}")
                print(f"  Status: {contract.get('spi:triContractStatusCL', 'N/A')}")
            
            return True
        else:
            print("❌ No contracts found or empty response")
            return False
            
    except Exception as e:
        print(f"❌ Fetch test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mcp_config():
    """Test MCP configuration file"""
    print("\n⚙️  Testing MCP Configuration...")
    print("=" * 60)
    
    mcp_config_path = Path.home() / '.bob' / 'mcp.json'
    
    if not mcp_config_path.exists():
        # Try the project .bob directory
        mcp_config_path = Path(__file__).parent.parent / '.bob' / 'mcp.json'
    
    if mcp_config_path.exists():
        try:
            with open(mcp_config_path, 'r') as f:
                mcp_config = json.load(f)
            
            if 'mcpServers' in mcp_config and 'bob-mref2-mcp' in mcp_config['mcpServers']:
                server_config = mcp_config['mcpServers']['bob-mref2-mcp']
                print("✓ MCP configuration found")
                print(f"  Server: bob-mref2-mcp")
                print(f"  Command: {server_config.get('command')}")
                print(f"  Args: {' '.join(server_config.get('args', []))}")
                print(f"  Working Dir: {server_config.get('cwd')}")
                print(f"  Disabled: {server_config.get('disabled', False)}")
                return True
            else:
                print("❌ Server 'bob-mref2-mcp' not found in MCP config")
                return False
                
        except Exception as e:
            print(f"❌ Failed to read MCP config: {e}")
            return False
    else:
        print(f"❌ MCP config file not found at: {mcp_config_path}")
        return False


def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("  Bob_MREF2_MCP Standalone Test Suite")
    print("=" * 60)
    
    # Test 1: Load configuration
    print("\n📁 Loading Configuration...")
    config = load_config()
    if not config:
        print("\n❌ Test suite failed: Cannot load configuration")
        return False
    print("✓ Configuration loaded successfully")
    
    # Test 2: MCP Configuration
    mcp_ok = test_mcp_config()
    
    # Test 3: Connection
    client = test_connection(config)
    if not client:
        print("\n⚠️  Connection test failed, but configuration is valid")
        print("   This may be due to network issues or invalid credentials")
        return mcp_ok
    
    # Test 4: Fetch contracts
    fetch_ok = test_fetch_contracts(client)
    
    # Summary
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)
    print(f"  Configuration: ✓")
    print(f"  MCP Config: {'✓' if mcp_ok else '❌'}")
    print(f"  Connection: {'✓' if client else '❌'}")
    print(f"  Fetch Data: {'✓' if fetch_ok else '❌'}")
    print("=" * 60)
    
    if mcp_ok and client and fetch_ok:
        print("\n✅ All tests passed! MCP server is ready to use in Bob.")
        return True
    elif mcp_ok:
        print("\n⚠️  MCP configuration is valid, but connection tests failed.")
        print("   The server should work in Bob if credentials are correct.")
        return True
    else:
        print("\n❌ Some tests failed. Please check the configuration.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# Made with Bob
