from typing import Annotated
from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator

from wapang.common.exceptions import InvalidFormatException
from wapang.app.users.schemas import skip_none

def validate_item_name(v: str) -> str:
    if not v or len(v) > 50:
        raise InvalidFormatException()
    return v

def validate_price(v: int) -> int:
    if v < 0:
        raise InvalidFormatException()
    return v

def validate_stock(v: int) -> int:
    if v < 0:
        raise InvalidFormatException()
    return v

class ItemCreateRequest(BaseModel):
    item_name: Annotated[str, AfterValidator(validate_item_name)]
    price: Annotated[int, AfterValidator(validate_price)]
    stock: Annotated[int, AfterValidator(validate_stock)]

class ItemUpdateRequest(BaseModel):
    item_name: Annotated[str | None, AfterValidator(skip_none(validate_item_name))] = None
    price: Annotated[int | None, AfterValidator(skip_none(validate_price))] = None
    stock: Annotated[int | None, AfterValidator(skip_none(validate_stock))] = None

class ItemResponse(BaseModel):
    id: str
    item_name: str
    price: int
    stock: int

    class Config:
        from_attributes = True

class ItemQueryParams(BaseModel):
    store_id: str | None = None
    min_price: int | None = None
    max_price: int | None = None
    in_stock: bool = False