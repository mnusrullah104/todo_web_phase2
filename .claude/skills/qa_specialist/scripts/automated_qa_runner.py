#!/usr/bin/env python3
"""
Automated QA runner for verifying implementations against acceptance criteria
"""

import json
import requests
import sys
import argparse
import unittest
import time
from typing import Dict, List, Any, Optional
import yaml
from urllib.parse import urljoin

class QATester:
    """QA Tester class for verifying implementations against acceptance criteria"""

    def __init__(self, base_url: str, config_file: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'QA-Tester/1.0'
        })

        # Load configuration if provided
        self.config = {}
        if config_file:
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f) or {}

    def add_auth_header(self, token: str):
        """Add authentication header to requests"""
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })

    def test_api_endpoint(self, method: str, endpoint: str,
                         expected_status: int = 200,
                         payload: Optional[Dict] = None,
                         headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Test a specific API endpoint"""
        url = urljoin(self.base_url, endpoint)

        # Update headers if provided
        original_headers = self.session.headers.copy()
        if headers:
            self.session.headers.update(headers)

        try:
            response = self.session.request(method, url, json=payload)

            result = {
                'url': url,
                'method': method,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'passed': response.status_code == expected_status,
                'response_time': response.elapsed.total_seconds(),
                'response_body': response.json() if response.content else None,
                'headers': dict(response.headers)
            }

            if not result['passed']:
                result['error'] = f"Expected {expected_status}, got {response.status_code}"

            return result

        except requests.exceptions.RequestException as e:
            return {
                'url': url,
                'method': method,
                'status_code': None,
                'expected_status': expected_status,
                'passed': False,
                'error': str(e),
                'response_time': None
            }
        finally:
            # Restore original headers
            self.session.headers.clear()
            self.session.headers.update(original_headers)

    def test_unauthorized_access(self, method: str, endpoint: str) -> Dict[str, Any]:
        """Test that unauthorized access returns 401"""
        # Temporarily remove auth header
        auth_header = self.session.headers.pop('Authorization', None)

        try:
            result = self.test_api_endpoint(method, endpoint, expected_status=401)

            if result['status_code'] == 401:
                result['passed'] = True
                result['message'] = "Correctly returned 401 Unauthorized"
            elif result['status_code'] == 200:
                result['passed'] = False
                result['error'] = "Should have returned 401 Unauthorized but returned 200 OK"
            else:
                result['passed'] = False
                result['error'] = f"Expected 401, got {result['status_code']}"

            return result
        finally:
            # Restore auth header if it existed
            if auth_header:
                self.session.headers['Authorization'] = auth_header

    def test_input_validation(self, endpoint: str, invalid_payloads: List[Dict]) -> List[Dict[str, Any]]:
        """Test input validation with invalid payloads"""
        results = []

        for i, payload in enumerate(invalid_payloads):
            result = self.test_api_endpoint('POST', endpoint, expected_status=400, payload=payload)
            result['test_case'] = f'invalid_payload_{i+1}'
            results.append(result)

        return results

    def run_acceptance_criteria_tests(self, criteria: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run tests based on acceptance criteria"""
        results = {
            'total_tests': len(criteria),
            'passed_tests': 0,
            'failed_tests': 0,
            'results': []
        }

        for i, criterion in enumerate(criteria):
            print(f"Running test {i+1}/{len(criteria)}: {criterion.get('description', f'Test {i+1}')}")

            test_type = criterion.get('type', 'api_test')

            if test_type == 'api_test':
                result = self.test_api_endpoint(
                    method=criterion.get('method', 'GET'),
                    endpoint=criterion.get('endpoint'),
                    expected_status=criterion.get('expected_status', 200),
                    payload=criterion.get('payload'),
                    headers=criterion.get('headers')
                )
            elif test_type == 'unauthorized_test':
                result = self.test_unauthorized_access(
                    method=criterion.get('method', 'GET'),
                    endpoint=criterion.get('endpoint')
                )
            elif test_type == 'validation_test':
                invalid_payloads = criterion.get('invalid_payloads', [])
                validation_results = self.test_input_validation(
                    criterion.get('endpoint'),
                    invalid_payloads
                )
                result = {
                    'test_type': 'validation_test',
                    'passed': all(r['passed'] for r in validation_results),
                    'sub_results': validation_results
                }
            else:
                result = {
                    'passed': False,
                    'error': f'Unknown test type: {test_type}'
                }

            result['criterion'] = criterion
            results['results'].append(result)

            if result.get('passed', False):
                results['passed_tests'] += 1
                print(f"  ✓ PASSED")
            else:
                results['failed_tests'] += 1
                error = result.get('error', 'Unknown error')
                print(f"  ✗ FAILED: {error}")

        return results

def load_test_config(config_file: str) -> Dict[str, Any]:
    """Load test configuration from file"""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def create_sample_test_config():
    """Create a sample test configuration file"""
    sample_config = {
        'base_url': 'http://localhost:8000',
        'auth_token': 'your_jwt_token_here',
        'acceptance_criteria': [
            {
                'description': 'Get all tasks endpoint works',
                'type': 'api_test',
                'method': 'GET',
                'endpoint': '/api/v1/tasks',
                'expected_status': 200
            },
            {
                'description': 'Unauthorized access to protected endpoint',
                'type': 'unauthorized_test',
                'method': 'GET',
                'endpoint': '/api/v1/tasks'
            },
            {
                'description': 'Input validation for task creation',
                'type': 'validation_test',
                'endpoint': '/api/v1/tasks',
                'invalid_payloads': [
                    {'name': ''},  # Missing required field
                    {'name': 'a' * 200},  # Too long name
                    {'name': 'valid_name', 'priority': 'invalid_priority'}  # Invalid enum value
                ]
            },
            {
                'description': 'Create a new task',
                'type': 'api_test',
                'method': 'POST',
                'endpoint': '/api/v1/tasks',
                'expected_status': 201,
                'payload': {
                    'name': 'Test Task',
                    'description': 'A test task',
                    'priority': 'medium'
                }
            }
        ]
    }

    with open('sample_test_config.yaml', 'w') as f:
        yaml.dump(sample_config, f, default_flow_style=False)

    print("Sample test configuration created: sample_test_config.yaml")

def main():
    parser = argparse.ArgumentParser(description='Automated QA Tester for API validation')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--base-url', '-u', help='Base URL for API testing')
    parser.add_argument('--auth-token', '-t', help='Authentication token')
    parser.add_argument('--create-sample', action='store_true', help='Create sample configuration file')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='text', help='Output format')

    args = parser.parse_args()

    if args.create_sample:
        create_sample_test_config()
        return

    if not args.config and not args.base_url:
        print("Error: Either --config or --base-url must be provided")
        parser.print_help()
        sys.exit(1)

    if args.create_sample:
        create_sample_test_config()
        return

    # Initialize tester
    tester = QATester(args.base_url or '')

    if args.config:
        config = load_test_config(args.config)
        base_url = config.get('base_url', args.base_url)
        auth_token = config.get('auth_token', args.auth_token)
        criteria = config.get('acceptance_criteria', [])

        tester = QATester(base_url)

        if auth_token:
            tester.add_auth_header(auth_token)
    else:
        if args.auth_token:
            tester.add_auth_header(args.auth_token)

        # If no config file, run basic connectivity test
        print(f"Testing basic connectivity to {tester.base_url}")
        result = tester.test_api_endpoint('GET', '/')
        print(f"Connectivity test: {'PASSED' if result['passed'] else 'FAILED'}")
        return

    # Run the tests
    print(f"Running {len(criteria)} acceptance criteria tests...")
    print("-" * 50)

    start_time = time.time()
    results = tester.run_acceptance_criteria_tests(criteria)
    end_time = time.time()

    # Print summary
    print("-" * 50)
    print("TEST RESULTS SUMMARY")
    print("-" * 50)
    print(f"Total tests: {results['total_tests']}")
    print(f"Passed: {results['passed_tests']}")
    print(f"Failed: {results['failed_tests']}")
    print(f"Success rate: {(results['passed_tests']/results['total_tests']*100):.1f}%")
    print(f"Total time: {(end_time - start_time):.2f}s")

    if args.format == 'json':
        print(json.dumps(results, indent=2, default=str))

    # Exit with error code if any tests failed
    if results['failed_tests'] > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()