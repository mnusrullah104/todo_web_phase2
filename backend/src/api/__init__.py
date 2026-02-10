from fastapi import APIRouter
from .tasks import router as tasks_router
from .auth import router as auth_router
from .chat import router as chat_router

router = APIRouter()

# Include auth routes
router.include_router(auth_router)

# Include task routes - the user_id will be part of the path
router.include_router(tasks_router, prefix="/{user_id}")

# Include chat routes (Phase III - AI Chatbot)
router.include_router(chat_router)