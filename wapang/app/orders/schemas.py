from pydantic import BaseModel
from typing import Annotated
from pydantic.functional_validators import AfterValidator

from wapang.app.orders.models import StatusEnum
from wapang.app.items.schemas import validate_stock

class ItemRequest(BaseModel):
    item_id: str
    quantity: Annotated[int, AfterValidator(validate_stock)]

class OrderCreateRequest(BaseModel):
    items: list[ItemRequest]

class ItemResponse(BaseModel):
    item_id: str
    item_name: str
    price: int
    quantity: int
    subtotal: int

class OrderDetailResponse(BaseModel):
    store_id: str
    store_name: str
    delivery_fee: int
    store_total_price: int
    items: list[ItemResponse]

class OrderUserResponse(BaseModel):
    order_id: str
    total_price: int
    status: StatusEnum

class OrderResponse(BaseModel):
    order_id: str
    details: list[OrderDetailResponse]
    total_price: int
    status: StatusEnum

class OrderStatusUpdateRequest(BaseModel):
    status: StatusEnum