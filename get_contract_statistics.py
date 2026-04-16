#!/usr/bin/env python3
"""
Generate Detailed Contract Statistics from MREF Data
Analyzes all_contracts_output.json and provides comprehensive statistics
"""

import json
from datetime import datetime
from collections import Counter, defaultdict


def load_contracts(json_file='all_contracts_output.json'):
    """Load contracts from JSON file"""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def analyze_contracts(data):
    """Perform comprehensive analysis of contracts"""
    contracts = data.get('contracts', [])
    
    stats = {
        'overview': {
            'total_count': data.get('total_count', 0),
            'retrieved_count': data.get('retrieved_count', 0),
            'success': data.get('success', False)
        },
        'by_status': Counter(),
        'by_contract_status': Counter(),
        'by_country': Counter(),
        'by_city': Counter(),
        'by_state': Counter(),
        'by_provider_type': Counter(),
        'by_accounting_type': Counter(),
        'by_accounting_calendar': Counter(),
        'rentable_area': {
            'total': 0,
            'count': 0,
            'min': float('inf'),
            'max': 0,
            'values': []
        },
        'date_ranges': {
            'start_dates': [],
            'expiration_dates': []
        },
        'top_contracts': []
    }
    
    # Analyze each contract
    for contract in contracts:
        # Status analysis
        status = contract.get('spi:triStatusCL') or 'Unknown'
        stats['by_status'][status] += 1
        
        contract_status = contract.get('spi:triContractStatusCL') or 'Not Set'
        stats['by_contract_status'][contract_status] += 1
        
        # Location analysis
        country = contract.get('spi:triCountryTX') or 'Unknown'
        stats['by_country'][country] += 1
        
        city = contract.get('spi:triCityTX') or 'Unknown'
        stats['by_city'][city] += 1
        
        state = contract.get('spi:triStateProvTX') or 'Unknown'
        stats['by_state'][state] += 1
        
        # Type analysis
        provider = contract.get('spi:triProviderTypeLI') or 'Unknown'
        stats['by_provider_type'][provider] += 1
        
        accounting = contract.get('spi:triAccountingTypeLI') or 'Unknown'
        stats['by_accounting_type'][accounting] += 1
        
        calendar = contract.get('spi:triAccountingCalendarCL') or 'Unknown'
        stats['by_accounting_calendar'][calendar] += 1
        
        # Rentable area analysis
        rentable = contract.get('spi:triContractRentableNU')
        if rentable:
            stats['rentable_area']['total'] += rentable
            stats['rentable_area']['count'] += 1
            stats['rentable_area']['min'] = min(stats['rentable_area']['min'], rentable)
            stats['rentable_area']['max'] = max(stats['rentable_area']['max'], rentable)
            stats['rentable_area']['values'].append(rentable)
        
        # Date analysis
        start_date = contract.get('spi:triStartDA')
        if start_date:
            stats['date_ranges']['start_dates'].append(start_date)
        
        exp_date = contract.get('spi:triExpirationDA')
        if exp_date:
            stats['date_ranges']['expiration_dates'].append(exp_date)
        
        # Store contract info for top contracts
        stats['top_contracts'].append({
            'id': contract.get('spi:triIdTX', 'Unknown'),
            'name': contract.get('spi:triNameTX', 'Unknown'),
            'city': city,
            'country': country,
            'status': status,
            'rentable': rentable or 0,
            'start': start_date,
            'expiration': exp_date
        })
    
    # Calculate averages
    if stats['rentable_area']['count'] > 0:
        stats['rentable_area']['average'] = stats['rentable_area']['total'] / stats['rentable_area']['count']
    else:
        stats['rentable_area']['average'] = 0
    
    # Sort top contracts by rentable area
    stats['top_contracts'].sort(key=lambda x: x['rentable'], reverse=True)
    
    return stats


