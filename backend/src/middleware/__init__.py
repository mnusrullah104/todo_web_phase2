"""Middleware package for FastAPI application"""
from .error_handler import setup_error_handlers

__all__ = ["setup_error_handlers"]
