from typing import Annotated
from fastapi import APIRouter, Depends

from wapang.app.users.models import User
from wapang.app.auth.utils import login_with_header
from wapang.app.orders.services import OrderService
from wapang.app.orders.schemas import OrderCreateRequest, OrderStatusUpdateRequest, OrderResponse

order_router = APIRouter()

@order_router.post("/", status_code=201)
def create_order(
    user: Annotated[User, Depends(login_with_header)],
    request: OrderCreateRequest,
    order_service: Annotated[OrderService, Depends()]
) -> OrderResponse:
    return order_service.create_order(user, request)

@order_router.get("/{order_id}")
def get_order(
    order_id: str,
    user: Annotated[User, Depends(login_with_header)],
    order_service: Annotated[OrderService, Depends()]
) -> OrderResponse:
    return order_service.get_order(user, order_id)

@order_router.patch("/{order_id}", status_code=200)
def update_order_status(
    order_id: str,
    request: OrderStatusUpdateRequest,
    user: Annotated[User, Depends(login_with_header)],
    order_service: Annotated[OrderService, Depends()]
):
    order_status = order_service.update_order_status(user, order_id, request)
    return {"status": order_status}