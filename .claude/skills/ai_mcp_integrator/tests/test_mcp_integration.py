"""
Basic tests for MCP and OpenAI integration
"""

import unittest
from unittest.mock import Mock, AsyncMock, patch
import sys
import os

# Add the backend directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

class TestMCPIntegration(unittest.TestCase):
    """Test MCP server functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_context = Mock()
        self.mock_arguments = {"name": "Test Task", "description": "A test task"}

    def test_task_storage_initialization(self):
        """Test that task storage is initialized properly"""
        # Import here to avoid issues with the MCP server running
        from backend.mcp_server.server import TASK_STORAGE

        self.assertIsInstance(TASK_STORAGE, dict)
        self.assertEqual(len(TASK_STORAGE), 0)

    @patch('uuid.uuid4')
    def test_add_task_functionality(self, mock_uuid):
        """Test adding a task via MCP server"""
        # Import here to avoid issues with the MCP server running
        from backend.mcp_server.server import handle_add_task

        # Mock UUID to have a predictable value
        mock_uuid.return_value = "test-uuid-123"

        # Test the function
        result = handle_add_task(self.mock_context, self.mock_arguments)

        expected_result = {
            "result": {
                "id": "test-uuid-123",
                "name": "Test Task",
                "message": "Task 'Test Task' added successfully"
            }
        }

        self.assertEqual(result, expected_result)

    def test_add_task_validation(self):
        """Test validation for add_task function"""
        from backend.mcp_server.server import handle_add_task

        # Test with empty name
        empty_args = {"name": "", "description": "A test task"}

        with self.assertRaises(ValueError) as context:
            handle_add_task(self.mock_context, empty_args)

        self.assertIn("Task name is required", str(context.exception))

    def test_add_task_no_name(self):
        """Test validation when no name is provided"""
        from backend.mcp_server.server import handle_add_task

        # Test with no name
        no_name_args = {"description": "A test task"}

        with self.assertRaises(KeyError):
            handle_add_task(self.mock_context, no_name_args)

class TestOpenAIAgent(unittest.IsolatedAsyncioTestCase):
    """Test OpenAI agent functionality"""

    async def test_agent_initialization(self):
        """Test that the agent initializes correctly with API key"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            from backend.agents.task_agent import TaskAgent

            agent = TaskAgent()

            self.assertIsNotNone(agent.api_key)
            self.assertEqual(agent.model, "gpt-4-turbo")
            self.assertEqual(len(agent.tools), 4)  # add_task, list_tasks, complete_task, delete_task

    async def test_agent_missing_api_key(self):
        """Test that agent raises error without API key"""
        with patch.dict(os.environ, {}, clear=True):
            from backend.agents.task_agent import TaskAgent

            with self.assertRaises(ValueError):
                TaskAgent()

    async def test_get_available_tools(self):
        """Test getting available tools from agent"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            from backend.agents.task_agent import TaskAgent

            agent = TaskAgent()
            tools = agent.get_available_tools()

            expected_tools = ["add_task", "list_tasks", "complete_task", "delete_task"]
            self.assertEqual(set(tools), set(expected_tools))

class TestAPIStructure(unittest.TestCase):
    """Test API structure and routing"""

    def test_import_routes(self):
        """Test that API routes can be imported without errors"""
        try:
            from backend.api.chat_routes import router as chat_router
            from backend.api.task_routes import router as task_router

            self.assertIsNotNone(chat_router)
            self.assertIsNotNone(task_router)
        except ImportError as e:
            self.fail(f"Failed to import API routes: {e}")

if __name__ == '__main__':
    print("Running MCP and OpenAI integration tests...")
    unittest.main(verbosity=2)