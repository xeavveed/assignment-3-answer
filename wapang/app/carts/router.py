from typing import Annotated
from fastapi import APIRouter, Depends, Query

from wapang.app.auth.utils import login_with_header
from wapang.app.carts.schemas import CartItemRequest, CartResponse
from wapang.app.carts.services import CartService
from wapang.app.orders.services import OrderService
from wapang.app.orders.schemas import ItemRequest, ItemRequest, OrderCreateRequest, OrderResponse
from wapang.app.users.models import User


cart_router = APIRouter()

@cart_router.patch("/", status_code=200)
def add_or_update_cart(
    request: CartItemRequest,
    user: Annotated[User, Depends(login_with_header)],
    order_service: Annotated[OrderService, Depends()],
    cart_service: Annotated[CartService, Depends()],
) -> CartResponse:
    details, total_price = cart_service.add_or_update_cart(user, request, order_service)
    return CartResponse(details=details, total_price=total_price)

@cart_router.get("/", status_code=200)
def get_cart_items(
    user: Annotated[User, Depends(login_with_header)],
    order_service: Annotated[OrderService, Depends()],
    cart_service: Annotated[CartService, Depends()],
) -> CartResponse:
    details, total_price = cart_service.get_cart_items(user, order_service)
    return CartResponse(details=details, total_price=total_price)

@cart_router.delete("/", status_code=204)
def clear_cart(
    user: Annotated[User, Depends(login_with_header)],
    cart_service: Annotated[CartService, Depends()],
):
    cart_service.clear_cart(user)

@cart_router.post("/checkout", status_code=201)
def checkout_cart(
    user: Annotated[User, Depends(login_with_header)],
    cart_service: Annotated[CartService, Depends()],
    order_service: Annotated[OrderService, Depends()],
) -> OrderResponse:
    order = cart_service.checkout(user, order_service)
    return order