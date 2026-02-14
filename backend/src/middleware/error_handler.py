"""
Global error handling middleware for FastAPI
Provides consistent error responses and logging
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback
from typing import Union

logger = logging.getLogger(__name__)


class ErrorResponse:
    """Standardized error response structure"""

    @staticmethod
    def create(
        success: bool = False,
        message: str = "An error occurred",
        status_code: int = 500,
        details: Union[dict, list, None] = None
    ) -> dict:
        """Create a standardized error response"""
        response = {
            "success": success,
            "message": message,
            "status_code": status_code
        }
        if details:
            response["details"] = details
        return response


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with user-friendly messages"""

    # Map status codes to user-friendly messages
    user_messages = {
        400: "Invalid request. Please check your input.",
        401: "Authentication required. Please log in.",
        403: "You don't have permission to perform this action.",
        404: "The requested resource was not found.",
        409: "This action conflicts with existing data.",
        422: "Invalid data provided. Please check your input.",
        429: "Too many requests. Please try again later.",
        500: "An internal error occurred. Please try again.",
        503: "Service temporarily unavailable. Please try again later."
    }

    # Use custom message if provided, otherwise use default
    message = exc.detail if exc.detail else user_messages.get(
        exc.status_code,
        "An unexpected error occurred"
    )

    # Log the error
    logger.warning(
        f"HTTP {exc.status_code}: {message} - Path: {request.url.path}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse.create(
            success=False,
            message=message,
            status_code=exc.status_code
        )
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed field information"""

    # Extract validation errors
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(
        f"Validation error on {request.url.path}: {errors}"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse.create(
            success=False,
            message="Validation error. Please check your input.",
            status_code=422,
            details=errors
        )
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""

    # Log the full traceback for debugging
    logger.error(
        f"Unhandled exception on {request.url.path}: {str(exc)}\n"
        f"Traceback: {traceback.format_exc()}"
    )

    # Don't expose internal errors in production
    # Return a generic message
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse.create(
            success=False,
            message="An unexpected error occurred. Our team has been notified.",
            status_code=500
        )
    )


def setup_error_handlers(app):
    """Register all error handlers with the FastAPI app"""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