def print_statistics(stats):
    """Print formatted statistics"""
    print("=" * 100)
    print("MREF CONTRACT STATISTICS - COMPREHENSIVE REPORT")
    print("=" * 100)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Overview
    print("=" * 100)
    print("OVERVIEW")
    print("=" * 100)
    print(f"Total Contracts: {stats['overview']['total_count']}")
    print(f"Retrieved: {stats['overview']['retrieved_count']}")
    print(f"Success: {stats['overview']['success']}")
    print()
    
    # Status Distribution
    print("=" * 100)
    print("STATUS DISTRIBUTION")
    print("=" * 100)
    for status, count in stats['by_status'].most_common():
        percentage = (count / stats['overview']['total_count']) * 100
        print(f"  {status:30s}: {count:4d} ({percentage:5.1f}%)")
    print()
    
    # Contract Status Distribution
    print("=" * 100)
    print("CONTRACT STATUS DISTRIBUTION")
    print("=" * 100)
    for status, count in stats['by_contract_status'].most_common():
        percentage = (count / stats['overview']['total_count']) * 100
        print(f"  {status:30s}: {count:4d} ({percentage:5.1f}%)")
    print()
    
    # Geographic Distribution - Countries
    print("=" * 100)
    print("TOP 15 COUNTRIES")
    print("=" * 100)
    for country, count in stats['by_country'].most_common(15):
        percentage = (count / stats['overview']['total_count']) * 100
        print(f"  {country:30s}: {count:4d} ({percentage:5.1f}%)")
    print()
    
    # Geographic Distribution - Cities
    print("=" * 100)
    print("TOP 20 CITIES")
    print("=" * 100)
    for city, count in stats['by_city'].most_common(20):
        percentage = (count / stats['overview']['total_count']) * 100
        print(f"  {city:30s}: {count:4d} ({percentage:5.1f}%)")
    print()
    
    # Geographic Distribution - States
    print("=" * 100)
    print("TOP 15 STATES/PROVINCES")
    print("=" * 100)
    for state, count in stats['by_state'].most_common(15):
        percentage = (count / stats['overview']['total_count']) * 100
        print(f"  {state:30s}: {count:4d} ({percentage:5.1f}%)")
    print()
    
    # Provider Type Distribution
    print("=" * 100)
    print("PROVIDER TYPE DISTRIBUTION")
    print("=" * 100)
    for provider, count in stats['by_provider_type'].most_common():
        percentage = (count / stats['overview']['total_count']) * 100
        print(f"  {provider:30s}: {count:4d} ({percentage:5.1f}%)")
    print()
    
    # Accounting Type Distribution
    print("=" * 100)
    print("ACCOUNTING TYPE DISTRIBUTION")
    print("=" * 100)
    for accounting, count in stats['by_accounting_type'].most_common():
        percentage = (count / stats['overview']['total_count']) * 100
        print(f"  {accounting:30s}: {count:4d} ({percentage:5.1f}%)")
    print()
    
    # Rentable Area Statistics
    print("=" * 100)
    print("RENTABLE AREA STATISTICS")
    print("=" * 100)
    print(f"  Total Rentable Area: {stats['rentable_area']['total']:,.0f} sq ft")
    print(f"  Contracts with Area: {stats['rentable_area']['count']}")
    print(f"  Average Area: {stats['rentable_area']['average']:,.0f} sq ft")
    print(f"  Minimum Area: {stats['rentable_area']['min']:,.0f} sq ft")
    print(f"  Maximum Area: {stats['rentable_area']['max']:,.0f} sq ft")
    print()
    
    # Date Range Analysis
    print("=" * 100)
    print("DATE RANGE ANALYSIS")
    print("=" * 100)
    if stats['date_ranges']['start_dates']:
        start_dates = sorted(stats['date_ranges']['start_dates'])
        print(f"  Earliest Start Date: {start_dates[0]}")
        print(f"  Latest Start Date: {start_dates[-1]}")
    
    if stats['date_ranges']['expiration_dates']:
        exp_dates = sorted(stats['date_ranges']['expiration_dates'])
        print(f"  Earliest Expiration: {exp_dates[0]}")
        print(f"  Latest Expiration: {exp_dates[-1]}")
    print()
    
    # Top 10 Contracts by Rentable Area
    print("=" * 100)
    print("TOP 10 CONTRACTS BY RENTABLE AREA")
    print("=" * 100)
    for i, contract in enumerate(stats['top_contracts'][:10], 1):
        print(f"\n{i}. {contract['name']}")
        print(f"   ID: {contract['id']}")
        print(f"   Location: {contract['city']}, {contract['country']}")
        print(f"   Status: {contract['status']}")
        print(f"   Rentable Area: {contract['rentable']:,.0f} sq ft")
        print(f"   Duration: {contract['start']} to {contract['expiration']}")
    print()
    
    print("=" * 100)
    print("END OF REPORT")
    print("=" * 100)


def save_statistics_json(stats, output_file='contract_statistics.json'):
    """Save statistics to JSON file"""
    # Convert Counter objects to dicts for JSON serialization
    json_stats = {
        'overview': stats['overview'],
        'by_status': dict(stats['by_status']),
        'by_contract_status': dict(stats['by_contract_status']),
        'by_country': dict(stats['by_country']),
        'by_city': dict(stats['by_city']),
        'by_state': dict(stats['by_state']),
        'by_provider_type': dict(stats['by_provider_type']),
        'by_accounting_type': dict(stats['by_accounting_type']),
        'by_accounting_calendar': dict(stats['by_accounting_calendar']),
        'rentable_area': {
            'total': stats['rentable_area']['total'],
            'count': stats['rentable_area']['count'],
            'average': stats['rentable_area']['average'],
            'min': stats['rentable_area']['min'],
            'max': stats['rentable_area']['max']
        },
        'date_ranges': {
            'earliest_start': min(stats['date_ranges']['start_dates']) if stats['date_ranges']['start_dates'] else None,
            'latest_start': max(stats['date_ranges']['start_dates']) if stats['date_ranges']['start_dates'] else None,
            'earliest_expiration': min(stats['date_ranges']['expiration_dates']) if stats['date_ranges']['expiration_dates'] else None,
            'latest_expiration': max(stats['date_ranges']['expiration_dates']) if stats['date_ranges']['expiration_dates'] else None
        },
        'top_10_contracts': stats['top_contracts'][:10],
        'generated_at': datetime.now().isoformat()
    }
    
    with open(output_file, 'w') as f:
        json.dump(json_stats, f, indent=2)
    
    print(f"\n📄 Statistics saved to: {output_file}")


def main():
    """Main execution"""
    try:
        # Load contracts
        print("Loading contracts from all_contracts_output.json...")
        data = load_contracts()
        
        # Analyze contracts
        print("Analyzing contracts...")
        stats = analyze_contracts(data)
        
        # Print statistics
        print_statistics(stats)
        
        # Save to JSON
        save_statistics_json(stats)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

# Made with Bob