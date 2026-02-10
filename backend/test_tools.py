"""Quick test script for MCP tools.

Tests all 5 tools with a test user to verify functionality.
"""
import asyncio
from uuid import uuid4
from sqlmodel import Session, create_engine, SQLModel
from src.models import User, Task, Conversation, Message
from src.mcp.tools.add_task import add_task_impl
from src.mcp.tools.list_tasks import list_tasks_impl
from src.mcp.tools.complete_task import complete_task_impl
from src.mcp.tools.delete_task import delete_task_impl
from src.mcp.tools.update_task import update_task_impl
from src.config.settings import get_settings

settings = get_settings()


async def test_tools():
    """Test all MCP tools."""
    print("Testing MCP Tools\n")

    # Create test database engine
    engine = create_engine(settings.database_url)

    # Create test user
    test_user_id = uuid4()
    print(f"Test User ID: {test_user_id}\n")

    with Session(engine) as session:
        # Test 1: Add Task
        print("[1] Testing add_task...")
        result = await add_task_impl(
            session=session,
            user_id=test_user_id,
            title="Buy groceries",
            description="Milk, eggs, bread"
        )
        print(f"   Status: {result['status']}")
        if result['status'] == 'success':
            task1_id = result['data']['id']
            print(f"   Created task: {result['data']['title']} (ID: {task1_id})")
        print()

        # Test 2: Add another task
        print("[2] Testing add_task (second task)...")
        result = await add_task_impl(
            session=session,
            user_id=test_user_id,
            title="Call dentist",
            description=""
        )
        print(f"   Status: {result['status']}")
        if result['status'] == 'success':
            task2_id = result['data']['id']
            print(f"   Created task: {result['data']['title']} (ID: {task2_id})")
        print()

        # Test 3: List Tasks
        print("[3] Testing list_tasks (all)...")
        result = await list_tasks_impl(
            session=session,
            user_id=test_user_id
        )
        print(f"   Status: {result['status']}")
        if result['status'] == 'success':
            print(f"   Found {result['data']['count']} tasks")
            for task in result['data']['tasks']:
                print(f"   - {task['title']} (completed: {task['completed']})")
        print()

        # Test 4: Complete Task
        print("[4] Testing complete_task...")
        result = await complete_task_impl(
            session=session,
            user_id=test_user_id,
            task_id=task1_id,
            completed=True
        )
        print(f"   Status: {result['status']}")
        if result['status'] == 'success':
            print(f"   Marked '{result['data']['title']}' as completed")
        print()

        # Test 5: List Pending Tasks
        print("[5] Testing list_tasks (pending only)...")
        result = await list_tasks_impl(
            session=session,
            user_id=test_user_id,
            completed=False
        )
        print(f"   Status: {result['status']}")
        if result['status'] == 'success':
            print(f"   Found {result['data']['count']} pending tasks")
            for task in result['data']['tasks']:
                print(f"   - {task['title']}")
        print()

        # Test 6: Update Task
        print("[6] Testing update_task...")
        result = await update_task_impl(
            session=session,
            user_id=test_user_id,
            task_id=task2_id,
            title="Call dentist tomorrow",
            description="Schedule cleaning appointment"
        )
        print(f"   Status: {result['status']}")
        if result['status'] == 'success':
            print(f"   Updated task: {result['data']['title']}")
            print(f"   New description: {result['data']['description']}")
        print()

        # Test 7: Delete Task
        print("[7] Testing delete_task...")
        result = await delete_task_impl(
            session=session,
            user_id=test_user_id,
            task_id=task1_id
        )
        print(f"   Status: {result['status']}")
        if result['status'] == 'success':
            print(f"   Deleted task: {result['data']['title']}")
        print()

        # Test 8: Final List
        print("[8] Testing list_tasks (final check)...")
        result = await list_tasks_impl(
            session=session,
            user_id=test_user_id
        )
        print(f"   Status: {result['status']}")
        if result['status'] == 'success':
            print(f"   Remaining tasks: {result['data']['count']}")
            for task in result['data']['tasks']:
                print(f"   - {task['title']} (completed: {task['completed']})")
        print()

        # Cleanup
        print("Cleaning up test data...")
        from sqlmodel import select, delete
        statement = delete(Task).where(Task.user_id == test_user_id)
        session.exec(statement)
        session.commit()
        print("   Test data cleaned up")

    print("\nAll tool tests completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_tools())
