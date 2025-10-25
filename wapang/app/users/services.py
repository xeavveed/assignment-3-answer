from typing import Annotated
from argon2 import PasswordHasher

from fastapi import Depends
from wapang.app.users.models import User
from wapang.app.users.repositories import UserRepository
from wapang.app.users.exceptions import EmailAlreadyExistsException
from wapang.app.users.schemas import UserUpdateRequest
from wapang.common.exceptions import InvalidFormatException

class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()]) -> None:
        self.user_repository = user_repository

    def create_user(self, email: str, password: str) -> User:        
        if self.user_repository.get_user_by_email(email):
            raise EmailAlreadyExistsException()

        hashed_password = PasswordHasher().hash(password)

        return self.user_repository.create_user(email, hashed_password)

    def update_user(self, request: UserUpdateRequest, user: User) -> User:
        if not any([request.nickname, request.address, request.phone_number]):
            raise InvalidFormatException()
        for key, value in request.model_dump(exclude_none=True).items():
            setattr(user, key, value)
        self.user_repository.update_user(user)
        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.user_repository.get_user_by_id(user_id)