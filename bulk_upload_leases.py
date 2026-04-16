#!/usr/bin/env python3
"""
Bulk Upload Leases from CSV to MREF using OSLC API
Reads lease data from CSV and creates multiple leases using authenticated OSLC service object endpoint
"""

import json
import sys
import csv
from datetime import datetime
from mref_oslc_client import MREFOSLCClient
import time


def load_leases_from_csv(csv_file):
    """
    Load lease data from CSV file
    
    Args:
        csv_file: Path to CSV file
        
    Returns:
        List of lease dictionaries
    """
    leases = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                leases.append(row)
        
        print(f"✅ Loaded {len(leases)} leases from {csv_file}")
        return leases
        
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return []


def create_lease_payload(csv_row, username, password):
    """
    Convert CSV row to OSLC lease payload
    
    Args:
        csv_row: Dictionary from CSV row
        username: MREF username
        password: MREF password
        
    Returns:
        OSLC payload dictionary
    """
    payload = {
        # Authentication (required for OSLC service object)
        "userName": username,
        "password": password,
        
        # OSLC action
        "spi:action": "Create Draft",
        
        # Map CSV columns to OSLC properties
        "spi:triIdTX": csv_row.get('triIdTX', ''),
        "spi:triNameTX": csv_row.get('triNameTX', ''),
        "spi:triProviderTypeLI": csv_row.get('triProviderTypeLI', 'Primary'),
        "spi:triAccountingTypeLI": csv_row.get('triAccountingTypeLI', 'Accounts Payable (AP)'),
        "spi:triCityTX": csv_row.get('triCityTX', ''),
        "spi:triStateProvTX": csv_row.get('triStateProvTX', ''),
        "spi:triCountryTX": csv_row.get('triCountryTX', ''),
        "spi:triStartDA": csv_row.get('triStartDA', ''),
        "spi:triExpirationDA": csv_row.get('triExpirationDA', ''),
        "spi:triContractStatusCL": csv_row.get('triContractStatusCL', 'Active'),
        "spi:triAccountingCalendarCL": csv_row.get('triAccountingCalendarCL', 'Standard Calendar'),
        "spi:triUserMessageFlagTX": csv_row.get('triUserMessageFlagTX', '')
    }
    
    return payload


def bulk_upload_leases(csv_file='lease_bulk_upload_template.csv'):
    """
    Bulk upload leases from CSV file
    
    Args:
        csv_file: Path to CSV file with lease data
    """
    print("=" * 100)
    print("BULK UPLOAD LEASES - OSLC API")
    print("=" * 100)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"CSV File: {csv_file}")
    
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
        
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False
    
    # Load leases from CSV
    print("\n[Step 2] Loading leases from CSV...")
    leases = load_leases_from_csv(csv_file)
    
    if not leases:
        print("❌ No leases to upload")
        return False
    
    print(f"   Found {len(leases)} leases to upload")
    
    # Initialize OSLC client
    print("\n[Step 3] Initializing MREF OSLC Client...")
    client = MREFOSLCClient(
        base_url=mref_config['base_url'],
        username=mref_config['username'],
        password=mref_config['password']
    )
    print("✅ OSLC Client initialized")
    
    # Authenticate
    print("\n[Step 4] Authenticating with MREF...")
    auth_result = client.authenticate()
    
    if not auth_result['success']:
        print(f"❌ Authentication failed!")
        print(f"   Status: {auth_result.get('status_code', 'N/A')}")
        return False
    
    print(f"✅ Authentication successful!")
    print(f"   Status: HTTP {auth_result['status_code']}")
    print(f"   Duration: {auth_result['duration_ms']:.0f}ms")
    
    jsessionid = auth_result.get('cookies', {}).get('JSESSIONID', 'N/A')
    print(f"   JSESSIONID: {jsessionid[:50]}...")
    
    # Upload leases
    print("\n[Step 5] Uploading leases...")
    print("=" * 100)
    
    lease_endpoint = oslc_endpoints['service_object']['lease']
    results = {
        'success': [],
        'failed': [],
        'total': len(leases)
    }
    
    for idx, csv_row in enumerate(leases, 1):
        lease_id = csv_row.get('triIdTX', 'Unknown')
        lease_name = csv_row.get('triNameTX', 'Unknown')
        
        print(f"\n[{idx}/{len(leases)}] Creating Lease: {lease_id}")
        print(f"   Name: {lease_name}")
        print(f"   Location: {csv_row.get('triCityTX', 'N/A')}, {csv_row.get('triStateProvTX', 'N/A')}")
        
        # Create payload
        payload = create_lease_payload(csv_row, mref_config['username'], mref_config['password'])
        
        # Create lease
        try:
            create_result = client.oslc_post(lease_endpoint, payload)
            
            if create_result['success'] and create_result.get('status_code') == 201:
                print(f"   ✅ SUCCESS - HTTP {create_result['status_code']} ({create_result.get('duration_ms', 0):.0f}ms)")
                results['success'].append({
                    'id': lease_id,
                    'name': lease_name,
                    'status_code': create_result['status_code'],
                    'duration_ms': create_result.get('duration_ms', 0)
                })
            else:
                print(f"   ❌ FAILED - HTTP {create_result.get('status_code', 'N/A')}")
                print(f"   Error: {create_result.get('error', 'Unknown error')}")
                results['failed'].append({
                    'id': lease_id,
                    'name': lease_name,
                    'status_code': create_result.get('status_code', 'N/A'),
                    'error': create_result.get('error', 'Unknown error')
                })
        
        except Exception as e:
            print(f"   ❌ EXCEPTION: {e}")
            results['failed'].append({
                'id': lease_id,
                'name': lease_name,
                'error': str(e)
            })
        
        # Add delay between requests to avoid overwhelming the server
        if idx < len(leases):
            time.sleep(1)  # 1 second delay between requests
    
    # Close client
    client.close()
    
    # Summary
    print("\n" + "=" * 100)
    print("BULK UPLOAD SUMMARY")
    print("=" * 100)
    print(f"Total Leases: {results['total']}")
    print(f"✅ Successful: {len(results['success'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"Success Rate: {(len(results['success']) / results['total'] * 100):.1f}%")
    
    if results['success']:
        print(f"\n✅ Successfully Created Leases:")
        for lease in results['success']:
            print(f"   - {lease['id']}: {lease['name']} (HTTP {lease['status_code']}, {lease['duration_ms']:.0f}ms)")
    
    if results['failed']:
        print(f"\n❌ Failed Leases:")
        for lease in results['failed']:
            error_msg = lease.get('error', 'Unknown error')
            if len(error_msg) > 100:
                error_msg = error_msg[:100] + "..."
            print(f"   - {lease['id']}: {lease['name']}")
            print(f"     Error: {error_msg}")
    
    print("=" * 100)
    
    # Save results to JSON
    results_file = f"bulk_upload_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Results saved to: {results_file}")
    
    return len(results['failed']) == 0


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Bulk upload leases from CSV to MREF')
    parser.add_argument('csv_file', nargs='?', default='lease_bulk_upload_template.csv',
                       help='Path to CSV file (default: lease_bulk_upload_template.csv)')
    
    args = parser.parse_args()
    
    try:
        success = bulk_upload_leases(args.csv_file)
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