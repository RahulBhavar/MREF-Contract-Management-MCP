"""
MREF OSLC API Client - Maximo Real Estate and Facilities
Implements authentication and OSLC endpoint operations
Supports GET and POST operations for OSLC queries and service objects
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mref_oslc_client.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MREFOSLCClient:
    """
    Maximo Real Estate and Facilities OSLC API Client
    
    Authenticates using /p/websignon/signon endpoint
    Provides GET and POST operations for OSLC endpoints
    """
    
    def __init__(self, base_url: str, username: str, password: str):
        """
        Initialize MREF OSLC API Client
        
        Args:
            base_url: TRIRIGA base URL (e.g., https://semas.facilities.semas.apps.srvengmas.cp.fyre.ibm.com/app/tririga)
            username: TRIRIGA username
            password: TRIRIGA password
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        
        # Session management
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification
        self.authenticated = False
        self.cookies = None
        
        logger.info(f"Initialized MREF OSLC API Client for {self.base_url}")
    
    def authenticate(self) -> Dict[str, Any]:
        """
        Authenticate with MREF using /p/websignon/signon endpoint
        
        Returns:
            Authentication result dictionary with success status and session cookies
        """
        logger.info("=" * 80)
        logger.info("MREF AUTHENTICATION - /p/websignon/signon")
        logger.info("=" * 80)
        
        # Authentication endpoint
        auth_url = f"{self.base_url}/p/websignon/signon"
        
        # Prepare authentication payload
        auth_payload = {
            'userName': self.username,
            'password': self.password
        }
        
        # Set headers (X-Requested-With is required for AJAX requests)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        try:
            logger.info(f"POST {auth_url}")
            logger.info(f"Username: {self.username}")
            
            start_time = datetime.now()
            response = self.session.post(
                auth_url,
                json=auth_payload,
                headers=headers,
                timeout=30
            )
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            logger.info(f"Response Status: HTTP {response.status_code} ({duration_ms:.0f}ms)")
            
            # Check if authentication was successful
            if response.ok:  # HTTP 200-299
                self.authenticated = True
                self.cookies = response.cookies
                
                # Try to parse response
                try:
                    response_data = response.json()
                except:
                    response_data = {'text': response.text}
                
                # Log cookies
                if self.cookies:
                    logger.info(f"Cookies Received: {list(self.cookies.keys())}")
                    for cookie in self.cookies:
                        cookie_value = cookie.value if cookie.value else ""
                        logger.info(f"  - {cookie.name}: {cookie_value[:50]}...")
                
                result = {
                    'success': True,
                    'status_code': response.status_code,
                    'message': 'Authentication successful',
                    'duration_ms': duration_ms,
                    'cookies': dict(self.cookies),
                    'response_data': response_data
                }
                
                logger.info("✅ Authentication SUCCESSFUL!")
                return result
            else:
                logger.error(f"❌ Authentication FAILED: HTTP {response.status_code}")
                logger.error(f"Response: {response.text}")
                
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'message': f'Authentication failed: HTTP {response.status_code}',
                    'error': response.text
                }
                
        except Exception as e:
            logger.error(f"❌ Authentication ERROR: {e}")
            return {
                'success': False,
                'message': f'Authentication error: {str(e)}',
                'error': str(e)
            }
    
    def oslc_get(self, endpoint: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Perform GET request to OSLC endpoint
        
        Args:
            endpoint: OSLC endpoint path (e.g., '/oslc/spq/cstRELeaseQC')
            params: Optional query parameters (e.g., {'oslc.select': '*'})
        
        Returns:
            Response dictionary with success status and data
        
        Example:
            result = client.oslc_get('/oslc/spq/cstRELeaseQC', {'oslc.select': '*'})
        """
        if not self.authenticated:
            return {
                'success': False,
                'message': 'Not authenticated. Call authenticate() first.',
                'error': 'Authentication required'
            }
        
        logger.info("=" * 80)
        logger.info(f"OSLC GET REQUEST - {endpoint}")
        logger.info("=" * 80)
        
        # Build full URL
        url = f"{self.base_url}{endpoint}"
        
        # Set headers (X-Requested-With is required for AJAX requests)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        try:
            logger.info(f"GET {url}")
            if params:
                logger.info(f"Parameters: {json.dumps(params, indent=2)}")
            
            start_time = datetime.now()
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=30
            )
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            logger.info(f"Response Status: HTTP {response.status_code} ({duration_ms:.0f}ms)")
            
            if response.ok:
                try:
                    data = response.json()
                    
                    # Extract count if available
                    count = 0
                    if isinstance(data, dict):
                        if 'oslc:results' in data:
                            count = len(data['oslc:results'])
                        elif 'member' in data:
                            count = len(data['member'])
                    elif isinstance(data, list):
                        count = len(data)
                    
                    result = {
                        'success': True,
                        'status_code': response.status_code,
                        'duration_ms': duration_ms,
                        'count': count,
                        'data': data,
                        'message': f'Successfully retrieved {count} records'
                    }
                    
                    logger.info(f"✅ GET Request SUCCESSFUL - Retrieved {count} records")
                    return result
                    
                except json.JSONDecodeError:
                    logger.warning("Response is not JSON, returning as text")
                    return {
                        'success': True,
                        'status_code': response.status_code,
                        'duration_ms': duration_ms,
                        'data': response.text,
                        'message': 'Response received (non-JSON)'
                    }
            else:
                logger.error(f"❌ GET Request FAILED: HTTP {response.status_code}")
                logger.error(f"Response: {response.text}")
                
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'message': f'GET request failed: HTTP {response.status_code}',
                    'error': response.text
                }
                
        except Exception as e:
            logger.error(f"❌ GET Request ERROR: {e}")
            return {
                'success': False,
                'message': f'GET request error: {str(e)}',
                'error': str(e)
            }
    
    def oslc_post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform POST request to OSLC endpoint
        
        Args:
            endpoint: OSLC endpoint path (e.g., '/oslc/so/cstRELeaseCF')
            data: Request body data
        
        Returns:
            Response dictionary with success status and created resource info
        
        Example:
            data = {
                "userName": "facilitiesadmin",
                "password": "passwordpassword",
                "spi:action": "Create Draft",
                "spi:triNameTX": "5 year RE Lease",
                ...
            }
            result = client.oslc_post('/oslc/so/cstRELeaseCF', data)
        """
        if not self.authenticated:
            return {
                'success': False,
                'message': 'Not authenticated. Call authenticate() first.',
                'error': 'Authentication required'
            }
        
        logger.info("=" * 80)
        logger.info(f"OSLC POST REQUEST - {endpoint}")
        logger.info("=" * 80)
        
        # Build full URL
        url = f"{self.base_url}{endpoint}"
        
        # Set headers
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        try:
            logger.info(f"POST {url}")
            logger.info(f"Payload: {json.dumps(data, indent=2)}")
            
            start_time = datetime.now()
            response = self.session.post(
                url,
                json=data,
                headers=headers,
                timeout=30
            )
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            logger.info(f"Response Status: HTTP {response.status_code} ({duration_ms:.0f}ms)")
            
            if response.ok or response.status_code == 201:  # Success or Created
                try:
                    response_data = response.json()
                    
                    result = {
                        'success': True,
                        'status_code': response.status_code,
                        'duration_ms': duration_ms,
                        'data': response_data,
                        'message': 'Resource created successfully'
                    }
                    
                    logger.info("✅ POST Request SUCCESSFUL")
                    return result
                    
                except json.JSONDecodeError:
                    logger.warning("Response is not JSON, returning as text")
                    return {
                        'success': True,
                        'status_code': response.status_code,
                        'duration_ms': duration_ms,
                        'data': response.text,
                        'message': 'Resource created (non-JSON response)'
                    }
            else:
                logger.error(f"❌ POST Request FAILED: HTTP {response.status_code}")
                logger.error(f"Response: {response.text}")
                
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'message': f'POST request failed: HTTP {response.status_code}',
                    'error': response.text
                }
                
        except Exception as e:
            logger.error(f"❌ POST Request ERROR: {e}")
            return {
                'success': False,
                'message': f'POST request error: {str(e)}',
                'error': str(e)
            }
    
    def close(self):
        """Close the session"""
        if self.session:
            self.session.close()
            logger.info("Session closed")


