"""Navigate tool for Phase III AI Chatbot Integration.

Handles page navigation requests from the chatbot.
"""
from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session
import logging

logger = logging.getLogger(__name__)

# Available routes mapping
ROUTE_MAP = {
    "dashboard": "/dashboard",
    "home": "/dashboard",
    "tasks": "/tasks",
    "todo": "/tasks",
    "todos": "/tasks",
    "task list": "/tasks",
    "calendar": "/calendar",
    "schedule": "/calendar",
    "analytics": "/analytics",
    "stats": "/analytics",
    "statistics": "/analytics",
    "reports": "/analytics",
    "settings": "/settings",
    "profile": "/settings",
    "preferences": "/settings",
    "evaluations": "/evaluations",
    "reviews": "/evaluations",
}


async def navigate(
    session: Session,
    user_id: UUID,
    page: str
) -> Dict[str, Any]:
    """Navigate to a specific page.

    Args:
        session: Database session (not used but required for consistency)
        user_id: UUID of the authenticated user
        page: Page name or route to navigate to

    Returns:
        Dict containing navigation result with route
    """
    try:
        # Normalize the page name
        page_lower = page.lower().strip()

        # Find matching route
        route = ROUTE_MAP.get(page_lower)

        if not route:
            # Try partial matching
            for key, value in ROUTE_MAP.items():
                if key in page_lower or page_lower in key:
                    route = value
                    break

        if route:
            logger.info(f"Navigation requested by user {user_id}: {page} -> {route}")
            return {
                "status": "success",
                "route": route,
                "page_name": page,
                "message": f"Navigating to {page}"
            }
        else:
            logger.warning(f"Unknown page requested: {page}")
            available_pages = ", ".join(sorted(set(ROUTE_MAP.keys())))
            return {
                "status": "error",
                "error": "unknown_page",
                "message": f"I don't know how to navigate to '{page}'. Available pages: {available_pages}"
            }

    except Exception as e:
        logger.error(f"Navigation error: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": "navigation_error",
            "message": f"Failed to navigate: {str(e)}"
        }
