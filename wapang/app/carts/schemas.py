from pydantic import BaseModel
from typing import Annotated
from pydantic.functional_validators import AfterValidator
from wapang.app.orders.schemas import OrderDetailResponse
from wapang.app.items.schemas import validate_stock

class CartItemRequest(BaseModel):
    item_id: str
    quantity: Annotated[int, AfterValidator(validate_stock)]

class CartResponse(BaseModel):
    details: list[OrderDetailResponse]
    total_price: int