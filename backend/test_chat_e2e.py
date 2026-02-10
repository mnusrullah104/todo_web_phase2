"""
End-to-end test for Phase III AI Chatbot Integration.

Tests all 5 MCP tools through the chat endpoint with Cohere API.
"""
import requests
import json
from uuid import uuid4

# Configuration
BASE_URL = "http://localhost:8001"
TEST_USER_ID = "123e4567-e89b-12d3-a456-426614174000"
conversation_id = None

def send_message(message):
    """Send a message to the chat endpoint."""
    global conversation_id

    url = f"{BASE_URL}/api/{TEST_USER_ID}/chat"
    payload = {
        "message": message,
        "conversation_id": conversation_id
    }

    print(f"\n{'='*60}")
    print(f"USER: {message}")
    print(f"{'='*60}")

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        conversation_id = data["conversation_id"]
        print(f"ASSISTANT: {data['response']}")
        if data.get('tool_calls'):
            print(f"\nTools used: {[tc['tool'] for tc in data['tool_calls']]}")
        return data
    else:
        print(f"ERROR: {response.status_code} - {response.text}")
        return None

def main():
    """Run end-to-end tests."""
    print("\n" + "="*60)
    print("Phase III AI Chatbot - End-to-End Test")
    print("="*60)

    # Test 1: Add tasks
    print("\n[TEST 1] Adding tasks...")
    send_message("Add a task to buy groceries")
    send_message("Create a task to call dentist tomorrow")
    send_message("Add finish report with description needs charts and data")

    # Test 2: List tasks
    print("\n[TEST 2] Listing tasks...")
    send_message("What's on my list?")
    send_message("Show my pending tasks")

    # Test 3: Complete task
    print("\n[TEST 3] Completing a task...")
    send_message("Mark buy groceries as done")
    send_message("Show completed tasks")

    # Test 4: Update task
    print("\n[TEST 4] Updating a task...")
    send_message("Change call dentist to call dentist and schedule cleaning")

    # Test 5: Delete task
    print("\n[TEST 5] Deleting a task...")
    send_message("Delete the groceries task")
    send_message("What's on my list now?")

    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)

if __name__ == "__main__":
    main()
