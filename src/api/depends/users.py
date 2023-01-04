from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories import UserRepository
from db.tables import User
from db.utils.db_session import get_session
from dto.users_schemas import TokenPayload
from services import UserService
from services.exceptions import NotAuthorizedException, NotFoundValueException
from settings.api import api_settings

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth",
    scheme_name="JWT",
    auto_error=False,
)


async def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)


async def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository=repository)


async def get_current_user(
    token: str = Depends(reuseable_oauth),
    repository: UserRepository = Depends(get_user_repository),
) -> User | None:
    if token is None:
        raise NotAuthorizedException(["User"])
    try:
        payload = jwt.decode(
            token,
            api_settings.JWT_SECRET_KEY,
            algorithms=[api_settings.ALGORITHM],
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await repository.get_user_by_email(token_data.sub)
    if user is None:
        raise NotFoundValueException(["User"])
    return user
