from functools import wraps
import re
from typing import Annotated, Callable, TypeVar
from pydantic import BaseModel, EmailStr, field_validator
from pydantic.functional_validators import AfterValidator

from wapang.common.exceptions import InvalidFormatException

def validate_email(v: str) -> str:
    pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    if not isinstance(v, str) or not pattern.match(v):
        raise InvalidFormatException()
    return v

def validate_phone_number(v: str) -> str:
    pattern = re.compile(r"^010-\d{4}-\d{4}$")
    if not pattern.match(v):
        raise InvalidFormatException()
    return v

def validate_password(v: str) -> str:
    if len(v) < 8 or len(v) > 20:
        raise InvalidFormatException()
    return v

def validate_address(v: str) -> str:
    if len(v) > 100:
        raise InvalidFormatException()
    return v

def validate_nickname(v: str) -> str:
    if len(v) > 20:
        raise InvalidFormatException()
    return v

T = TypeVar("T")

def skip_none(validator: Callable[[T], T]) -> Callable[[T | None], T | None]:
    @wraps(validator)
    def wrapper(value: T | None) -> T | None:
        if value is None:
            return value
        return validator(value)

    return wrapper

class UserSignupRequest(BaseModel):
    email: Annotated[str, AfterValidator(validate_email)]
    password: Annotated[str, AfterValidator(validate_password)]

    @field_validator("password", mode="after")
    def validate_password(cls, v) -> str:
        if len(v) < 8 or len(v) > 20:
            raise InvalidFormatException()
        return v
    
class UserUpdateRequest(BaseModel):
    nickname: Annotated[str | None, AfterValidator(skip_none(validate_nickname))] = None
    address: Annotated[str | None, AfterValidator(skip_none(validate_address))] = None
    phone_number: Annotated[str | None, AfterValidator(skip_none(validate_phone_number))] = None

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    nickname: str | None
    address: str | None
    phone_number: str | None
    
    class Config:
        from_attributes = True