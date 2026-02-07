from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.repositories.user import UserRepository
from app.schemas.users import UserCreate, UserPublic, UserLogin
from app.schemas.generic import APIResponse, LoginResponse
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import create_user, login_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", status_code=status.HTTP_200_OK)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> APIResponse:
    """
    Register a new user.

    Args:
        user (UserCreate): The user data to create.
        db (AsyncSession): The database session.

    Returns:
        APIResponse: The created user object.
    """
    user_repo = UserRepository(db)
    existing_user = await user_repo.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    db_user = await create_user(user_repo, user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed"
        )
    return APIResponse(
        response={
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
        },
        message=f"User {user.username} created successfully",
    )


@router.post("/login", response_model=LoginResponse)
async def authenticate_user(
    response: Response,
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    """
    Authenticate a user.

    Args:
        user (UserBase): The user data to authenticate.
        db (AsyncSession): The database session.

    Returns:
        User: The authenticated user object.
    """
    user_repo = UserRepository(db)
    login_result = await login_user(user_repo, user.username, user.password)
    if not login_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized account or invalid credentials.",
        )
    user_data = login_result.get("user", dict())
    access_token = login_result.get("access_token", "")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=3600,
        samesite="lax",
        secure=False,
    )
    return LoginResponse(
        message=f"User {user_data.username} authenticated successfully",
        access_token=access_token,
        user=UserPublic(
            id=user_data.id,
            email=user_data.email,
            username=user_data.username,
            role=user_data.role,
            is_active=user_data.is_active,
            full_name=(
                f"{user_data.first_name} {user_data.last_name}"
                if user_data.first_name and user_data.last_name
                else None
            ),
        ),
    )
