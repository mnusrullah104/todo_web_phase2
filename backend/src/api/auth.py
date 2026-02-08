from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional
import uuid
from datetime import timedelta, datetime
import logging
import traceback

from ..auth.jwt import create_access_token, get_password_hash, verify_password
from ..database.session import get_session
from ..config.settings import get_settings
from ..models.user import User, UserCreate, UserLogin

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user and store in PostgreSQL database.
    """
    try:
        logger.info(f"Registration attempt for email: {user_data.email}")

        # Check if user already exists
        statement = select(User).where(User.email == user_data.email)
        existing_user = session.exec(statement).first()

        if existing_user:
            logger.warning(f"Registration failed: Email already exists - {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)

        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Create access token
        access_token_expires = timedelta(minutes=get_settings().access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(new_user.id), "email": new_user.email},
            expires_delta=access_token_expires
        )

        logger.info(f"User registered successfully: {user_data.email}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {"id": str(new_user.id), "email": new_user.email}
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login")
async def login_user(user_data: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate user against PostgreSQL database and return access token.
    """
    try:
        logger.info(f"Login attempt for email: {user_data.email}")

        # Find user by email
        statement = select(User).where(User.email == user_data.email)
        user = session.exec(statement).first()

        if not user or not verify_password(user_data.password, user.hashed_password):
            logger.warning(f"Login failed: Invalid credentials for {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=get_settings().access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        logger.info(f"User logged in successfully: {user_data.email}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {"id": str(user.id), "email": user.email}
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/logout")
async def logout_user():
    """
    Logout endpoint.
    For stateless JWT, the client removes the token from local storage.
    """
    return {"message": "Successfully logged out"}