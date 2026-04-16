#!/usr/bin/env python3
"""
Create Lease with ID 17032026 using OSLC API
Uses proper MREF OSLC authentication with JSESSIONID and creates lease via OSLC service object endpoint
"""

import json
import sys
from datetime import datetime, timedelta
from mref_oslc_client import MREFOSLCClient


def create_lease_17032026():
    """
    Create a new lease with ID 17032026 using OSLC API
    """
    print("=" * 100)
    print("CREATE LEASE 17032026 - OSLC API")
    print("=" * 100)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load configuration
    print("\n[Step 1] Loading OSLC configuration...")
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        mref_config = config['mref']
        oslc_endpoints = config['oslc_endpoints']
        
        print(f"✅ Configuration loaded")
        print(f"   Base URL: {mref_config['base_url']}")
        print(f"   Username: {mref_config['username']}")
        print(f"   Auth Path: {mref_config['auth_path']}")
        print(f"   Lease Service Object: {oslc_endpoints['service_object']['lease']}")
        
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False
    
    # Initialize OSLC client
    print("\n[Step 2] Initializing MREF OSLC Client...")
    client = MREFOSLCClient(
        base_url=mref_config['base_url'],
        username=mref_config['username'],
        password=mref_config['password']
    )
    print("✅ OSLC Client initialized")
    
    # Authenticate and get JSESSIONID
    print("\n[Step 3] Authenticating with MREF...")
    print(f"   Endpoint: {mref_config['base_url']}{mref_config['auth_path']}")
    
    auth_result = client.authenticate()
    
    if not auth_result['success']:
        print(f"❌ Authentication failed!")
        print(f"   Status: {auth_result.get('status_code', 'N/A')}")
        print(f"   Error: {auth_result.get('error', 'Unknown error')}")
        return False
    
    print(f"✅ Authentication successful!")
    print(f"   Status: HTTP {auth_result['status_code']}")
    print(f"   Duration: {auth_result['duration_ms']:.0f}ms")
    
    # Show JSESSIONID
    jsessionid = auth_result.get('cookies', {}).get('JSESSIONID', 'N/A')
    print(f"   JSESSIONID: {jsessionid[:50]}...")
    
    # Prepare lease data
    print("\n[Step 4] Preparing lease data for ID 17032026...")
    
    # Calculate dates
    start_date = datetime.now()
    end_date = start_date + timedelta(days=1825)  # 5 years
    
    lease_data = {
        # Authentication (required for OSLC service object)
        "userName": mref_config['username'],
        "password": mref_config['password'],
        
        # OSLC action
        "spi:action": "Create Draft",
        
        # Primary identification - matching working example
        "spi:triIdTX": "17032026",
        "spi:triNameTX": "Real Estate Lease 17032026 - Created via OSLC API",
        
        # Provider and type (from working example)
        "spi:triProviderTypeLI": "Primary",
        "spi:triAccountingTypeLI": "Accounts Payable (AP)",
        
        # Location details (matching working example format)
        "spi:triCityTX": "OAKBROOK TERRACE",
        "spi:triStateProvTX": "Illinois",
        "spi:triCountryTX": "United States",
        
        # Dates (YYYY-MM-DD format)
        "spi:triStartDA": start_date.strftime('%Y-%m-%d'),
        "spi:triExpirationDA": end_date.strftime('%Y-%m-%d'),
        
        # Status - use triContractStatusCL not triStatusCL (from working example)
        "spi:triContractStatusCL": "Active",
        
        # Additional properties (from working example)
        "spi:triAccountingCalendarCL": "Standard Calendar",
        "spi:triUserMessageFlagTX": ""
    }
    
    print("✅ Lease data prepared")
    print(f"   Lease ID: {lease_data['spi:triIdTX']}")
    print(f"   Lease Name: {lease_data['spi:triNameTX']}")
    print(f"   Location: {lease_data['spi:triCityTX']}, {lease_data['spi:triStateProvTX']}, {lease_data['spi:triCountryTX']}")
    print(f"   Contract Status: {lease_data['spi:triContractStatusCL']}")
    print(f"   Start Date: {lease_data['spi:triStartDA']}")
    print(f"   End Date: {lease_data['spi:triExpirationDA']}")
    print(f"   Provider Type: {lease_data['spi:triProviderTypeLI']}")
    print(f"   Accounting Type: {lease_data['spi:triAccountingTypeLI']}")
    print(f"   Accounting Calendar: {lease_data['spi:triAccountingCalendarCL']}")
    
    # Create the lease using OSLC service object endpoint
    print("\n[Step 5] Creating lease via OSLC service object...")
    lease_endpoint = oslc_endpoints['service_object']['lease']
    print(f"   POST {mref_config['base_url']}{lease_endpoint}")
    print(f"   Using JSESSIONID: {jsessionid[:20]}...")
    print(f"   Payload size: {len(json.dumps(lease_data))} bytes")
    
    create_result = client.oslc_post(lease_endpoint, lease_data)
    
    print(f"\n   Response Status: HTTP {create_result.get('status_code', 'N/A')}")
    print(f"   Duration: {create_result.get('duration_ms', 0):.0f}ms")
    
    if not create_result['success']:
        print(f"❌ Lease creation failed!")
        print(f"   Error: {create_result.get('error', 'Unknown error')}")
        print(f"   Message: {create_result.get('message', 'No message')}")
        return False
    
    print(f"✅ Lease creation request successful!")
    
    # Show response data if available
    if 'data' in create_result and create_result['data']:
        print(f"\n   Response Data:")
        if isinstance(create_result['data'], dict):
            print(f"   {json.dumps(create_result['data'], indent=6)}")
        else:
            print(f"   {create_result['data']}")
    
    # Verify the lease was created by querying
    print("\n[Step 6] Verifying lease creation...")
    query_endpoint = oslc_endpoints['query']['lease']
    print(f"   GET {mref_config['base_url']}{query_endpoint}")
    
    # Query parameters to find our lease
    query_params = {
        'oslc.select': '*',
        'oslc.where': f'spi:triIdTX="17032026"',
        'oslc.pageSize': '10'
    }
    
    try:
        verify_result = client.oslc_get(query_endpoint, query_params)
        
        if verify_result['success']:
            print(f"✅ Lease verification query successful!")
            print(f"   Status: HTTP {verify_result['status_code']}")
            print(f"   Duration: {verify_result['duration_ms']:.0f}ms")
            print(f"   Records found: {verify_result.get('count', 0)}")
            
            if verify_result.get('count', 0) > 0:
                print(f"\n✅ LEASE 17032026 FOUND IN SYSTEM!")
                print(f"   The lease was successfully created and is now available in MREF")
                
                # Show some details from the found lease
                data = verify_result.get('data', {})
                if isinstance(data, dict) and 'oslc:results' in data:
                    results = data['oslc:results']
                    if results and len(results) > 0:
                        lease = results[0]
                        print(f"\n   Found Lease Details:")
                        print(f"   - ID: {lease.get('spi:triIdTX', 'N/A')}")
                        print(f"   - Name: {lease.get('spi:triNameTX', 'N/A')}")
                        print(f"   - Status: {lease.get('spi:triStatusCL', 'N/A')}")
                        print(f"   - City: {lease.get('spi:triCityTX', 'N/A')}")
                        print(f"   - Start Date: {lease.get('spi:triStartDA', 'N/A')}")
                        print(f"   - Expiration Date: {lease.get('spi:triExpirationDA', 'N/A')}")
            else:
                print(f"⚠️  Lease not found in verification query")
                print(f"   Note: The lease may have been created but might take time to appear in queries")
                print(f"   Or the lease might be in draft status and not yet visible")
        else:
            print(f"⚠️  Verification query failed")
            print(f"   Status: HTTP {verify_result.get('status_code', 'N/A')}")
            print(f"   Note: Lease creation may have succeeded despite verification failure")
            
    except Exception as e:
        print(f"⚠️  Verification error: {e}")
        print(f"   Note: Lease may have been created successfully")
    
    # Close client
    client.close()
    
    # Summary
    print("\n" + "=" * 100)
    print("OPERATION SUMMARY")
    print("=" * 100)
    print(f"✅ Authentication: SUCCESS (JSESSIONID obtained)")
    print(f"✅ Lease Creation: SUCCESS (HTTP {create_result.get('status_code', 'N/A')})")
    print(f"   Lease ID: 17032026")
    print(f"   Lease Name: {lease_data['spi:triNameTX']}")
    print(f"   Location: {lease_data['spi:triCityTX']}, {lease_data['spi:triStateProvTX']}, {lease_data['spi:triCountryTX']}")
    print(f"   Contract Status: {lease_data['spi:triContractStatusCL']}")
    print(f"   Provider Type: {lease_data['spi:triProviderTypeLI']}")
    print(f"   Accounting Type: {lease_data['spi:triAccountingTypeLI']}")
    print(f"   Duration: {lease_data['spi:triStartDA']} to {lease_data['spi:triExpirationDA']}")
    print("=" * 100)
    
    return True


def main():
    """Main execution"""
    try:
        success = create_lease_17032026()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob