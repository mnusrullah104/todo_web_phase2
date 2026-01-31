"""
Tests for QA Specialist processes and validation
"""

import unittest
import json
import yaml
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys
import os

# Add the scripts directory to the path to import the QA tester
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

class TestQATester(unittest.TestCase):
    """Test the QA Tester functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Import here to avoid issues when the module is not available during initialization
        from automated_qa_runner import QATester

        self.tester = QATester("http://test-api.com")

    @patch('requests.Session.request')
    def test_api_endpoint_success(self, mock_request):
        """Test successful API endpoint test"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "success"}
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b'{"data": "success"}'

        mock_request.return_value = mock_response

        result = self.tester.test_api_endpoint('GET', '/test', expected_status=200)

        self.assertTrue(result['passed'])
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['expected_status'], 200)
        self.assertEqual(result['response_body']['data'], 'success')

    @patch('requests.Session.request')
    def test_api_endpoint_failure(self, mock_request):
        """Test API endpoint test with failure"""
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_response.headers = {}
        mock_response.content = b''

        mock_request.return_value = mock_response

        result = self.tester.test_api_endpoint('GET', '/test', expected_status=200)

        self.assertFalse(result['passed'])
        self.assertEqual(result['status_code'], 404)
        self.assertEqual(result['expected_status'], 200)
        self.assertIn('error', result)

    @patch('requests.Session.request')
    def test_unauthorized_access(self, mock_request):
        """Test unauthorized access validation"""
        # Mock 401 response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_response.elapsed.total_seconds.return_value = 0.05
        mock_response.content = b'{"error": "Unauthorized"}'

        mock_request.return_value = mock_response

        # Add auth token first
        self.tester.add_auth_header("valid_token")

        # Remove auth header for this specific test
        auth_header = self.tester.session.headers.pop('Authorization', None)
        result = self.tester.test_api_endpoint('GET', '/protected', expected_status=401)

        # Restore auth header
        if auth_header:
            self.tester.session.headers['Authorization'] = auth_header

        self.assertTrue(result['passed'])
        self.assertEqual(result['status_code'], 401)

    def test_add_auth_header(self):
        """Test adding authentication header"""
        self.tester.add_auth_header("test_token")

        self.assertIn('Authorization', self.tester.session.headers)
        self.assertEqual(self.tester.session.headers['Authorization'], 'Bearer test_token')

    def test_run_acceptance_criteria_tests_empty(self):
        """Test running acceptance criteria tests with empty list"""
        results = self.tester.run_acceptance_criteria_tests([])

        self.assertEqual(results['total_tests'], 0)
        self.assertEqual(results['passed_tests'], 0)
        self.assertEqual(results['failed_tests'], 0)
        self.assertEqual(len(results['results']), 0)

class TestAcceptanceCriteriaVerification(unittest.TestCase):
    """Test acceptance criteria verification concepts"""

    def test_criteria_format_validation(self):
        """Test that acceptance criteria follow proper format"""
        criteria_examples = [
            {
                "description": "Given user is logged in, when requesting tasks, then return list of tasks",
                "type": "api_test",
                "method": "GET",
                "endpoint": "/api/v1/tasks",
                "expected_status": 200
            },
            {
                "description": "Verify unauthorized access returns 401",
                "type": "unauthorized_test",
                "method": "GET",
                "endpoint": "/api/v1/tasks"
            }
        ]

        for criterion in criteria_examples:
            # Validate required fields exist
            self.assertIn('description', criterion)
            self.assertIn('type', criterion)

            # Validate type is valid
            valid_types = ['api_test', 'unauthorized_test', 'validation_test']
            self.assertIn(criterion['type'], valid_types)

            # Validate description is meaningful
            self.assertGreater(len(criterion['description']), 0)

    def test_error_handling_criteria(self):
        """Test error handling criteria validation"""
        error_criteria = {
            "description": "Verify 401 Unauthorized for missing JWT",
            "type": "unauthorized_test",
            "method": "GET",
            "endpoint": "/api/v1/protected"
        }

        self.assertEqual(error_criteria['type'], 'unauthorized_test')
        self.assertIn('endpoint', error_criteria)
        self.assertIn('method', error_criteria)

class TestConfiguration(unittest.TestCase):
    """Test configuration file handling"""

    def test_sample_config_validity(self):
        """Test that the sample configuration is valid"""
        config_path = Path(__file__).parent.parent / "assets" / "sample_test_config.yaml"

        self.assertTrue(config_path.exists(), f"Sample config file not found at {config_path}")

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Validate basic structure
        self.assertIn('base_url', config)
        self.assertIn('acceptance_criteria', config)
        self.assertIsInstance(config['acceptance_criteria'], list)
        self.assertGreater(len(config['acceptance_criteria']), 0)

    def test_criteria_completeness(self):
        """Test that criteria in sample config are complete"""
        config_path = Path(__file__).parent.parent / "assets" / "sample_test_config.yaml"

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        for i, criterion in enumerate(config['acceptance_criteria']):
            with self.subTest(criterion_index=i):
                # Check that each criterion has required fields
                self.assertIn('description', criterion, f"Criterion {i} missing description")
                self.assertIn('type', criterion, f"Criterion {i} missing type")

                # Check that type is valid
                valid_types = ['api_test', 'unauthorized_test', 'validation_test']
                self.assertIn(criterion['type'], valid_types, f"Criterion {i} has invalid type: {criterion['type']}")

class TestErrorHandlingValidation(unittest.TestCase):
    """Test error handling validation concepts"""

    def test_error_response_format(self):
        """Test standard error response format validation"""
        error_response = {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input parameters",
                "details": "Field 'name' is required",
                "timestamp": "2023-01-01T00:00:00Z",
                "correlationId": "abc-123-def"
            }
        }

        # Validate error response structure
        self.assertIn('error', error_response)
        self.assertIn('code', error_response['error'])
        self.assertIn('message', error_response['error'])

        # Validate required fields are present
        required_fields = ['code', 'message', 'timestamp']
        for field in required_fields:
            self.assertIn(field, error_response['error'])

    def test_status_code_validation(self):
        """Test validation of different HTTP status codes"""
        status_tests = [
            (200, "success"),
            (400, "client_error"),
            (401, "unauthorized"),
            (403, "forbidden"),
            (404, "not_found"),
            (500, "server_error")
        ]

        for status_code, category in status_tests:
            if category in ['client_error', 'unauthorized', 'forbidden', 'not_found', 'server_error']:
                # These are error categories
                self.assertGreaterEqual(status_code, 400, f"Status code {status_code} should be >= 400 for {category}")
            else:
                # These are success categories
                self.assertLess(status_code, 400, f"Status code {status_code} should be < 400 for {category}")

class TestMCPValidation(unittest.TestCase):
    """Test MCP (Model Context Protocol) validation concepts"""

    def test_mcp_tool_format(self):
        """Test MCP tool response format"""
        mcp_response = {
            "result": {
                "id": "task-123",
                "name": "Test Task",
                "status": "created"
            }
        }

        self.assertIn('result', mcp_response)
        self.assertIn('id', mcp_response['result'])
        self.assertIn('name', mcp_response['result'])

    def test_mcp_error_format(self):
        """Test MCP error response format"""
        mcp_error = {
            "error": {
                "code": "MCP_TOOL_ERROR",
                "message": "Tool execution failed",
                "data": {
                    "tool": "add_task",
                    "arguments": {}
                }
            }
        }

        self.assertIn('error', mcp_error)
        self.assertIn('code', mcp_error['error'])
        self.assertIn('message', mcp_error['error'])

def run_all_tests():
    """Run all QA specialist tests"""
    print("Running QA Specialist tests...")

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return success/failure
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    if success:
        print("\n✅ All QA Specialist tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)