# Example usage
if __name__ == "__main__":
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Initialize client
    client = MREFOSLCClient(
        base_url=config['mref']['base_url'],
        username=config['mref']['username'],
        password=config['mref']['password']
    )
    
    # Authenticate
    auth_result = client.authenticate()
    print(f"\nAuthentication: {auth_result['message']}")
    
    if auth_result['success']:
        # Example GET request
        print("\n" + "=" * 80)
        print("Testing OSLC GET Request")
        print("=" * 80)
        get_result = client.oslc_get('/oslc/spq/cstRELeaseQC', {'oslc.select': '*'})
        print(f"GET Result: {get_result['message']}")
        if get_result['success']:
            print(f"Records retrieved: {get_result['count']}")
        
        # Example POST request
        print("\n" + "=" * 80)
        print("Testing OSLC POST Request")
        print("=" * 80)
        post_data = {
            "userName": "facilitiesadmin",
            "password": "passwordpassword",
            "spi:action": "Create Draft",
            "spi:triProviderTypeLI": "Primary",
            "spi:triCityTX": "OAKBROOK TERRACE",
            "spi:triStartDA": "2019-01-01",
            "spi:triIdTX": "GPNA-US-RE-OP-TERMOPEX1",
            "spi:triCountryTX": "United States",
            "spi:triContractStatusCL": "Active",
            "spi:triAccountingTypeLI": "Accounts Payable (AP)",
            "spi:triStateProvTX": "Illinois",
            "spi:triExpirationDA": "2023-12-12",
            "spi:triUserMessageFlagTX": "",
            "spi:triNameTX": "5 year RE Lease, exercise termination option112",
            "spi:triAccountingCalendarCL": "Standard Calendar"
        }
        post_result = client.oslc_post('/oslc/so/cstRELeaseCF', post_data)
        print(f"POST Result: {post_result['message']}")
    
    # Close session
    client.close()

# Made with Bob
