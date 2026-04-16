#!/usr/bin/env python3
"""
Export contracts from JSON to CSV format
Converts all_contracts_output.json to a clean CSV file
"""

import json
import csv
from datetime import datetime
from pathlib import Path


def export_contracts_to_csv(json_file='all_contracts_output.json', csv_file=None):
    """
    Export contracts from JSON to CSV format
    
    Args:
        json_file: Path to input JSON file
        csv_file: Path to output CSV file (auto-generated if None)
    """
    # Set default CSV filename with timestamp
    if csv_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file = f'contracts_export_{timestamp}.csv'
    
    # Read JSON data
    print(f"Reading contracts from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    contracts = data.get('contracts', [])
    total_count = data.get('total_count', 0)
    retrieved_count = data.get('retrieved_count', 0)
    
    print(f"Total contracts: {total_count}")
    print(f"Retrieved contracts: {retrieved_count}")
    print(f"Contracts to export: {len(contracts)}")
    
    if not contracts:
        print("No contracts found to export!")
        return
    
    # Define CSV column mapping (clean names)
    column_mapping = {
        'dcterms:identifier': 'Contract_ID',
        'spi:triIdTX': 'Contract_Code',
        'spi:triNameTX': 'Contract_Name',
        'spi:triStatusCL': 'Status',
        'spi:triContractStatusCL': 'Contract_Status',
        'spi:triProviderTypeLI': 'Provider_Type',
        'spi:triAccountingTypeLI': 'Accounting_Type',
        'spi:triAccountingCalendarCL': 'Accounting_Calendar',
        'spi:triStartDA': 'Start_Date',
        'spi:triExpirationDA': 'Expiration_Date',
        'spi:triContractRentableNU': 'Rentable_Area',
        'spi:triCityTX': 'City',
        'spi:triStateProvTX': 'State_Province',
        'spi:triCountryTX': 'Country',
        'spi:triUserMessageFlagTX': 'User_Message_Flag',
        'rdf:about': 'Resource_URL',
        'spi:action': 'Action_URL'
    }
    
    # Get all unique keys from contracts
    all_keys = set()
    for contract in contracts:
        all_keys.update(contract.keys())
    
    # Create ordered fieldnames
    fieldnames = []
    for key in column_mapping.keys():
        if key in all_keys:
            fieldnames.append(column_mapping[key])
    
    # Add any additional fields not in mapping
    for key in sorted(all_keys):
        if key not in column_mapping:
            fieldnames.append(key)
    
    # Write to CSV
    print(f"\nExporting to {csv_file}...")
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for contract in contracts:
            # Map contract data to clean column names
            row = {}
            for original_key, clean_name in column_mapping.items():
                if original_key in contract:
                    value = contract[original_key]
                    # Convert None to empty string for CSV
                    row[clean_name] = '' if value is None else value
            
            # Add any additional fields
            for key in contract.keys():
                if key not in column_mapping:
                    value = contract[key]
                    row[key] = '' if value is None else value
            
            writer.writerow(row)
    
    print(f"✓ Successfully exported {len(contracts)} contracts to {csv_file}")
    
    # Print summary statistics
    print("\n" + "="*60)
    print("EXPORT SUMMARY")
    print("="*60)
    print(f"Output file: {csv_file}")
    print(f"Total records: {len(contracts)}")
    print(f"Columns: {len(fieldnames)}")
    print("\nColumn names:")
    for i, col in enumerate(fieldnames, 1):
        print(f"  {i:2d}. {col}")
    
    # Show statistics if available
    if 'statistics' in data:
        stats = data['statistics']
        print("\n" + "="*60)
        print("CONTRACT STATISTICS")
        print("="*60)
        
        if 'by_status' in stats:
            print("\nBy Status:")
            for status, count in sorted(stats['by_status'].items(), key=lambda x: x[1], reverse=True):
                status_name = status if status else '(No Status)'
                print(f"  {status_name}: {count}")
        
        if 'by_country' in stats:
            print("\nTop 10 Countries:")
            countries = sorted(stats['by_country'].items(), key=lambda x: x[1], reverse=True)[:10]
            for country, count in countries:
                country_name = country if country else '(No Country)'
                print(f"  {country_name}: {count}")
    
    return csv_file


if __name__ == '__main__':
    import sys
    
    # Get file paths from command line or use defaults
    json_file = sys.argv[1] if len(sys.argv) > 1 else 'all_contracts_output.json'
    csv_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        output_file = export_contracts_to_csv(json_file, csv_file)
        print(f"\n✓ Export complete! File saved as: {output_file}")
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Made with Bob
