#!/usr/bin/env python3
"""
Standalone script to fetch all contracts from MREF
This demonstrates the fetch_all_contracts functionality
"""

import json
from mref_oslc_client import MREFOSLCClient

def load_config():
    """Load configuration"""
    with open('config.json', 'r') as f:
        return json.load(f)

def fetch_all_contracts(page_size=100):
    """Fetch all contracts"""
    print("=" * 80)
    print("  Fetching All Real Estate Contracts from MREF")
    print("=" * 80)
    
    # Load config
    config = load_config()
    mref_config = config['mref']
    
    # Initialize client
    print(f"\n📡 Connecting to: {mref_config['base_url']}")
    print(f"👤 Username: {mref_config['username']}")
    
    client = MREFOSLCClient(
        base_url=mref_config['base_url'],
        username=mref_config['username'],
        password=mref_config['password']
    )
    
    # Authenticate
    print("\n🔐 Authenticating...")
    auth_result = client.authenticate()
    
    if not auth_result['success']:
        print(f"❌ Authentication failed: {auth_result.get('message')}")
        return None
    
    print("✅ Authentication successful!")
    
    # Fetch contracts
    print(f"\n📋 Fetching contracts (page size: {page_size})...")
    result = client.oslc_get('/oslc/spq/cstRELeaseQC', {
        'oslc.select': '*',
        'oslc.pageSize': str(page_size)
    })
    
    if not result['success']:
        print(f"❌ Failed to fetch contracts: {result.get('error')}")
        return None
    
    # Process results
    data = result.get('data', {})
    contracts = data.get('rdfs:member', [])
    response_info = data.get('oslc:responseInfo', {})
    total_count = response_info.get('oslc:totalCount', len(contracts))
    
    print(f"\n✅ Successfully retrieved {len(contracts)} of {total_count} total contracts")
    
    # Display summary
    print("\n" + "=" * 80)
    print("  CONTRACT SUMMARY")
    print("=" * 80)
    
    # Status distribution
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
    
    print(f"\n📊 Status Distribution:")
    for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(contracts) * 100) if contracts else 0
        print(f"   - {status}: {count} ({percentage:.1f}%)")
    
    print(f"\n🌆 Top 10 Cities:")
    for city, count in sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   - {city}: {count}")
    
    print(f"\n🌍 Countries:")
    for country, count in sorted(country_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {country}: {count}")
    
    # Display sample contracts
    print("\n" + "=" * 80)
    print("  SAMPLE CONTRACTS (First 10)")
    print("=" * 80)
    
    for i, contract in enumerate(contracts[:10], 1):
        print(f"\n{i}. {contract.get('spi:triNameTX', 'N/A')}")
        print(f"   ID: {contract.get('dcterms:identifier', 'N/A')}")
        print(f"   City: {contract.get('spi:triCityTX', 'N/A')}")
        print(f"   State: {contract.get('spi:triStateProvTX', 'N/A')}")
        print(f"   Country: {contract.get('spi:triCountryTX', 'N/A')}")
        print(f"   Status: {contract.get('spi:triContractStatusCL', 'N/A')}")
        print(f"   Start Date: {contract.get('spi:triStartDA', 'N/A')}")
        print(f"   End Date: {contract.get('spi:triExpirationDA', 'N/A')}")
    
    # Save to JSON file
    output_file = 'all_contracts_output.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'success': True,
            'total_count': total_count,
            'retrieved_count': len(contracts),
            'contracts': contracts,
            'statistics': {
                'by_status': status_counts,
                'by_city': city_counts,
                'by_country': country_counts
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Full results saved to: {output_file}")
    print("\n" + "=" * 80)
    
    return {
        'success': True,
        'total_count': total_count,
        'retrieved_count': len(contracts),
        'contracts': contracts
    }

if __name__ == "__main__":
    import sys
    
    # Get page size from command line or use default
    page_size = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    
    result = fetch_all_contracts(page_size)
    
    if result:
        print("\n✅ Operation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Operation failed!")
        sys.exit(1)

# Made with Bob
