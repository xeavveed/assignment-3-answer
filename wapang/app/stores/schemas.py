import re
from typing import Annotated

from pydantic import BaseModel, EmailStr
from pydantic.functional_validators import AfterValidator

from wapang.app.users.schemas import validate_address, validate_phone_number, skip_none
from wapang.common.exceptions import InvalidFormatException

def validate_store_name(v: str) -> str:
    if len(v) < 3 or len(v) > 20:
        raise InvalidFormatException()
    return v

def validate_delivery_fee(v: int) -> int:
    if v < 0:
        raise InvalidFormatException()
    return v

class StoreCreateRequest(BaseModel):
    store_name: Annotated[str, AfterValidator(validate_store_name)]
    address: Annotated[str, AfterValidator(validate_address)]
    email: EmailStr
    phone_number: Annotated[str, AfterValidator(validate_phone_number)]
    delivery_fee: Annotated[int, AfterValidator(validate_delivery_fee)]

    
class StoreUpdateRequest(BaseModel):
    store_name: Annotated[str | None, AfterValidator(skip_none(validate_store_name))] = None
    address: Annotated[str | None, AfterValidator(skip_none(validate_address))] = None
    email: EmailStr | None = None
    phone_number: Annotated[str | None, AfterValidator(skip_none(validate_phone_number))] = None
    delivery_fee: Annotated[int | None, AfterValidator(skip_none(validate_delivery_fee))] = None
    

class StoreResponse(BaseModel):
    id: str
    store_name: str
    address: str
    email: EmailStr
    phone_number: str
    delivery_fee: int