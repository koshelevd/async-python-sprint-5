from email_validator import EmailSyntaxError, validate_email

from db.repositories import UserRepository
from db.tables import User
from dto.users_schemas import TokenSchema
from services.exceptions import BadRequestException, NotAuthorizedException
from utils.auth import (
    create_access_token,
    get_hashed_password,
    verify_password,
)
from utils.const import get_short_url


class UserService:
    """Service for working with users."""

    def __init__(self, *, user_repository: UserRepository):
        self.user_repo = user_repository

    async def signup(self, email: str, password: str) -> User:
        """
        Create new user.

        :param email: email
        :param password: password
        :return: user
        """
        try:
            validate_email(email)
        except EmailSyntaxError as e:
            raise BadRequestException(message=str(e))
        user = await self.user_repo.get_user_by_email(email)
        if user:
            raise BadRequestException("User with this email already exist")
        hash_ = get_hashed_password(password)
        user = self.user_repo.create(email=email, password=hash_)
        self.user_repo.session.add(user)
        await self.user_repo.session.commit()
        return user

    async def signin(self, email: str, password: str) -> TokenSchema:
        """
        Sign in user.

        :param email: email
        :param password: password
        :return: user
        """
        user = await self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            raise BadRequestException("Wrong email or password")

        access_token = create_access_token(user.email)
        refresh_token = create_access_token(user.email)
        result = TokenSchema(
            access_token=access_token, refresh_token=refresh_token
        )
        return result

    async def get_user_status(self, user: User):
        """
        Get user status.

        :param user: user
        :return: user status
        """
        ...
